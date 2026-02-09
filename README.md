# 🚀 CollectProcessor AI - FastAPI ML/GenAI Application

A production-ready FastAPI application designed for machine learning and generative AI workloads with enterprise-grade SQL Server integration. Built for scalability, maintainability, and easy deployment.

## ✨ Features

- 🔥 **FastAPI Framework**: High-performance async web framework with automatic API documentation
- 🛡️ **Enterprise Security**: Non-root containers, environment-based configuration, manual schema management
- 🗃️ **SQL Server Integration**: Production-ready database connection with connection pooling
- 🐳 **Docker Ready**: Multi-stage builds with optimized production images
- 📊 **Health Monitoring**: Comprehensive health checks for application and database
- 🔧 **Environment Management**: Flexible configuration system with `.env` support
- 📈 **Scalable Architecture**: Modular design with ML fraud detection and GenAI integrations
- 🧪 **Testing Framework**: Built-in testing structure with pytest
- 📝 **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## 📂 Project Structure

```
collectprocessor-AI/
├── 📁 src/                          # Main application source code
│   ├── 📁 api/                      # API layer
│   │   └── 📁 routers/              # API route definitions
│   │       ├── health.py            # ❤️  Health check endpoints
│   │       ├── workers.py           # 👥 Worker management endpoints  
│   │       ├── ml.py                # 🤖 Machine learning fraud detection endpoints
│   │       └── genai.py             # 🧠 Generative AI endpoints (ready for expansion)
│   ├── 📁 core/                     # Core application components
│   │   └── config.py                # ⚙️  Environment & database configuration
│   ├── 📁 db/                       # Database layer
│   │   ├── database.py              # 🔌 Database connection & session management
│   │   └── models.py                # 📊 SQLAlchemy database models
│   ├── 📁 ml/                       # 🤖 ML utilities & fraud detection models
│   └── 📁 genai/                    # 🧠 GenAI integrations & providers (expandable)
├── 📁 scripts/                      # Database & setup scripts
│   ├── init-db.sql                 # 🗃️  Database initialization
│   └── create_tables.sql           # 📋 Table creation scripts
├── 📁 models/                       # 💾 ML model storage directory
├── 📁 tests/                        # 🧪 Test suite
│   ├── test_health.py              # ❤️  Health endpoint tests
│   └── conftest.py                 # 🔧 Test configuration
├── 📄 main.py                       # 🚀 FastAPI application entry point
├── 📄 requirements.txt              # 📦 Python dependencies
├── 📄 Dockerfile                    # 🐳 Container build instructions
├── 📄 docker-compose.yml           # 🐙 Multi-container orchestration
├── 📄 .env.example                 # 📝 Environment variables template
├── 📄 .gitignore                   # 🙈 Git ignore patterns
└── 📄 README.md                    # 📖 This documentation
```

## 🚀 Quick Start Guide

### Prerequisites

- **Docker & Docker Desktop** (for containerized deployment)
- **Python 3.11+** (for local development)  
- **SQL Server access** (your existing database)
- **Git** (for cloning the repository)

---

### 🐳 Option 1: Docker Setup (Recommended)

**Perfect for production-like environment and easy deployment**

#### Step 1: Clone & Setup Environment
```bash
# Clone the repository
git clone https://github.com/yardidev/collectprocessor-AI.git
cd collectprocessor-AI

# Create your environment file from template
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows
```

#### Step 2: Configure Environment Variables
Edit `.env` file with your database details:
```env
# SQL Server Settings - Update with your values
SQL_SERVER_HOST=your-database-host.com
SQL_SERVER_PORT=1433
SQL_SERVER_DATABASE=your_database_name
SQL_SERVER_USERNAME=your_username
SQL_SERVER_PASSWORD=your_password
SQL_SERVER_DRIVER=ODBC Driver 18 for SQL Server
```

> ⚠️ **Security Note**: Never commit `.env` files to version control. The `.env.example` file serves as a template - copy it to `.env` and update with your actual credentials.

