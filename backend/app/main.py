from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import structlog

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="BevScan API",
    description="Smart Invoice Parser for Beverage Teams",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting BevScan API server")
    logger.info(f"Environment: {settings.LLM_PROVIDER} LLM provider")
    logger.info(f"Database: {settings.DATABASE_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down BevScan API server")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "BevScan API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_provider": settings.LLM_PROVIDER,
        "database": "connected"  # TODO: Add actual DB check
    }

# Include API routes
from app.api.routes.invoice import router as invoice_router
from app.api.routes.alerts import router as alerts_router
app.include_router(invoice_router)
app.include_router(alerts_router)
# app.include_router(upload.router, prefix="/api/v1")
# app.include_router(parse.router, prefix="/api/v1")
# app.include_router(dashboard.router, prefix="/api/v1")
# app.include_router(alerts.router, prefix="/api/v1")
# app.include_router(export.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    ) 