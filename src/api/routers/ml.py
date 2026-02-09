"""
Machine Learning model endpoints.
"""
import os
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import pandas as pd
import joblib

from src.core.config import settings

router = APIRouter()

# ---------------------------------------------------
# Load artifacts at startup (VERY IMPORTANT)
# ---------------------------------------------------
model = None
scaler = None
model_columns = None

def load_fraud_models():
    """Load fraud detection models from disk."""
    global model, scaler, model_columns
    
    models_dir = "models"
    
    try:
        model_path = os.path.join(models_dir, "fraud_model.pkl")
        scaler_path = os.path.join(models_dir, "scaler.pkl")
        columns_path = os.path.join(models_dir, "model_columns.pkl")
        
        if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(columns_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            model_columns = joblib.load(columns_path)
            print("✅ Fraud detection models loaded successfully")
        else:
            print("⚠️  Model files not found. Please ensure fraud_model.pkl, scaler.pkl, and model_columns.pkl are in the models/ directory")
    except Exception as e:
        print(f"❌ Error loading models: {e}")

# Load models when module is imported
load_fraud_models()


# ---------------------------------------------------
# Request schema (input)
# ---------------------------------------------------
class Transaction(BaseModel):
    """Transaction data for fraud detection."""
    transaction_id: int
    customer_id: int
    amount: float
    is_weekend: int
    night_transaction: int
    card_not_present: int
    account_age_days: int
    new_merchant: int
    international_txn: int
    impossible_travel: int
    txn_velocity_5min: int
    new_device_high_amount: int
    blacklisted_ip: int
    multiple_cards_same_device: int
    tx_hour: int
    tx_day: int
    tx_month: int


class FraudPredictionResponse(BaseModel):
    """Response model for fraud prediction."""
    transaction_id: int
    customer_id: int
    fraud_prediction: int
    fraud_probability: float
    risk_level: str


class BatchTransactionRequest(BaseModel):
    """Request model for batch transaction processing."""
    transactions: list[Transaction]


class BatchPredictionResponse(BaseModel):
    """Response model for batch fraud predictions."""
    total_transactions: int
    successful_predictions: int
    failed_predictions: int
    results: list[FraudPredictionResponse]
    errors: list[dict] = []


# ---------------------------------------------------
# Risk rule function
# ---------------------------------------------------
def risk_category(prob: float) -> str:
    """
    Categorize risk based on fraud probability using configurable thresholds.
    
    Thresholds and labels can be customized via environment variables:
    - FRAUD_RISK_LOW_THRESHOLD (default: 0.3)
    - FRAUD_RISK_HIGH_THRESHOLD (default: 0.7)
    - FRAUD_RISK_NORMAL_LABEL, FRAUD_RISK_MODERATE_LABEL, FRAUD_RISK_HIGH_LABEL
    """
    if prob >= settings.FRAUD_RISK_HIGH_THRESHOLD:
        return settings.FRAUD_RISK_HIGH_LABEL
    elif prob >= settings.FRAUD_RISK_LOW_THRESHOLD:
        return settings.FRAUD_RISK_MODERATE_LABEL
    else:
        return settings.FRAUD_RISK_NORMAL_LABEL


# ---------------------------------------------------
# Endpoints
# ---------------------------------------------------

@router.get("/models")
async def list_models() -> Dict[str, Any]:
    """List available ML models and their status."""
    models_status = {
        "fraud_detection": {
            "loaded": model is not None and scaler is not None and model_columns is not None,
            "model_file": "fraud_model.pkl",
            "scaler_file": "scaler.pkl", 
            "columns_file": "model_columns.pkl"
        }
    }
    
    return {
        "models": models_status,
        "message": "ML models status"
    }


def _predict_single_transaction(txn: Transaction) -> FraudPredictionResponse:
    """
    Internal helper function to predict fraud for a single transaction.
    
    Args:
        txn: Transaction data
        
    Returns:
        Fraud prediction response
        
    Raises:
        Exception: If prediction fails
    """
    # Convert to dataframe
    df = pd.DataFrame([txn.dict()])
    
    # Keep IDs for response
    txn_id = df["transaction_id"].iloc[0]
    cust_id = df["customer_id"].iloc[0]
    
    # Keep all columns including IDs as they were part of training data
    df_model = df.copy()
    
    # Verify all required columns are present
    missing_cols = [col for col in model_columns if col not in df_model.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Ensure feature order matches training data exactly
    df_model = df_model[model_columns]
    
    # Scale features
    scaled = scaler.transform(df_model)
    
    # Make predictions
    pred = int(model.predict(scaled)[0])
    prob = float(model.predict_proba(scaled)[0][1])  # Probability of fraud (class 1)
    
    return FraudPredictionResponse(
        transaction_id=txn_id,
        customer_id=cust_id,
        fraud_prediction=pred,
        fraud_probability=round(prob, 4),
        risk_level=risk_category(prob)
    )


@router.post("/predict/transaction", response_model=FraudPredictionResponse)
async def predict_fraud(txn: Transaction) -> FraudPredictionResponse:
    """
    Predict fraud probability for a transaction.
    
    Args:
        txn: Transaction data
        
    Returns:
        Fraud prediction with probability and risk level
        
    Raises:
        HTTPException: 503 if models not loaded or prediction fails
    """
    # Check if models are loaded
    if model is None or scaler is None or model_columns is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fraud detection models not loaded. Please check model files in models/ directory."
        )
    
    try:
        return _predict_single_transaction(txn)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error making prediction: {str(e)}"
        )