#### Step 3: Database Setup (One-time only)
```bash
# Create required database tables
# Connect to your SQL Server and run:
sqlcmd -S your-server -U your-user -P your-password -i scripts/create_tables.sql
```

#### Step 4: Launch with Docker
```bash
# Start Docker Desktop first, then:
docker-compose up -d --build

# Check container status
docker-compose ps

# View logs
docker-compose logs -f app
```

#### Step 5: Verify Installation
- 📚 **API Documentation**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/api/v1/health
- 👥 **Workers API**: http://localhost:8000/api/v1/workers
- 🔍 **Detailed Health**: http://localhost:8000/api/v1/health/detailed

---

### 💻 Option 2: Local Development Setup

**Perfect for development, debugging, and code modifications**

#### Step 1: Environment Setup
```bash
# Clone repository
git clone https://github.com/yardidev/collectprocessor-AI.git
cd collectprocessor-AI

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### Step 2: Configure Environment
```bash
# Create environment file
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit .env with your database credentials
```

#### Step 3: Database Setup
```bash
# Run database initialization (one-time)
sqlcmd -S your-server -U your-user -P your-password -i scripts/create_tables.sql
```

#### Step 4: Run Application
```bash
# Start the FastAPI application
python main.py

# Application will start on http://localhost:8000
```

## 🗃️ Database Configuration

### 🔐 Connection String Format

The application uses the following SQL Server connection format:
```
Server=your-host,port;Database=your-db;User Id=username;Password=password;Encrypt=True;TrustServerCertificate=True;
```

### 📋 Manual Schema Management

**🚨 IMPORTANT**: This application does **NOT** auto-create database tables for production safety.

#### Why Manual Database Setup?
- ✅ **Production Safety**: Prevents accidental schema modifications
- ✅ **Version Control**: All database changes are tracked in SQL files
- ✅ **Team Collaboration**: Schema changes require explicit review
- ✅ **Migration Control**: Full control over when and how schema changes occur
- ✅ **Environment Consistency**: Ensures identical schema across all environments

#### Database Setup Steps
```bash
# Method 1: Using SQL Command Line
sqlcmd -S your-server,port -U your-username -P your-password -i scripts/create_tables.sql

# Method 2: Using SQL Server Management Studio (SSMS)
# 1. Connect to your SQL Server instance
# 2. Open scripts/create_tables.sql
# 3. Execute the script

# Method 3: Using Azure Data Studio
# 1. Connect to your SQL Server
# 2. Open scripts/create_tables.sql  
# 3. Run the script
```

### 🔧 Environment Variables Configuration

Edit your `.env` file with your database details:

```env
# Application Settings
APP_NAME=CollectProcessor AI
APP_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
DEBUG=true

# CORS Settings  
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# SQL Server Configuration
SQL_SERVER_HOST=your-database-host.com
SQL_SERVER_PORT=1433
SQL_SERVER_DATABASE=your_database_name  
SQL_SERVER_USERNAME=your_username
SQL_SERVER_PASSWORD=your_password
SQL_SERVER_DRIVER=ODBC Driver 18 for SQL Server
SQL_SERVER_TRUST_CERT=true
SQL_SERVER_ENCRYPT=true

# Database Behavior
AUTO_CREATE_TABLES=false  # Keep this false for production safety

