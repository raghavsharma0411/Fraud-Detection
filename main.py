"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.core.config import settings
from src.api.routers import health, ml, genai, workers

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI application for ML/GenAI model endpoints",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(ml.router, prefix="/api/v1", tags=["Machine Learning"])
app.include_router(genai.router, prefix="/api/v1", tags=["Generative AI"])
app.include_router(workers.router, prefix="/api/v1", tags=["Workers"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    print(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    
    # Use localhost for display if HOST is 0.0.0.0 (not clickable)
    display_host = "localhost" if settings.HOST == "0.0.0.0" else settings.HOST
    base_url = f"http://{display_host}:{settings.PORT}"
    
    print()
    print("🚀 Application is ready!")
    print("=" * 60)
    print("📚 API Documentation:")
    print(f"   • Swagger UI:  {base_url}/docs")
    print(f"   • ReDoc:       {base_url}/redoc")
    print()
    print("❤️  Health Endpoints:")
    print(f"   • Basic:       {base_url}/api/v1/health")
    print(f"   • Detailed:    {base_url}/api/v1/health/detailed")
    print()
    print("🤖 ML Fraud Detection:")
    print(f"   • Single:      {base_url}/api/v1/ml/predict/transaction")
    print(f"   • Batch:       {base_url}/api/v1/ml/predict/transactions/batch")
    print(f"   • Models:      {base_url}/api/v1/ml/models")
    print(f"   • Risk Config: {base_url}/api/v1/ml/risk-config")
    print()
    print("👥 Workers API:")
    print(f"   • All Workers: {base_url}/api/v1/workers")
    print(f"   • Statistics:  {base_url}/api/v1/workers/stats/summary")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown."""
    print("Shutting down application")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )