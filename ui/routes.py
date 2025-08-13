"""
UI Routes for Digital Twin System Web Interface
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Create UI router
ui_router = APIRouter()

# Templates directory
templates = Jinja2Templates(directory="ui/templates")

@ui_router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    try:
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "title": "Digital Twin Dashboard",
                "page": "dashboard"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render dashboard: {e}")
        raise HTTPException(status_code=500, detail="Failed to render dashboard")

@ui_router.get("/twins", response_class=HTMLResponse)
async def twins_page(request: Request):
    """Digital twins management page"""
    try:
        return templates.TemplateResponse(
            "twins.html",
            {
                "request": request,
                "title": "Digital Twins",
                "page": "twins"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render twins page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render twins page")

@ui_router.get("/twins/{twin_id}", response_class=HTMLResponse)
async def twin_detail_page(request: Request, twin_id: str):
    """Individual twin detail page"""
    try:
        return templates.TemplateResponse(
            "twin_detail.html",
            {
                "request": request,
                "title": f"Twin {twin_id}",
                "page": "twin_detail",
                "twin_id": twin_id
            }
        )
    except Exception as e:
        logger.error(f"Failed to render twin detail page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render twin detail page")

@ui_router.get("/health", response_class=HTMLResponse)
async def health_page(request: Request):
    """Health monitoring page"""
    try:
        return templates.TemplateResponse(
            "health.html",
            {
                "request": request,
                "title": "Health Monitoring",
                "page": "health"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render health page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render health page")

@ui_router.get("/personality", response_class=HTMLResponse)
async def personality_page(request: Request):
    """Personality analysis page"""
    try:
        return templates.TemplateResponse(
            "personality.html",
            {
                "request": request,
                "title": "Personality Analysis",
                "page": "personality"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render personality page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render personality page")

@ui_router.get("/behavior", response_class=HTMLResponse)
async def behavior_page(request: Request):
    """Behavior simulation page"""
    try:
        return templates.TemplateResponse(
            "behavior.html",
            {
                "request": request,
                "title": "Behavior Simulation",
                "page": "behavior"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render behavior page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render behavior page")

@ui_router.get("/visualization", response_class=HTMLResponse)
async def visualization_page(request: Request):
    """3D visualization page"""
    try:
        return templates.TemplateResponse(
            "visualization.html",
            {
                "request": request,
                "title": "3D Visualization",
                "page": "visualization"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render visualization page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render visualization page")

@ui_router.get("/synthetic", response_class=HTMLResponse)
async def synthetic_data_page(request: Request):
    """Synthetic data management page"""
    try:
        return templates.TemplateResponse(
            "synthetic.html",
            {
                "request": request,
                "title": "Synthetic Data",
                "page": "synthetic"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render synthetic data page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render synthetic data page")

@ui_router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """System settings page"""
    try:
        return templates.TemplateResponse(
            "settings.html",
            {
                "request": request,
                "title": "Settings",
                "page": "settings"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render settings page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render settings page")

@ui_router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page"""
    try:
        return templates.TemplateResponse(
            "about.html",
            {
                "request": request,
                "title": "About",
                "page": "about"
            }
        )
    except Exception as e:
        logger.error(f"Failed to render about page: {e}")
        raise HTTPException(status_code=500, detail="Failed to render about page")
