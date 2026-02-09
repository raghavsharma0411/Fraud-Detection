# 🤖 ML Fraud Detection API Documentation

## Overview

The ML Fraud Detection API provides endpoints for detecting fraudulent transactions using machine learning models. The API supports both single transaction predictions and batch processing for multiple transactions.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Model Setup](#model-setup)
- [Available Endpoints](#available-endpoints)
- [Single Transaction Prediction](#single-transaction-prediction)
- [Batch Transaction Prediction](#batch-transaction-prediction)
- [Model Management](#model-management)
- [Risk Configuration](#risk-configuration)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Prerequisites

Before using the fraud detection endpoints, ensure you have:

1. **Required Model Files**: Place these files in `models/` directory:
   - `fraud_model.pkl` - Trained fraud detection model
   - `scaler.pkl` - Feature scaler used during training
   - `model_columns.pkl` - Column order from training data

2. **Dependencies**: All required packages are listed in `requirements.txt`

3. **Running Application**: Start the FastAPI application on `http://localhost:8000`

## Model Setup

### 📁 Model Files Location

```
C:\CP-AI\models\
├── fraud_model.pkl      # Trained ML model (e.g., Random Forest, XGBoost)
├── scaler.pkl           # StandardScaler or similar preprocessing
└── model_columns.pkl    # List of feature column names and order
```

### 🔄 Model Loading

Models are loaded automatically when the application starts. If models are not found, you'll receive a `503 Service Unavailable` error when making predictions.

## Available Endpoints

### Base URL
```
http://localhost:8000/api/v1/ml
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/models` | Check model loading status |
| POST   | `/predict/transaction` | Single transaction prediction |
| POST   | `/predict/transactions/batch` | Batch transaction predictions |
| POST   | `/reload-models` | Reload models from disk |
| GET    | `/risk-config` | Get current risk configuration |

---

## Single Transaction Prediction

### 🎯 Endpoint
```http
POST /api/v1/ml/predict/transaction
```

### 📥 Request Body

```json
{
  "transaction_id": 12345,
  "customer_id": 67890,
  "amount": 150.0,
  "is_weekend": 0,
  "night_transaction": 1,
  "card_not_present": 1,
  "account_age_days": 365,
  "new_merchant": 0,
  "international_txn": 0,
  "impossible_travel": 0,
  "txn_velocity_5min": 2,
  "new_device_high_amount": 0,
  "blacklisted_ip": 0,
  "multiple_cards_same_device": 0,
  "tx_hour": 23,
  "tx_day": 15,
  "tx_month": 11
}
```

### 📤 Response

```json
{
  "transaction_id": 12345,
  "customer_id": 67890,
  "fraud_prediction": 0,
  "fraud_probability": 0.1234,
  "risk_level": "Normal / No Risk"
}
```

### 📊 Field Descriptions

#### Request Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `transaction_id` | int | Unique transaction identifier | `12345` |
| `customer_id` | int | Unique customer identifier | `67890` |
| `amount` | float | Transaction amount | `150.0` |
| `is_weekend` | int | 1 if weekend, 0 otherwise | `0` |
| `night_transaction` | int | 1 if night time (e.g., 10PM-6AM), 0 otherwise | `1` |
| `card_not_present` | int | 1 if card not physically present, 0 otherwise | `1` |
| `account_age_days` | int | Age of customer account in days | `365` |
| `new_merchant` | int | 1 if first transaction with merchant, 0 otherwise | `0` |
| `international_txn` | int | 1 if international transaction, 0 otherwise | `0` |
| `impossible_travel` | int | 1 if geographically impossible travel, 0 otherwise | `0` |
| `txn_velocity_5min` | int | Number of transactions in last 5 minutes | `2` |
| `new_device_high_amount` | int | 1 if new device with high amount, 0 otherwise | `0` |
| `blacklisted_ip` | int | 1 if IP is blacklisted, 0 otherwise | `0` |
| `multiple_cards_same_device` | int | 1 if multiple cards used on same device, 0 otherwise | `0` |
| `tx_hour` | int | Hour of transaction (0-23) | `23` |
| `tx_day` | int | Day of month (1-31) | `15` |
| `tx_month` | int | Month (1-12) | `11` |

#### Response Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `transaction_id` | int | Original transaction ID | `12345` |
| `customer_id` | int | Original customer ID | `67890` |
| `fraud_prediction` | int | Binary prediction: 0 (legitimate), 1 (fraud) | `0` |
| `fraud_probability` | float | Probability of fraud (0.0-1.0) | `0.1234` |
| `risk_level` | string | Risk categorization | `"Normal / No Risk"` |

#### Risk Levels

| Probability Range | Risk Level | Recommendation |
|-------------------|------------|----------------|
| 0.0 - 0.29 | `"Normal / No Risk"` | Allow transaction |
| 0.3 - 0.69 | `"Moderate Risk (Verify)"` | Request additional verification |
| 0.7 - 1.0 | `"High Risk (Avoid)"` | Block or review transaction |

> **📝 Note**: Risk thresholds and labels are **configurable** via environment variables. See [Risk Configuration](#risk-configuration) section below.

---

## Batch Transaction Prediction

### 🎯 Endpoint
```http
POST /api/v1/ml/predict/transactions/batch
```

### 📥 Request Body

```json
{
  "transactions": [
    {
      "transaction_id": 8001,
      "customer_id": 3001,
      "amount": 120,
      "is_weekend": 0,
      "night_transaction": 0,
      "card_not_present": 0,
      "account_age_days": 900,
      "new_merchant": 0,
      "international_txn": 0,
      "impossible_travel": 0,
      "txn_velocity_5min": 1,
      "new_device_high_amount": 0,
      "blacklisted_ip": 0,
      "multiple_cards_same_device": 0,
      "tx_hour": 11,
      "tx_day": 10,
      "tx_month": 1
    },
    {
      "transaction_id": 8002,
      "customer_id": 3002,
      "amount": 9800,
      "is_weekend": 1,
      "night_transaction": 1,
      "card_not_present": 1,
      "account_age_days": 3,
      "new_merchant": 1,
      "international_txn": 1,
      "impossible_travel": 1,
      "txn_velocity_5min": 9,
      "new_device_high_amount": 1,
      "blacklisted_ip": 1,
      "multiple_cards_same_device": 1,
      "tx_hour": 3,
      "tx_day": 21,
      "tx_month": 1
    }
  ]
}
```

### 📤 Response

```json
{
  "total_transactions": 2,
  "successful_predictions": 2,
  "failed_predictions": 0,
  "results": [
    {
      "transaction_id": 8001,
      "customer_id": 3001,
      "fraud_prediction": 0,
      "fraud_probability": 0.0542,
      "risk_level": "Normal / No Risk"
    },
    {
      "transaction_id": 8002,
      "customer_id": 3002,
      "fraud_prediction": 1,
      "fraud_probability": 0.9876,
      "risk_level": "High Risk (Avoid)"
    }
  ],
  "errors": []
}
```

### 📊 Batch Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `total_transactions` | int | Total number of transactions processed |
| `successful_predictions` | int | Number of successful predictions |
| `failed_predictions` | int | Number of failed predictions |
| `results` | array | Array of successful prediction results |
| `errors` | array | Array of error details for failed predictions |

### ⚠️ Error Response (When Some Transactions Fail)

```json
{
  "total_transactions": 3,
  "successful_predictions": 2,
  "failed_predictions": 1,
  "results": [
    {
      "transaction_id": 8001,
      "customer_id": 3001,
      "fraud_prediction": 0,
      "fraud_probability": 0.0542,
      "risk_level": "Normal / No Risk"
    }
  ],
  "errors": [
    {
      "transaction_index": 2,
      "transaction_id": 8003,
      "error": "Missing required columns: ['amount']"
    }
  ]
}
```

---

## Model Management

### 🔍 Check Model Status

```http
GET /api/v1/ml/models
```

**Response:**
```json
{
  "models": {
    "fraud_detection": {
      "loaded": true,
      "model_file": "fraud_model.pkl",
      "scaler_file": "scaler.pkl",
      "columns_file": "model_columns.pkl"
    }
  },
  "message": "ML models status"
}
```

### 🔄 Reload Models

```http
POST /api/v1/ml/reload-models
```

**Response:**
```json
{
  "success": true,
  "message": "Models reloaded successfully"
}
```

---

## Risk Configuration

### 🎛️ Customizable Risk Thresholds

The fraud detection system uses configurable risk thresholds that can be customized via environment variables. This allows different organizations to set their own risk tolerance levels.

### 📊 Default Configuration

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Low Threshold** | `0.3` | Below this = Normal Risk |
| **High Threshold** | `0.7` | Above this = High Risk |
| **Normal Label** | `"Normal / No Risk"` | Low risk description |
| **Moderate Label** | `"Moderate Risk (Verify)"` | Medium risk description |
| **High Label** | `"High Risk (Avoid)"` | High risk description |

### ⚙️ Environment Variables

Add these to your `.env` file to customize risk levels:

```env
# Risk Thresholds (0.0 - 1.0)
FRAUD_RISK_LOW_THRESHOLD=0.3
FRAUD_RISK_HIGH_THRESHOLD=0.7

# Custom Risk Labels
FRAUD_RISK_NORMAL_LABEL=Normal / No Risk
FRAUD_RISK_MODERATE_LABEL=Moderate Risk (Verify)
FRAUD_RISK_HIGH_LABEL=High Risk (Avoid)
```

### 📝 Example Customizations

#### Conservative Risk Settings (Lower Tolerance)
```env
FRAUD_RISK_LOW_THRESHOLD=0.2
FRAUD_RISK_HIGH_THRESHOLD=0.5
FRAUD_RISK_MODERATE_LABEL=Review Required
FRAUD_RISK_HIGH_LABEL=Block Transaction
```

#### Aggressive Risk Settings (Higher Tolerance)
```env
FRAUD_RISK_LOW_THRESHOLD=0.5
FRAUD_RISK_HIGH_THRESHOLD=0.8
FRAUD_RISK_NORMAL_LABEL=Approved
FRAUD_RISK_MODERATE_LABEL=Manual Review
FRAUD_RISK_HIGH_LABEL=Suspected Fraud
```

### 🔍 Check Current Configuration

```http
GET /api/v1/ml/risk-config
```

**Response:**
```json
{
  "risk_thresholds": {
    "low_threshold": 0.3,
    "high_threshold": 0.7,
    "explanation": "0.0 - 0.29: Normal / No Risk, 0.30 - 0.69: Moderate Risk (Verify), 0.70 - 1.0: High Risk (Avoid)"
  },
  "risk_labels": {
    "normal": "Normal / No Risk",
    "moderate": "Moderate Risk (Verify)",
    "high": "High Risk (Avoid)"
  },
  "environment_variables": {
    "FRAUD_RISK_LOW_THRESHOLD": "Set to 0.3 (default: 0.3)",
    "FRAUD_RISK_HIGH_THRESHOLD": "Set to 0.7 (default: 0.7)",
    "FRAUD_RISK_NORMAL_LABEL": "Set to 'Normal / No Risk' (default: 'Normal / No Risk')",
    "FRAUD_RISK_MODERATE_LABEL": "Set to 'Moderate Risk (Verify)' (default: 'Moderate Risk (Verify)')",
    "FRAUD_RISK_HIGH_LABEL": "Set to 'High Risk (Avoid)' (default: 'High Risk (Avoid)')"
  }
}
```

### 🔄 Applying Changes

After updating environment variables:
1. **Restart the application** for changes to take effect
2. **Verify configuration** using the `/risk-config` endpoint
3. **Test with sample transactions** to confirm new thresholds

### ⚠️ Important Notes

- **Threshold Validation**: `FRAUD_RISK_LOW_THRESHOLD` must be less than `FRAUD_RISK_HIGH_THRESHOLD`
- **Range**: Both thresholds must be between 0.0 and 1.0
- **No Runtime Changes**: Configuration is loaded at startup - restart required for changes
- **Backward Compatibility**: Default values maintain existing behavior if not configured

---

## Error Handling

### HTTP Status Codes

| Status Code | Description | Possible Causes |
|-------------|-------------|-----------------|
| `200` | Success | Request processed successfully |
| `400` | Bad Request | Invalid input data, missing required fields |
| `503` | Service Unavailable | Models not loaded, model files missing |
| `500` | Internal Server Error | Prediction error, model compatibility issues |

### Common Error Responses

#### Models Not Loaded
```json
{
  "detail": "Fraud detection models not loaded. Please check model files in models/ directory."
}
```

#### Missing Required Fields
```json
{
  "detail": "Missing required columns: ['amount', 'customer_id']"
}
```

#### Empty Batch Request
```json
{
  "detail": "No transactions provided for batch processing."
}
```

---

## Examples

### 🌐 cURL Examples

#### Single Transaction Prediction

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/ml/predict/transaction' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "transaction_id": 12345,
    "customer_id": 67890,
    "amount": 150.0,
    "is_weekend": 0,
    "night_transaction": 1,
    "card_not_present": 1,
    "account_age_days": 365,
    "new_merchant": 0,
    "international_txn": 0,
    "impossible_travel": 0,
    "txn_velocity_5min": 2,
    "new_device_high_amount": 0,
    "blacklisted_ip": 0,
    "multiple_cards_same_device": 0,
    "tx_hour": 23,
    "tx_day": 15,
    "tx_month": 11
  }'
```

#### Batch Transaction Prediction

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/ml/predict/transactions/batch' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "transactions": [
      {
        "transaction_id": 8001,
        "customer_id": 3001,
        "amount": 120,
        "is_weekend": 0,
        "night_transaction": 0,
        "card_not_present": 0,
        "account_age_days": 900,
        "new_merchant": 0,
        "international_txn": 0,
        "impossible_travel": 0,
        "txn_velocity_5min": 1,
        "new_device_high_amount": 0,
        "blacklisted_ip": 0,
        "multiple_cards_same_device": 0,
        "tx_hour": 11,
        "tx_day": 10,
        "tx_month": 1
      }
    ]
  }'
```

### 🐍 Python Examples

#### Using requests library

```python
import requests
import json

# Single transaction prediction
url = "http://localhost:8000/api/v1/ml/predict/transaction"
transaction_data = {
    "transaction_id": 12345,
    "customer_id": 67890,
    "amount": 150.0,
    "is_weekend": 0,
    "night_transaction": 1,
    "card_not_present": 1,
    "account_age_days": 365,
    "new_merchant": 0,
    "international_txn": 0,
    "impossible_travel": 0,
    "txn_velocity_5min": 2,
    "new_device_high_amount": 0,
    "blacklisted_ip": 0,
    "multiple_cards_same_device": 0,
    "tx_hour": 23,
    "tx_day": 15,
    "tx_month": 11
}

response = requests.post(url, json=transaction_data)
if response.status_code == 200:
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']}")
    print(f"Risk Level: {result['risk_level']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

#### Batch Processing

```python
# Batch transaction prediction
batch_url = "http://localhost:8000/api/v1/ml/predict/transactions/batch"
batch_data = {
    "transactions": [
        {
            "transaction_id": 8001,
            "customer_id": 3001,
            "amount": 120,
            # ... other fields
        },
        {
            "transaction_id": 8002,
            "customer_id": 3002,
            "amount": 9800,
            # ... other fields
        }
    ]
}

response = requests.post(batch_url, json=batch_data)
if response.status_code == 200:
    result = response.json()
    print(f"Total: {result['total_transactions']}")
    print(f"Successful: {result['successful_predictions']}")
    print(f"Failed: {result['failed_predictions']}")
    
    for prediction in result['results']:
        print(f"Transaction {prediction['transaction_id']}: {prediction['risk_level']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### 🌐 JavaScript Examples

#### Using fetch API

```javascript
// Single transaction prediction
async function predictSingleTransaction() {
    const url = 'http://localhost:8000/api/v1/ml/predict/transaction';
    const transactionData = {
        transaction_id: 12345,
        customer_id: 67890,
        amount: 150.0,
        is_weekend: 0,
        night_transaction: 1,
        card_not_present: 1,
        account_age_days: 365,
        new_merchant: 0,
        international_txn: 0,
        impossible_travel: 0,
        txn_velocity_5min: 2,
        new_device_high_amount: 0,
        blacklisted_ip: 0,
        multiple_cards_same_device: 0,
        tx_hour: 23,
        tx_day: 15,
        tx_month: 11
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(transactionData)
        });

        if (response.ok) {
            const result = await response.json();
            console.log(`Fraud Probability: ${result.fraud_probability}`);
            console.log(`Risk Level: ${result.risk_level}`);
        } else {
            console.error(`Error: ${response.status}`);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}

// Batch transaction prediction
async function predictBatchTransactions() {
    const url = 'http://localhost:8000/api/v1/ml/predict/transactions/batch';
    const batchData = {
        transactions: [
            {
                transaction_id: 8001,
                customer_id: 3001,
                amount: 120,
                // ... other fields
            }
        ]
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(batchData)
        });

        if (response.ok) {
            const result = await response.json();
            console.log(`Total: ${result.total_transactions}`);
            console.log(`Successful: ${result.successful_predictions}`);
            
            result.results.forEach(prediction => {
                console.log(`Transaction ${prediction.transaction_id}: ${prediction.risk_level}`);
            });
        } else {
            console.error(`Error: ${response.status}`);
        }
    } catch (error) {
        console.error('Request failed:', error);
    }
}
```

---

## 🔧 Troubleshooting

### Common Issues

1. **Models Not Loading**
   - Ensure all three model files exist in `models/` directory
   - Check file permissions
   - Verify model files are valid pickle files

2. **Column Mismatch Errors**
   - Ensure all required fields are included in request
   - Verify field names match exactly (case-sensitive)
   - Check that `model_columns.pkl` matches your training data

3. **Prediction Errors**
   - Ensure model was trained with same feature engineering
   - Verify scaler is compatible with current features
   - Check for data type mismatches

4. **Performance Issues**
   - For high-volume batch processing, consider breaking into smaller batches
   - Monitor memory usage with large batch sizes
   - Consider model optimization for production deployment

---

## 📈 Performance Considerations

### Batch Processing
- **Recommended batch size**: 100-500 transactions
- **Memory usage**: ~1MB per 1000 transactions
- **Processing time**: ~50ms per transaction (depends on model complexity)

### Scaling Tips
- Use batch endpoints for multiple transactions
- Implement caching for frequently accessed models
- Consider model quantization for faster inference
- Monitor API response times and adjust batch sizes accordingly

---

## 🔐 Security Notes

- **Data Privacy**: Transaction data contains sensitive information
- **Input Validation**: All inputs are validated before processing
- **Error Messages**: Error messages do not expose internal system details
- **Model Security**: Model files should be protected and version-controlled

---

## 📞 Support

For issues or questions:
- Check application logs for detailed error information
- Use `/api/v1/ml/models` endpoint to verify model status
- Refer to the main project README for general setup instructions

---

*Last Updated: February 2026*
*API Version: 1.0*