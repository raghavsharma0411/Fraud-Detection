"""
Database models for ML/GenAI application.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.sql import func

from src.db.database import Base


class ModelInfo(Base):
    """
    Sample table - ML model information and metadata.
    """
    __tablename__ = "model_info"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    version = Column(String(50), nullable=False)
    model_type = Column(String(50), nullable=False)  # 'ml', 'genai', etc.
    description = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    model_size_mb = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    parameters = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Worker(Base):
    """
    Worker table - Employee information.
    """
    __tablename__ = "Worker"
    
    WORKER_ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FIRST_NAME = Column(String(255), nullable=False)
    LAST_NAME = Column(String(255), nullable=False)
    SALARY = Column(Integer, nullable=False)
    JOINING_DATE = Column(DateTime, nullable=False)
    DEPARTMENT = Column(String(255), nullable=False)


# TODO: Add more tables as needed:
# 
# class PredictionLog(Base):
#     """Log of predictions made by ML models."""
#     __tablename__ = "prediction_logs"
#     # ... fields for tracking predictions
#
# class ChatSession(Base):
#     """Chat sessions for GenAI conversations."""
#     __tablename__ = "chat_sessions" 
#     # ... fields for chat sessions
#
# class ChatMessage(Base):
#     """Individual messages in chat sessions."""
#     __tablename__ = "chat_messages"
#     # ... fields for chat messages
#
# class ApiUsage(Base):
#     """API usage tracking for monitoring and billing."""
#     __tablename__ = "api_usage"
#     # ... fields for usage analytics