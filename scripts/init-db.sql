-- Basic database setup for ML/GenAI FastAPI application
-- NOTE: Using existing database 'collectprocessoradmin'
-- This script will verify database exists and is accessible

USE master;
GO

-- Check if database exists and is accessible
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'collectprocessoradmin')
BEGIN
    PRINT 'Database collectprocessoradmin found and accessible.';
END
ELSE
BEGIN
    PRINT 'ERROR: Database collectprocessoradmin not found!';
    PRINT 'Please ensure you have access to the database.';
END
GO

PRINT 'Database verification completed.';
PRINT 'Next step: Run create_tables.sql to create application tables.';
GO