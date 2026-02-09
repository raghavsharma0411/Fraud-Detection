"""
Application configuration settings.
"""
import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # ===== CURRENTLY ACTIVE SETTINGS =====
    
    # Application settings - Used in main.py and health endpoints
    APP_NAME: str = Field(default="ML-GenAI FastAPI", env="APP_NAME")  # FastAPI title and startup logs
    VERSION: str = Field(default="1.0.0", env="VERSION")  # API version and health checks
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")  # Environment tracking
    DEBUG: bool = Field(default=True, env="DEBUG")  # Controls SQL logging and uvicorn reload
    
    # Server settings - Used in main.py for uvicorn server
    HOST: str = Field(default="0.0.0.0", env="HOST")  # Server bind address
    PORT: int = Field(default=8000, env="PORT")  # Server port
    
    # CORS settings - Used in main.py for cross-origin requests
    ALLOWED_ORIGINS: List[str] = Field(default=["*"], env="ALLOWED_ORIGINS")  # CORS allowed origins
    
    # SQL Server settings - Used in database.py for connection
    SQL_SERVER_HOST: str = Field(default="ysidevdb.yardiapp.com", env="SQL_SERVER_HOST")  # Database host
    SQL_SERVER_PORT: int = Field(default=30040, env="SQL_SERVER_PORT")  # Database port
    SQL_SERVER_DATABASE: str = Field(default="collectprocessoradmin", env="SQL_SERVER_DATABASE")  # Database name
    SQL_SERVER_USERNAME: str = Field(default="collectprocessordev", env="SQL_SERVER_USERNAME")  # Database user
    SQL_SERVER_PASSWORD: str = Field(default="collectprocessordev", env="SQL_SERVER_PASSWORD")  # Database password
    SQL_SERVER_DRIVER: str = Field(default="ODBC Driver 17 for SQL Server", env="SQL_SERVER_DRIVER")  # ODBC driver
    SQL_SERVER_TRUST_CERT: bool = Field(default=True, env="SQL_SERVER_TRUST_CERT")  # Trust server certificate
    SQL_SERVER_ENCRYPT: bool = Field(default=True, env="SQL_SERVER_ENCRYPT")  # Encrypt connection
    
    # Database behavior settings
    AUTO_CREATE_TABLES: bool = Field(default=False, env="AUTO_CREATE_TABLES")  # DISABLED: Tables created manually via SQL
    
    # ML settings - Used in health.py for model directory checking and ml.py for predictions
    ML_MODEL_PATH: str = Field(default="./models", env="ML_MODEL_PATH")  # Path to ML model files
    
    # Fraud Detection Risk Thresholds - Used in ml.py for risk categorization
    FRAUD_RISK_LOW_THRESHOLD: float = Field(default=0.3, env="FRAUD_RISK_LOW_THRESHOLD")  # Below this = Normal risk
    FRAUD_RISK_HIGH_THRESHOLD: float = Field(default=0.7, env="FRAUD_RISK_HIGH_THRESHOLD")  # Above this = High risk
    
    # Fraud Detection Risk Labels - Used in ml.py for risk level descriptions
    FRAUD_RISK_NORMAL_LABEL: str = Field(default="Normal / No Risk", env="FRAUD_RISK_NORMAL_LABEL")  # Low risk label
    FRAUD_RISK_MODERATE_LABEL: str = Field(default="Moderate Risk (Verify)", env="FRAUD_RISK_MODERATE_LABEL")  # Medium risk label
    FRAUD_RISK_HIGH_LABEL: str = Field(default="High Risk (Avoid)", env="FRAUD_RISK_HIGH_LABEL")  # High risk label
    
    # ===== COMMENTED OUT - NOT CURRENTLY USED =====
    
    # # Security settings - Uncomment when implementing JWT tokens or sessions
    # SECRET_KEY: str = Field(default="your-secret-key-change-this", env="SECRET_KEY")  # For JWT tokens, sessions
    
    # # ML settings - Uncomment when implementing ML model loading
    # MAX_MODEL_SIZE_MB: int = Field(default=500, env="MAX_MODEL_SIZE_MB")  # Max model file size limit
    # DEFAULT_MODEL_TIMEOUT: int = Field(default=30, env="DEFAULT_MODEL_TIMEOUT")  # Model prediction timeout
    
    # # GenAI settings - Uncomment when implementing GenAI integrations
    # OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")  # OpenAI API access
    # AZURE_OPENAI_API_KEY: Optional[str] = Field(default=None, env="AZURE_OPENAI_API_KEY")  # Azure OpenAI access
    # AZURE_OPENAI_ENDPOINT: Optional[str] = Field(default=None, env="AZURE_OPENAI_ENDPOINT")  # Azure endpoint URL
    # HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")  # HuggingFace API access
    
    # # Logging settings - Uncomment when implementing structured logging
    # LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")  # Python logging level
    # LOG_FORMAT: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT")  # Log format
    
    # ===== ACTIVE PROPERTIES =====
    @property
    def sql_server_connection_string(self) -> str:
        """Generate SQL Server connection string - USED in database.py"""
        driver_name = self.SQL_SERVER_DRIVER.replace(' ', '+')
        
        # Basic connection string
        base_string = (
            f"mssql+pyodbc://{self.SQL_SERVER_USERNAME}:{self.SQL_SERVER_PASSWORD}@"
            f"{self.SQL_SERVER_HOST}:{self.SQL_SERVER_PORT}/{self.SQL_SERVER_DATABASE}"
            f"?driver={driver_name}"
        )
        
        # Only add SSL parameters for modern drivers
        if "ODBC Driver" in self.SQL_SERVER_DRIVER:
            trust_cert = "yes" if self.SQL_SERVER_TRUST_CERT else "no"
            encrypt = "yes" if self.SQL_SERVER_ENCRYPT else "no"
            base_string += f"&TrustServerCertificate={trust_cert}&Encrypt={encrypt}"
        
        return base_string
    
    # ===== COMMENTED OUT PROPERTIES - NOT CURRENTLY USED =====
    # @property
    # def sql_server_async_connection_string(self) -> str:
    #     """Generate async SQL Server connection string - For future async database operations"""
    #     trust_cert = "yes" if self.SQL_SERVER_TRUST_CERT else "no"
    #     return (
    #         f"mssql+aioodbc://{self.SQL_SERVER_USERNAME}:{self.SQL_SERVER_PASSWORD}@"
    #         f"{self.SQL_SERVER_HOST}:{self.SQL_SERVER_PORT}/{self.SQL_SERVER_DATABASE}"
    #         f"?driver={self.SQL_SERVER_DRIVER.replace(' ', '+')}&TrustServerCertificate={trust_cert}"
    #     )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create global settings instance
settings = Settings()