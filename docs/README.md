# 📚 Documentation

Welcome to the CollectProcessor AI documentation directory.

## Available Documentation

### API Documentation
- **[ML Fraud Detection API](ML_FRAUD_DETECTION_API.md)** - Complete guide to fraud detection endpoints
  - Single transaction prediction
  - Batch transaction processing
  - Model management
  - Examples in cURL, Python, JavaScript

### Quick Links
- **[Main Project README](../README.md)** - Project setup and overview
- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when running)
- **[Alternative Docs](http://localhost:8000/redoc)** - ReDoc interface (when running)

## Documentation Structure

```
docs/
├── README.md                     # This file - documentation index
├── ML_FRAUD_DETECTION_API.md     # ML fraud detection endpoints
└── [future documentation files]
```

## Getting Started

1. **Start the Application**
   ```bash
   python main.py
   # OR
   docker-compose up
   ```

2. **View Interactive Docs**
   - Open http://localhost:8000/docs in your browser
   - Try out the endpoints directly in the interface

3. **Read Detailed Guides**
   - For ML endpoints: [ML_FRAUD_DETECTION_API.md](ML_FRAUD_DETECTION_API.md)
   - For general setup: [../README.md](../README.md)

---

*Keep documentation up to date as the API evolves!*