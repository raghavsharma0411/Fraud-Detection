-- Database table creation scripts for ML/GenAI FastAPI application
-- 
-- IMPORTANT: This application is configured to NOT auto-create tables.
-- You MUST run this script manually to create the database schema.
--
-- Usage:
--   1. First run: sqlcmd -S ysidevdb.yardiapp.com,30040 -U collectprocessordev -P collectprocessordev -i init-db.sql
--   2. Then run: sqlcmd -S ysidevdb.yardiapp.com,30040 -U collectprocessordev -P collectprocessordev -i create_tables.sql

USE collectprocessoradmin;
GO

-- Model Information Table
CREATE TABLE model_info (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL UNIQUE,
    version NVARCHAR(50) NOT NULL,
    model_type NVARCHAR(50) NOT NULL,
    description NTEXT NULL,
    file_path NVARCHAR(500) NULL,
    model_size_mb FLOAT NULL,
    accuracy FLOAT NULL,
    parameters NVARCHAR(MAX) NULL, -- JSON data
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NULL
);

-- Create indexes for better performance
CREATE INDEX IX_model_info_name ON model_info(name);
CREATE INDEX IX_model_info_model_type ON model_info(model_type);
CREATE INDEX IX_model_info_is_active ON model_info(is_active);

-- Insert sample data
INSERT INTO model_info (name, version, model_type, description, is_active)
VALUES 
    ('sample_model', '1.0.0', 'ml', 'Sample ML model for testing', 1);

PRINT 'Sample table created successfully.';
GO

-- Worker Table (Employee Information)
CREATE TABLE Worker (
    WORKER_ID INT IDENTITY(1,1) PRIMARY KEY,
    FIRST_NAME NVARCHAR(255) NOT NULL,
    LAST_NAME NVARCHAR(255) NOT NULL,
    SALARY INT NOT NULL,
    JOINING_DATE DATETIME NOT NULL,
    DEPARTMENT NVARCHAR(255) NOT NULL
);

-- Create indexes for better performance
CREATE INDEX IX_Worker_Department ON Worker(DEPARTMENT);
CREATE INDEX IX_Worker_Salary ON Worker(SALARY);
CREATE INDEX IX_Worker_JoiningDate ON Worker(JOINING_DATE);

PRINT 'Worker table created successfully.';
GO

-- ===== FUTURE TABLES (UNCOMMENT WHEN NEEDED) =====

/*
-- Prediction Logs Table
CREATE TABLE prediction_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    model_name NVARCHAR(255) NOT NULL,
    input_data NVARCHAR(MAX) NOT NULL, -- JSON
    prediction NVARCHAR(MAX) NOT NULL, -- JSON
    confidence FLOAT NULL,
    processing_time_ms FLOAT NULL,
    user_id NVARCHAR(255) NULL,
    session_id NVARCHAR(255) NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE()
);

-- Create indexes
CREATE INDEX IX_prediction_logs_model_name ON prediction_logs(model_name);
CREATE INDEX IX_prediction_logs_user_id ON prediction_logs(user_id);
CREATE INDEX IX_prediction_logs_session_id ON prediction_logs(session_id);
CREATE INDEX IX_prediction_logs_created_at ON prediction_logs(created_at);

-- Chat Sessions Table
CREATE TABLE chat_sessions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    session_id NVARCHAR(255) NOT NULL UNIQUE,
    user_id NVARCHAR(255) NULL,
    model_name NVARCHAR(255) NOT NULL,
    title NVARCHAR(255) NULL,
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETUTCDATE(),
    updated_at DATETIME2 NULL
);

-- Create indexes
CREATE INDEX IX_chat_sessions_session_id ON chat_sessions(session_id);
CREATE INDEX IX_chat_sessions_user_id ON chat_sessions(user_id);
CREATE INDEX IX_chat_sessions_is_active ON chat_sessions(is_active);

-- Chat Messages Table
CREATE TABLE chat_messages (
    id INT IDENTITY(1,1) PRIMARY KEY,
    session_id NVARCHAR(255) NOT NULL,
    role NVARCHAR(50) NOT NULL, -- 'user', 'assistant', 'system'
    content NTEXT NOT NULL,
    tokens_used INT NULL,
    model_name NVARCHAR(255) NULL,
    metadata NVARCHAR(MAX) NULL, -- JSON
    created_at DATETIME2 DEFAULT GETUTCDATE()
);

-- Create indexes
CREATE INDEX IX_chat_messages_session_id ON chat_messages(session_id);
CREATE INDEX IX_chat_messages_role ON chat_messages(role);
CREATE INDEX IX_chat_messages_created_at ON chat_messages(created_at);

-- API Usage Table
CREATE TABLE api_usage (
    id INT IDENTITY(1,1) PRIMARY KEY,
    endpoint NVARCHAR(255) NOT NULL,
    method NVARCHAR(10) NOT NULL,
    user_id NVARCHAR(255) NULL,
    response_time_ms FLOAT NULL,
    status_code INT NOT NULL,
    tokens_used INT NULL,
    cost FLOAT NULL,
    error_message NTEXT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE()
);

-- Create indexes
CREATE INDEX IX_api_usage_endpoint ON api_usage(endpoint);
CREATE INDEX IX_api_usage_user_id ON api_usage(user_id);
CREATE INDEX IX_api_usage_status_code ON api_usage(status_code);
CREATE INDEX IX_api_usage_created_at ON api_usage(created_at);
*/