@router.post("/predict/transactions/batch", response_model=BatchPredictionResponse)
async def predict_fraud_batch(batch_request: BatchTransactionRequest) -> BatchPredictionResponse:
    """
    Predict fraud probability for multiple transactions in batch.
    
    Args:
        batch_request: Batch of transactions to process
        
    Returns:
        Batch fraud prediction results with success/error counts
        
    Raises:
        HTTPException: 503 if models not loaded, 400 if no transactions provided
    """
    # Check if models are loaded
    if model is None or scaler is None or model_columns is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fraud detection models not loaded. Please check model files in models/ directory."
        )
    
    # Validate input
    if not batch_request.transactions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No transactions provided for batch processing."
        )
    
    results = []
    errors = []
    successful_predictions = 0
    failed_predictions = 0
    
    # Process each transaction
    for i, txn in enumerate(batch_request.transactions):
        try:
            prediction = _predict_single_transaction(txn)
            results.append(prediction)
            successful_predictions += 1
            
        except Exception as e:
            failed_predictions += 1
            errors.append({
                "transaction_index": i,
                "transaction_id": txn.transaction_id,
                "error": str(e)
            })
    
    return BatchPredictionResponse(
        total_transactions=len(batch_request.transactions),
        successful_predictions=successful_predictions,
        failed_predictions=failed_predictions,
        results=results,
        errors=errors
    )


@router.post("/reload-models")
async def reload_models() -> Dict[str, Any]:
    """
    Reload fraud detection models from disk.
    
    Returns:
        Status of model reloading
    """
    try:
        load_fraud_models()
        
        models_loaded = model is not None and scaler is not None and model_columns is not None
        
        return {
            "success": models_loaded,
            "message": "Models reloaded successfully" if models_loaded else "Failed to load models"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reloading models: {str(e)}"
        )


@router.get("/risk-config")
async def get_risk_configuration() -> Dict[str, Any]:
    """
    Get current fraud risk thresholds and labels configuration.
    
    Returns:
        Dictionary with current risk configuration settings
    """
    return {
        "risk_thresholds": {
            "low_threshold": settings.FRAUD_RISK_LOW_THRESHOLD,
            "high_threshold": settings.FRAUD_RISK_HIGH_THRESHOLD,
            "explanation": f"0.0 - {settings.FRAUD_RISK_LOW_THRESHOLD-0.01:.2f}: {settings.FRAUD_RISK_NORMAL_LABEL}, "
                         f"{settings.FRAUD_RISK_LOW_THRESHOLD:.2f} - {settings.FRAUD_RISK_HIGH_THRESHOLD-0.01:.2f}: {settings.FRAUD_RISK_MODERATE_LABEL}, "
                         f"{settings.FRAUD_RISK_HIGH_THRESHOLD:.2f} - 1.0: {settings.FRAUD_RISK_HIGH_LABEL}"
        },
        "risk_labels": {
            "normal": settings.FRAUD_RISK_NORMAL_LABEL,
            "moderate": settings.FRAUD_RISK_MODERATE_LABEL,
            "high": settings.FRAUD_RISK_HIGH_LABEL
        },
        "environment_variables": {
            "FRAUD_RISK_LOW_THRESHOLD": f"Set to {settings.FRAUD_RISK_LOW_THRESHOLD} (default: 0.3)",
            "FRAUD_RISK_HIGH_THRESHOLD": f"Set to {settings.FRAUD_RISK_HIGH_THRESHOLD} (default: 0.7)",
            "FRAUD_RISK_NORMAL_LABEL": f"Set to '{settings.FRAUD_RISK_NORMAL_LABEL}' (default: 'Normal / No Risk')",
            "FRAUD_RISK_MODERATE_LABEL": f"Set to '{settings.FRAUD_RISK_MODERATE_LABEL}' (default: 'Moderate Risk (Verify)')",
            "FRAUD_RISK_HIGH_LABEL": f"Set to '{settings.FRAUD_RISK_HIGH_LABEL}' (default: 'High Risk (Avoid)')"
        }
    }