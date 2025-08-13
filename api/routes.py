"""
API Routes for Digital Twin System
"""

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, status
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import timedelta

from core.digital_twin_engine import DigitalTwinEngine
from core.models.digital_twin import DigitalTwin
from core.auth import auth_manager, get_current_user, get_current_active_user, create_user_account
from core.models.database import User
from core.shared import get_engine as get_shared_engine

logger = logging.getLogger(__name__)

# Create API router
api_router = APIRouter()

# Authentication Endpoints
@api_router.post("/auth/register", response_model=Dict[str, str])
async def register_user(
    username: str,
    email: str,
    password: str,
    full_name: Optional[str] = None
):
    """Register a new user account"""
    try:
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name
        }
        
        user = await create_user_account(user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        
        return {"message": "User registered successfully", "user_id": user.id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to register user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )

@api_router.post("/auth/login", response_model=Dict[str, Any])
async def login_user(username: str, password: str):
    """Authenticate user and return access token"""
    try:
        # Authenticate user
        user = await auth_manager.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=auth_manager.access_token_expire_minutes)
        access_token = auth_manager.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Create session
        session_token = auth_manager.generate_session_token()
        await auth_manager.create_user_session(user.id, session_token)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "session_token": session_token,
            "expires_in": auth_manager.access_token_expire_minutes * 60,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to login user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to authenticate user"
        )

@api_router.post("/auth/logout", response_model=Dict[str, str])
async def logout_user(
    session_token: str,
    current_user: User = Depends(get_current_active_user)
):
    """Logout user and revoke session"""
    try:
        success = await auth_manager.revoke_session(session_token)
        if success:
            return {"message": "Logged out successfully"}
        else:
            return {"message": "Session not found or already expired"}
            
    except Exception as e:
        logger.error(f"Failed to logout user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout user"
        )

@api_router.get("/auth/me", response_model=Dict[str, Any])
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "created_at": current_user.created_at.isoformat(),
        "updated_at": current_user.updated_at.isoformat()
    }

