#!/usr/bin/env python3
"""
Digital Twin Main Application
Main entry point for the digital twin system
"""

import asyncio
import logging
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from core.digital_twin_engine import DigitalTwinEngine
from core.config import settings
from core.shared import set_engine, get_engine
from api.routes import api_router
from ui.routes import ui_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    
    # Startup
    logger.info("Starting Digital Twin System...")
    try:
        engine = DigitalTwinEngine()
        await engine.initialize()
        set_engine(engine)  # Share the engine instance
        logger.info("Digital Twin Engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Digital Twin Engine: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Digital Twin System...")
    engine = get_engine()
    if engine:
        await engine.shutdown()
    logger.info("Digital Twin System shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="Digital Twin System",
    description="A comprehensive digital twin system using synthetic data",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")
app.include_router(ui_router, prefix="/ui")

# Mount static files
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Digital Twin System",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "ui": "/ui"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from core.shared import get_engine
    engine = get_engine()
    return {
        "status": "healthy",
        "timestamp": asyncio.get_event_loop().time(),
        "engine_status": "running" if engine else "stopped"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    try:
        while True:
            # Handle real-time data streaming
            data = await websocket.receive_text()
            # Process incoming data
            response = {"message": f"Received: {data}", "timestamp": asyncio.get_event_loop().time()}
            await websocket.send_text(str(response))
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    logger.info("Starting Digital Twin System...")
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