# ML Model Settings (Future Use)
ML_MODEL_PATH=./models
```

## 📡 API Documentation

### 🔍 Available Endpoints

#### Health Monitoring
- **GET** `/api/v1/health` - Basic health check
  ```json
  {"status": "healthy", "timestamp": "2026-02-07T10:30:00Z"}
  ```

- **GET** `/api/v1/health/detailed` - Comprehensive health check with database status
  ```json
  {
    "status": "healthy",
    "timestamp": "2026-02-07T10:30:00Z", 
    "database": {
      "status": "connected",
      "host": "your-db-host.com",
      "port": 1433,
      "database": "your_database"
    },
    "available_drivers": ["ODBC Driver 18 for SQL Server", "SQL Server"]
  }
  ```

#### Workers Management
- **GET** `/api/v1/workers` - Retrieve all workers
  ```json
  [
    {
      "worker_id": 1,
      "first_name": "John",
      "last_name": "Doe", 
      "salary": 50000,
      "joining_date": "2023-01-15",
      "department": "Engineering"
    }
  ]
  ```

#### ML Fraud Detection (NEW! 🚀)
- **POST** `/api/v1/ml/predict/transaction` - Single fraud prediction
- **POST** `/api/v1/ml/predict/transactions/batch` - Batch fraud predictions
- **GET** `/api/v1/ml/models` - Check model status
- **POST** `/api/v1/ml/reload-models` - Reload models

#### GenAI (Ready for Expansion)
- **GET** `/api/v1/genai/status` - GenAI service status

### 📚 Interactive API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 📖 Detailed API Documentation

- **[ML Fraud Detection API](docs/ML_FRAUD_DETECTION_API.md)** - Complete guide with examples
- **[Documentation Index](docs/README.md)** - All available documentation

---

## 🛠️ Development Guide

### 🧪 Running Tests
```bash
# Install test dependencies (included in requirements.txt)
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_health.py -v
```

### 🐳 Docker Commands

```bash
# Build and start services
docker-compose up -d --build

# View logs
docker-compose logs -f app

# Execute commands in container
docker-compose exec app bash

# Stop services
docker-compose down

# Rebuild single service
docker-compose build app

# Scale service (if needed)
docker-compose up -d --scale app=3
```

### 🔧 Local Development Tips

```bash
# Install dependencies in development mode
pip install -e .

# Run with auto-reload for development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Format code
black src/
isort src/

# Type checking
mypy src/
```

---

## 🚨 Troubleshooting

### Common Issues & Solutions

#### ❌ Database Connection Failed
```bash
# Check 1: Verify database credentials in .env
# Check 2: Ensure SQL Server is accessible from your network
# Check 3: Test connection manually
sqlcmd -S your-host,port -U username -P password -Q "SELECT 1"

# Check 4: ODBC Driver availability
docker-compose exec app odbcinst -q -d
```

#### ❌ Docker Build Failed
```bash
# Clear Docker cache and rebuild
docker system prune -a
docker-compose build --no-cache app
```

#### ❌ Permission Denied Errors
```bash
# Check file permissions
chmod +x scripts/*.sh

# For Docker on Linux/Mac
sudo chown -R $USER:$USER .
```

#### ❌ Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Change port in docker-compose.yml or .env
```

---

## 🔮 What's Next?

### Immediate Capabilities
- ✅ **RESTful API**: FastAPI with automatic documentation
- ✅ **Database Integration**: SQL Server with connection pooling  
- ✅ **Health Monitoring**: Application and database health checks
- ✅ **Worker Management**: CRUD operations for worker entities
- ✅ **Docker Deployment**: Production-ready containerization
- ✅ **Environment Configuration**: Flexible settings management

### Ready for Expansion
- 🤖 **ML Model Integration**: Deploy and serve machine learning models
- 🧠 **GenAI Services**: Integrate with OpenAI, Anthropic, or other AI providers
- 📊 **Data Analytics**: Add reporting and analytics endpoints
- 🔐 **Authentication**: JWT or OAuth2 integration ready
- 📈 **Monitoring**: Prometheus metrics and logging integration
- 🚀 **CI/CD**: GitHub Actions workflows for automated deployment

### Suggested Next Steps
1. **Add Authentication**: Implement JWT or API key authentication
2. **ML Model Deployment**: Add your first machine learning model endpoint
3. **GenAI Integration**: Connect to your preferred AI service provider
4. **Database Expansion**: Add more entities and relationships
5. **Monitoring Setup**: Add logging, metrics, and alerting
6. **Testing Enhancement**: Increase test coverage and add integration tests

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `pytest`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## 📞 Support

- **Issues**: Create an issue in the GitHub repository
- **Documentation**: Check `/docs` endpoint when running
- **Health Check**: Monitor `/api/v1/health/detailed` for system status

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.