"""
Health check endpoints.
"""
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.core.config import settings
from src.db.database import get_db

router = APIRouter()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint.
    Returns application status and basic information.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "app_name": settings.APP_NAME
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Detailed health check including database connectivity.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "app_name": settings.APP_NAME,
        "components": {}
    }
    
    # Check database connectivity
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        health_status["components"]["database"] = {
            "status": "healthy" if result else "unhealthy",
            "details": "SQL Server connection successful",
            "connection_info": {
                "host": settings.SQL_SERVER_HOST,
                "port": settings.SQL_SERVER_PORT,
                "database": settings.SQL_SERVER_DATABASE,
                "driver": settings.SQL_SERVER_DRIVER
            }
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "details": f"Database connection failed: {str(e)}",
            "connection_info": {
                "host": settings.SQL_SERVER_HOST,
                "port": settings.SQL_SERVER_PORT,
                "database": settings.SQL_SERVER_DATABASE,
                "driver": settings.SQL_SERVER_DRIVER
            }
        }
        
    # Check available ODBC drivers
    try:
        import pyodbc
        available_drivers = pyodbc.drivers()
        health_status["components"]["odbc_drivers"] = {
            "status": "healthy",
            "available_drivers": available_drivers
        }
    except Exception as e:
        health_status["components"]["odbc_drivers"] = {
            "status": "warning",
            "details": f"Could not list ODBC drivers: {str(e)}"
        }
    
    # Check ML models directory
    import os
    ml_model_path = settings.ML_MODEL_PATH
    if os.path.exists(ml_model_path):
        model_count = len([f for f in os.listdir(ml_model_path) if os.path.isfile(os.path.join(ml_model_path, f))])
        health_status["components"]["ml_models"] = {
            "status": "healthy",
            "details": f"Models directory exists with {model_count} files"
        }
    else:
        health_status["components"]["ml_models"] = {
            "status": "warning",
            "details": "Models directory does not exist"
        }
    
    return health_status


@router.get("/health/ready")
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check for Kubernetes/container orchestration.
    """
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check for Kubernetes/container orchestration.
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }