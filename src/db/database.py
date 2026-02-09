"""
Database connection and session management.
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from src.core.config import settings

# Set up logging
logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
connection_string = settings.sql_server_connection_string
logger.info(f"Database config - Host: {settings.SQL_SERVER_HOST}:{settings.SQL_SERVER_PORT}")
logger.info(f"Database config - Database: {settings.SQL_SERVER_DATABASE}")
logger.info(f"Database config - Driver: {settings.SQL_SERVER_DRIVER}")
logger.info(f"Using connection string: {connection_string.replace(settings.SQL_SERVER_PASSWORD, '***')}")

engine = create_engine(
    connection_string,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Enable connection pool pre-ping
    pool_recycle=300,     # Recycle connections every 5 minutes
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata for reflection and schema operations
metadata = MetaData()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    Yields a SQLAlchemy session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables.
    
    NOTE: Auto table creation is DISABLED by default (AUTO_CREATE_TABLES=False).
    Tables should be created manually using SQL scripts in scripts/ folder.
    """
    if settings.AUTO_CREATE_TABLES:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created automatically")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    else:
        logger.warning("init_db() called but AUTO_CREATE_TABLES is disabled")
        logger.info("Create tables manually using: sqlcmd -i scripts/create_tables.sql")


def check_db_connection() -> bool:
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False