"""
Tests for health check endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app

client = TestClient(app)


def test_basic_health_check():
    """Test basic health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert "environment" in data
    assert "app_name" in data


@patch('src.api.routers.health.get_db')
def test_detailed_health_check_with_db_success(mock_get_db):
    """Test detailed health check with successful database connection."""
    # Mock database session
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = [1]
    mock_get_db.return_value = mock_db
    
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "components" in data
    assert "database" in data["components"]
    assert data["components"]["database"]["status"] == "healthy"


@patch('src.api.routers.health.get_db')
def test_detailed_health_check_with_db_failure(mock_get_db):
    """Test detailed health check with database connection failure."""
    # Mock database session with exception
    mock_db = MagicMock()
    mock_db.execute.side_effect = Exception("Database connection failed")
    mock_get_db.return_value = mock_db
    
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "degraded"
    assert "components" in data
    assert "database" in data["components"]
    assert data["components"]["database"]["status"] == "unhealthy"


def test_readiness_check():
    """Test readiness check endpoint."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data


def test_liveness_check():
    """Test liveness check endpoint."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data