@api_router.post("/auth/change-password", response_model=Dict[str, str])
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user)
):
    """Change user password"""
    try:
        from core.auth import change_user_password
        
        success = await change_user_password(current_user.id, old_password, new_password)
        if success:
            return {"message": "Password changed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to change password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )

def get_engine() -> DigitalTwinEngine:
    """Dependency to get the digital twin engine"""
    engine = get_shared_engine()
    if engine is None:
        raise HTTPException(status_code=503, detail="Digital Twin Engine not initialized")
    return engine

# Digital Twin Management Endpoints
@api_router.post("/twins", response_model=Dict[str, str])
async def create_digital_twin(
    twin_config: Dict[str, Any],
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Create a new digital twin"""
    try:
        twin_id = await engine.create_twin(twin_config)
        return {"twin_id": twin_id, "message": "Digital twin created successfully"}
    except Exception as e:
        logger.error(f"Failed to create digital twin: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/twins", response_model=List[str])
async def list_digital_twins(engine: DigitalTwinEngine = Depends(get_engine)):
    """List all digital twin IDs"""
    try:
        return list(engine.twins.keys())
    except Exception as e:
        logger.error(f"Failed to list digital twins: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/twins/{twin_id}", response_model=Dict[str, Any])
async def get_digital_twin(
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Get digital twin details"""
    try:
        twin = await engine.get_twin(twin_id)
        if not twin:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        return twin.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get digital twin {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/twins/{twin_id}", response_model=Dict[str, str])
async def update_digital_twin(
    twin_id: str,
    updates: Dict[str, Any],
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Update a digital twin"""
    try:
        success = await engine.update_twin(twin_id, updates)
        if not success:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        return {"message": "Digital twin updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update digital twin {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/twins/{twin_id}", response_model=Dict[str, str])
async def delete_digital_twin(
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Delete a digital twin"""
    try:
        success = await engine.delete_twin(twin_id)
        if not success:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        return {"message": "Digital twin deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete digital twin {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Interaction Endpoints
@api_router.post("/twins/{twin_id}/interact", response_model=Dict[str, Any])
async def interact_with_twin(
    twin_id: str,
    interaction_data: Dict[str, Any],
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Interact with a digital twin"""
    try:
        response = await engine.process_interaction(twin_id, interaction_data)
        return response
    except Exception as e:
        logger.error(f"Failed to process interaction with twin {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# State Query Endpoints
@api_router.get("/twins/{twin_id}/state", response_model=Dict[str, Any])
async def get_twin_state(
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Get the current state of a digital twin"""
    try:
        state = await engine.get_twin_state(twin_id)
        if not state:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        return {
            "twin_id": state.twin_id,
            "last_update": state.last_update.isoformat(),
            "health_status": state.health_status,
            "personality_state": state.personality_state,
            "behavior_patterns": state.behavior_patterns,
            "conversation_history": state.conversation_history,
            "visual_state": state.visual_state
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get twin state for {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/twins/{twin_id}/health", response_model=Dict[str, Any])
async def get_twin_health(
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Get health status of a digital twin"""
    try:
        twin = await engine.get_twin(twin_id)
        if not twin:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        health_status = twin.get_health_status()
        return {
            "twin_id": twin_id,
            "health_status": health_status,
            "health_metrics": {
                "heart_rate": twin.health_metrics.heart_rate,
                "blood_pressure": f"{twin.health_metrics.blood_pressure_systolic}/{twin.health_metrics.blood_pressure_diastolic}",
                "temperature": twin.health_metrics.temperature,
                "oxygen_saturation": twin.health_metrics.oxygen_saturation,
                "stress_level": twin.health_metrics.stress_level,
                "energy_level": twin.health_metrics.energy_level
            },
            "last_update": twin.last_health_update.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get twin health for {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/twins/{twin_id}/personality", response_model=Dict[str, Any])
async def get_twin_personality(
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Get personality state of a digital twin"""
    try:
        twin = await engine.get_twin(twin_id)
        if not twin:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        personality_state = twin.get_personality_state()
        return {
            "twin_id": twin_id,
            "personality_state": personality_state,
            "last_update": twin.last_personality_update.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get twin personality for {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/twins/{twin_id}/behavior", response_model=Dict[str, Any])
async def get_twin_behavior(
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Get behavior patterns of a digital twin"""
    try:
        twin = await engine.get_twin(twin_id)
        if not twin:
            raise HTTPException(status_code=404, detail="Digital twin not found")
        
        behavior_patterns = twin.get_behavior_patterns()
        return {
            "twin_id": twin_id,
            "behavior_patterns": behavior_patterns,
            "current_activity": twin.current_activity,
            "current_mood": twin.current_mood,
            "energy_level": twin.energy_level,
            "last_update": twin.last_behavior_update.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get twin behavior for {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# System Management Endpoints
@api_router.get("/system/status", response_model=Dict[str, Any])
async def get_system_status(engine: DigitalTwinEngine = Depends(get_engine)):
    """Get overall system status"""
    try:
        return engine.get_system_status()
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/system/restart", response_model=Dict[str, str])
async def restart_system(engine: DigitalTwinEngine = Depends(get_engine)):
    """Restart the digital twin system"""
    try:
        # This would require proper shutdown/restart logic
        return {"message": "System restart initiated"}
    except Exception as e:
        logger.error(f"Failed to restart system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@api_router.websocket("/ws/{twin_id}")
async def websocket_twin_endpoint(
    websocket: WebSocket,
    twin_id: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """WebSocket endpoint for real-time twin communication"""
    await websocket.accept()
    
    try:
        # Verify twin exists
        twin = await engine.get_twin(twin_id)
        if not twin:
            await websocket.close(code=4004, reason="Twin not found")
            return
        
        logger.info(f"WebSocket connection established for twin: {twin_id}")
        
        while True:
            # Receive message
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process interaction
            response = await engine.process_interaction(twin_id, message)
            
            # Send response back
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for twin: {twin_id}")
    except Exception as e:
        logger.error(f"WebSocket error for twin {twin_id}: {e}")
        try:
            await websocket.close(code=1011, reason="Internal error")
        except:
            pass

# Synthetic Data Endpoints
@api_router.get("/synthetic/profiles/{profile_type}", response_model=List[Dict[str, Any]])
async def get_synthetic_profiles(
    profile_type: str,
    engine: DigitalTwinEngine = Depends(get_engine)
):
    """Get synthetic profiles of a specific type"""
    try:
        if not engine.synthetic_data_manager:
            raise HTTPException(status_code=503, detail="Synthetic data manager not available")
        
        # This would need to be implemented in the synthetic data manager
        return {"message": "Synthetic profiles endpoint not yet implemented"}
    except Exception as e:
        logger.error(f"Failed to get synthetic profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/synthetic/generate", response_model=Dict[str, str])
async def generate_synthetic_data(engine: DigitalTwinEngine = Depends(get_engine)):
    """Generate new synthetic data"""
    try:
        if not engine.synthetic_data_manager:
            raise HTTPException(status_code=503, detail="Synthetic data manager not available")
        
        await engine.synthetic_data_manager.generate_new_data()
        return {"message": "Synthetic data generation initiated"}
    except Exception as e:
        logger.error(f"Failed to generate synthetic data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
