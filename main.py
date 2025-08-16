#!/usr/bin/env python3
"""
Digital Twin System - Main Application
FastAPI-based backend with WebSocket support and comprehensive digital twin management
"""

import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Import core components
from core.digital_twin_engine import DigitalTwinEngine
from core.config import settings
from core.database import db_manager
from core.shared import set_engine
from api.routes import api_router
from ui.routes import ui_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/digital_twin.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global engine instance
engine: DigitalTwinEngine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global engine
    
    logger.info("🚀 Starting Digital Twin System...")
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        await db_manager.initialize()
        
        # Create and initialize the digital twin engine
        logger.info("Creating Digital Twin Engine...")
        engine = DigitalTwinEngine()
        
        # Set global engine reference
        set_engine(engine)
        
        # Initialize engine
        logger.info("Initializing Digital Twin Engine...")
        try:
            await engine.initialize()
            logger.info("✅ Digital Twin Engine initialized successfully")
        except Exception as e:
            if "OpenGL" in str(e) or "segmentation fault" in str(e):
                logger.warning("⚠️ OpenGL visualization disabled (common on headless systems)")
                logger.info("✅ Core Digital Twin functionality available")
            else:
                logger.error(f"Failed to initialize engine: {e}")
                raise
        
        # Create default demo twin if none exist
        if not engine.twins:
            logger.info("Creating default demo twin...")
            demo_config = {
                "name": "Demo Digital Twin",
                "description": "A demonstration digital twin with synthetic data",
                "twin_type": "human",
                "personality": {
                    "openness": 0.75,
                    "conscientiousness": 0.82,
                    "extraversion": 0.68,
                    "agreeableness": 0.71,
                    "neuroticism": 0.23
                },
                "metadata": {"demo": True, "created_at": datetime.now().isoformat()}
            }
            
            try:
                demo_id = await engine.create_twin(demo_config)
                logger.info(f"✅ Demo twin created: {demo_id}")
            except Exception as e:
                logger.warning(f"Could not create demo twin: {e}")
        
        logger.info("🎉 Digital Twin System started successfully")
        logger.info(f"📊 Active twins: {len(engine.twins) if engine.twins else 0}")
        logger.info(f"🌐 Web interface: http://localhost:{settings.PORT}")
        logger.info(f"📚 API documentation: http://localhost:{settings.PORT}/docs")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Failed to start Digital Twin System: {e}")
        raise
    finally:
        # Cleanup
        logger.info("🔄 Shutting down Digital Twin System...")
        if engine:
            try:
                await engine.shutdown()
                logger.info("✅ Digital Twin Engine shutdown complete")
            except Exception as e:
                logger.warning(f"Engine shutdown warning: {e}")
        
        try:
            await db_manager.close()
            logger.info("✅ Database connections closed")
        except Exception as e:
            logger.warning(f"Database shutdown warning: {e}")
        
        logger.info("👋 Digital Twin System shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="Digital Twin System",
    description="Advanced digital twin platform with synthetic data integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1", tags=["API"])

# Include UI routes
app.include_router(ui_router, prefix="/ui", tags=["UI"])

# Serve static files (CSS, JS, images)
app.mount("/styles", StaticFiles(directory="styles"), name="styles")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/assets", StaticFiles(directory="assets", html=True), name="assets")

# Root endpoint - serve the main dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    try:
        with open("index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dashboard not found"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health check"""
    global engine
    
    try:
        status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "database": "connected" if db_manager.is_connected() else "disconnected",
                "engine": "running" if engine and engine.running else "stopped",
                "active_twins": len(engine.twins) if engine and engine.twins else 0
            }
        }
        
        if engine:
            engine_status = engine.get_system_status()
            status["system"].update(engine_status)
        
        return status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# System information endpoint
@app.get("/system/info")
async def system_info():
    """Get system information"""
    global engine
    
    return {
        "system": "Digital Twin Platform",
        "version": "1.0.0",
        "python_version": sys.version,
        "engine_status": "running" if engine and engine.running else "stopped",
        "features": {
            "synthetic_data": True,
            "ai_personality": True,
            "health_monitoring": True,
            "behavior_simulation": True,
            "conversation_engine": True,
            "visualization": True,
            "websocket": True,
            "api": True
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return {"error": "Internal server error", "status_code": 500}

def main():
    """Main entry point"""
    try:
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Start the server
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info" if settings.DEBUG else "warning"
        )
        
    except KeyboardInterrupt:
        logger.info("👋 Application stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
