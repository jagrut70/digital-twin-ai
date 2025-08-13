"""
Visualization Engine
Handles 3D visualization, avatar rendering, and visual state management
"""

import asyncio
import logging
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import numpy as np
from dataclasses import dataclass

from ..config import settings

logger = logging.getLogger(__name__)

@dataclass
class VisualState:
    """Visual state of a digital twin"""
    avatar_id: str
    position: Tuple[float, float, float]
    rotation: Tuple[float, float, float, float]  # quaternion
    scale: Tuple[float, float, float]
    animation_state: str
    facial_expression: Dict[str, float]
    body_pose: Dict[str, float]
    clothing: Dict[str, str]
    accessories: List[str]
    lighting: Dict[str, float]
    last_update: datetime

@dataclass
class AvatarConfig:
    """Avatar configuration"""
    avatar_id: str
    model_path: str
    texture_path: str
    skeleton_path: str
    height: float
    body_type: str
    skin_tone: str
    hair_style: str
    eye_color: str

class VisualizationEngine:
    """Manages 3D visualization and avatar rendering"""
    
    def __init__(self):
        self.avatars: Dict[str, AvatarConfig] = {}
        self.visual_states: Dict[str, VisualState] = {}
        self.scene_objects: Dict[str, Dict[str, Any]] = {}
        self.renderer_config: Dict[str, Any] = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the visualization engine"""
        try:
            # Load avatar configurations
            await self._load_avatar_configs()
            
            # Initialize renderer
            await self._initialize_renderer()
            
            # Setup scene management
            await self._setup_scene_management()
            
            self.is_initialized = True
            logger.info("Visualization Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Visualization Engine: {e}")
            raise
    
    async def _load_avatar_configs(self):
        """Load predefined avatar configurations"""
        # Default avatar configurations
        self.avatars = {
            "default_male": AvatarConfig(
                avatar_id="default_male",
                model_path=f"{settings.UNITY_BUILD_PATH}/avatars/male_base.fbx",
                texture_path=f"{settings.UNITY_BUILD_PATH}/avatars/male_texture.png",
                skeleton_path=f"{settings.UNITY_BUILD_PATH}/avatars/male_skeleton.json",
                height=1.75,
                body_type="athletic",
                skin_tone="medium",
                hair_style="short",
                eye_color="brown"
            ),
            "default_female": AvatarConfig(
                avatar_id="default_female",
                model_path=f"{settings.UNITY_BUILD_PATH}/avatars/female_base.fbx",
                texture_path=f"{settings.UNITY_BUILD_PATH}/avatars/female_texture.png",
                skeleton_path=f"{settings.UNITY_BUILD_PATH}/avatars/female_skeleton.json",
                height=1.65,
                body_type="slim",
                skin_tone="medium",
                hair_style="long",
                eye_color="blue"
            )
        }
        
        # Load custom avatar configurations if they exist
        custom_avatar_path = f"{settings.UNITY_BUILD_PATH}/avatars/custom"
        if os.path.exists(custom_avatar_path):
            await self._load_custom_avatars(custom_avatar_path)
    
    async def _load_custom_avatars(self, custom_path: str):
        """Load custom avatar configurations from directory"""
        try:
            for item in os.listdir(custom_path):
                config_file = os.path.join(custom_path, item, "config.json")
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                        avatar_id = f"custom_{item}"
                        self.avatars[avatar_id] = AvatarConfig(**config_data)
                        logger.info(f"Loaded custom avatar: {avatar_id}")
        except Exception as e:
            logger.warning(f"Could not load custom avatars: {e}")
    
    async def _initialize_renderer(self):
        """Initialize the 3D renderer"""
        self.renderer_config = {
            "renderer_type": "opengl",
            "version": settings.OPENGL_VERSION,
            "shadows_enabled": True,
            "antialiasing": True,
            "max_fps": 60,
            "resolution": (1920, 1080),
            "background_color": (0.1, 0.1, 0.1, 1.0)
        }
        
        # Initialize OpenGL context if available
        try:
            import OpenGL.GL as gl
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glEnable(gl.GL_CULL_FACE)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            logger.info("OpenGL renderer initialized")
        except ImportError:
            logger.warning("OpenGL not available, using software renderer")
            self.renderer_config["renderer_type"] = "software"
    
    async def _setup_scene_management(self):
        """Setup scene management system"""
        self.scene_objects = {
            "lighting": {
                "ambient": {"intensity": 0.3, "color": (1.0, 1.0, 1.0)},
                "directional": {"intensity": 0.7, "color": (1.0, 0.95, 0.8), "direction": (0.5, 1.0, 0.5)},
                "point_lights": []
            },
            "environment": {
                "skybox": "default_skybox",
                "fog_enabled": False,
                "fog_density": 0.01,
                "fog_color": (0.5, 0.5, 0.5)
            },
            "physics": {
                "gravity": (0.0, -9.81, 0.0),
                "collision_detection": True,
                "physics_timestep": 1.0 / 60.0
            }
        }
    
    async def create_avatar(self, twin_id: str, avatar_config: Dict[str, Any]) -> str:
        """Create a new avatar for a digital twin"""
        try:
            # Generate avatar ID
            avatar_id = f"avatar_{twin_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create avatar configuration
            avatar = AvatarConfig(
                avatar_id=avatar_id,
                model_path=avatar_config.get("model_path", self.avatars["default_male"].model_path),
                texture_path=avatar_config.get("texture_path", self.avatars["default_male"].texture_path),
                skeleton_path=avatar_config.get("skeleton_path", self.avatars["default_male"].skeleton_path),
                height=avatar_config.get("height", 1.75),
                body_type=avatar_config.get("body_type", "athletic"),
                skin_tone=avatar_config.get("skin_tone", "medium"),
                hair_style=avatar_config.get("hair_style", "short"),
                eye_color=avatar_config.get("eye_color", "brown")
            )
            
            # Store avatar configuration
            self.avatars[avatar_id] = avatar
            
            # Initialize visual state
            initial_state = VisualState(
                avatar_id=avatar_id,
                position=(0.0, 0.0, 0.0),
                rotation=(0.0, 0.0, 0.0, 1.0),
                scale=(1.0, 1.0, 1.0),
                animation_state="idle",
                facial_expression={"neutral": 1.0, "happy": 0.0, "sad": 0.0, "angry": 0.0},
                body_pose={"standing": 1.0, "sitting": 0.0, "walking": 0.0},
                clothing={"shirt": "default", "pants": "default", "shoes": "default"},
                accessories=[],
                lighting={"intensity": 1.0, "color": (1.0, 1.0, 1.0)},
                last_update=datetime.now()
            )
            
            self.visual_states[avatar_id] = initial_state
            logger.info(f"Created avatar: {avatar_id}")
            
            return avatar_id
            
        except Exception as e:
            logger.error(f"Failed to create avatar: {e}")
            raise
    
    async def update_visual_state(self, avatar_id: str, updates: Dict[str, Any]) -> bool:
        """Update the visual state of an avatar"""
        if avatar_id not in self.visual_states:
            return False
        
        try:
            current_state = self.visual_states[avatar_id]
            
            # Update position
            if "position" in updates:
                current_state.position = tuple(updates["position"])
            
            # Update rotation
            if "rotation" in updates:
                current_state.rotation = tuple(updates["rotation"])
            
            # Update scale
            if "scale" in updates:
                current_state.scale = tuple(updates["scale"])
            
            # Update animation state
            if "animation_state" in updates:
                current_state.animation_state = updates["animation_state"]
            
            # Update facial expression
            if "facial_expression" in updates:
                current_state.facial_expression.update(updates["facial_expression"])
            
            # Update body pose
            if "body_pose" in updates:
                current_state.body_pose.update(updates["body_pose"])
            
            # Update clothing
            if "clothing" in updates:
                current_state.clothing.update(updates["clothing"])
            
            # Update accessories
            if "accessories" in updates:
                current_state.accessories = updates["accessories"]
            
            # Update lighting
            if "lighting" in updates:
                current_state.lighting.update(updates["lighting"])
            
            current_state.last_update = datetime.now()
            
            logger.debug(f"Updated visual state for avatar: {avatar_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update visual state for avatar {avatar_id}: {e}")
            return False
    
    async def get_visual_state(self, avatar_id: str) -> Optional[VisualState]:
        """Get the current visual state of an avatar"""
        return self.visual_states.get(avatar_id)
    
    async def render_frame(self, avatar_ids: List[str] = None) -> Dict[str, Any]:
        """Render a frame with the specified avatars"""
        try:
            if avatar_ids is None:
                avatar_ids = list(self.visual_states.keys())
            
            frame_data = {
                "timestamp": datetime.now().isoformat(),
                "avatars": {},
                "scene": self.scene_objects,
                "renderer": self.renderer_config
            }
            
            for avatar_id in avatar_ids:
                if avatar_id in self.visual_states:
                    state = self.visual_states[avatar_id]
                    avatar_config = self.avatars.get(avatar_id)
                    
                    frame_data["avatars"][avatar_id] = {
                        "state": {
                            "position": state.position,
                            "rotation": state.rotation,
                            "scale": state.scale,
                            "animation_state": state.animation_state,
                            "facial_expression": state.facial_expression,
                            "body_pose": state.body_pose,
                            "clothing": state.clothing,
                            "accessories": state.accessories
                        },
                        "config": {
                            "model_path": avatar_config.model_path if avatar_config else None,
                            "texture_path": avatar_config.texture_path if avatar_config else None,
                            "height": avatar_config.height if avatar_config else None
                        } if avatar_config else None
                    }
            
            return frame_data
            
        except Exception as e:
            logger.error(f"Failed to render frame: {e}")
            return {"error": str(e)}
    
    async def apply_animation(self, avatar_id: str, animation_name: str, duration: float = 1.0) -> bool:
        """Apply an animation to an avatar"""
        try:
            if avatar_id not in self.visual_states:
                return False
            
            # Update animation state
            await self.update_visual_state(avatar_id, {
                "animation_state": animation_name
            })
            
            # Schedule animation completion
            asyncio.create_task(self._complete_animation(avatar_id, duration))
            
            logger.info(f"Applied animation '{animation_name}' to avatar {avatar_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply animation to avatar {avatar_id}: {e}")
            return False
    
    async def _complete_animation(self, avatar_id: str, duration: float):
        """Complete an animation after the specified duration"""
        await asyncio.sleep(duration)
        
        # Reset to idle state
        await self.update_visual_state(avatar_id, {
            "animation_state": "idle"
        })
    
    async def export_scene(self, file_path: str, format: str = "gltf") -> bool:
        """Export the current scene to a file"""
        try:
            scene_data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "format": format,
                    "version": "1.0"
                },
                "avatars": self.visual_states,
                "scene": self.scene_objects,
                "renderer": self.renderer_config
            }
            
            with open(file_path, 'w') as f:
                json.dump(scene_data, f, indent=2, default=str)
            
            logger.info(f"Exported scene to: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export scene: {e}")
            return False
    
    async def shutdown(self):
        """Shutdown the visualization engine"""
        logger.info("Shutting down Visualization Engine...")
        
        # Clear all states
        self.visual_states.clear()
        self.avatars.clear()
        self.scene_objects.clear()
        
        self.is_initialized = False
        logger.info("Visualization Engine shutdown complete")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the visualization engine status"""
        return {
            "initialized": self.is_initialized,
            "active_avatars": len(self.visual_states),
            "available_avatars": len(self.avatars),
            "renderer_type": self.renderer_config.get("renderer_type", "unknown"),
            "scene_objects": len(self.scene_objects)
        }
