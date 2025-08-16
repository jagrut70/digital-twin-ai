"""
Visualization Engine
Handles 3D visualization, avatar rendering, and visual state management
Using Plotly for cross-platform compatibility
"""

import asyncio
import logging
import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import numpy as np
from dataclasses import dataclass, asdict

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    
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
        self.plotly_available = PLOTLY_AVAILABLE
        
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
        """Initialize the Plotly-based renderer"""
        if not PLOTLY_AVAILABLE:
            logger.error("Plotly not available. Cannot initialize visualization engine.")
            raise ImportError("Plotly is required for visualization but not installed.")
        
        self.renderer_config = {
            "renderer_type": settings.VISUALIZATION_ENGINE,
            "version": "web-based",
            "shadows_enabled": True,
            "antialiasing": True,
            "max_fps": 60,
            "resolution": (1920, 1080),
            "background_color": "rgb(26, 26, 26)",
            "theme": settings.PLOTLY_THEME,
            "export_path": settings.VISUALIZATION_EXPORT_PATH,
            "camera": {
                "eye": dict(x=1.5, y=1.5, z=1.5),
                "center": dict(x=0, y=0, z=0),
                "up": dict(x=0, y=0, z=1)
            }
        }
        
        # Set default Plotly configuration for web-based rendering
        # Use offline mode to avoid notebook dependencies
        logger.info("Plotly renderer initialized successfully")
    
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
    
    async def create_3d_avatar_visualization(self, avatar_id: str, include_data: bool = True) -> Optional[go.Figure]:
        """Create a 3D visualization of an avatar using Plotly"""
        if not PLOTLY_AVAILABLE or avatar_id not in self.visual_states:
            return None
        
        try:
            state = self.visual_states[avatar_id]
            avatar_config = self.avatars.get(avatar_id)
            
            # Create 3D scatter plot for avatar representation
            fig = go.Figure()
            
            # Avatar base (simplified as a cylinder/humanoid shape)
            avatar_height = avatar_config.height if avatar_config else 1.75
            x, y, z = state.position
            
            # Create simplified humanoid representation
            # Head
            head_x = [x - 0.1, x + 0.1, x + 0.1, x - 0.1, x - 0.1]
            head_y = [y - 0.1, y - 0.1, y + 0.1, y + 0.1, y - 0.1]
            head_z = [z + avatar_height - 0.2] * 5
            
            # Body
            body_x = [x - 0.2, x + 0.2, x + 0.2, x - 0.2, x - 0.2]
            body_y = [y - 0.1, y - 0.1, y + 0.1, y + 0.1, y - 0.1]
            body_z = [z + avatar_height - 0.4, z + avatar_height - 0.4, 
                     z + avatar_height - 0.8, z + avatar_height - 0.8, z + avatar_height - 0.4]
            
            # Add head
            fig.add_trace(go.Scatter3d(
                x=head_x, y=head_y, z=head_z,
                mode='lines+markers',
                name=f'Head - {avatar_id}',
                line=dict(color='lightblue', width=4),
                marker=dict(size=6, color='lightblue')
            ))
            
            # Add body
            fig.add_trace(go.Scatter3d(
                x=body_x, y=body_y, z=body_z,
                mode='lines+markers',
                name=f'Body - {avatar_id}',
                line=dict(color='blue', width=6),
                marker=dict(size=8, color='blue')
            ))
            
            # Add center point
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                name=f'Center - {avatar_id}',
                marker=dict(size=12, color='red', symbol='cross')
            ))
            
            # Configure layout
            fig.update_layout(
                scene=dict(
                    xaxis_title='X Position',
                    yaxis_title='Y Position',
                    zaxis_title='Z Position',
                    camera=self.renderer_config["camera"]
                ),
                title=f'Avatar Visualization: {avatar_id}',
                template=self.renderer_config["theme"]
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create 3D avatar visualization for {avatar_id}: {e}")
            return None
    
    async def create_scene_visualization(self, avatar_ids: List[str] = None) -> Optional[go.Figure]:
        """Create a 3D scene visualization with multiple avatars"""
        if not PLOTLY_AVAILABLE:
            return None
        
        try:
            if avatar_ids is None:
                avatar_ids = list(self.visual_states.keys())
            
            fig = go.Figure()
            
            # Add ground plane
            ground_size = 5
            ground_x = [-ground_size, ground_size, ground_size, -ground_size, -ground_size]
            ground_y = [-ground_size, -ground_size, ground_size, ground_size, -ground_size]
            ground_z = [0, 0, 0, 0, 0]
            
            fig.add_trace(go.Scatter3d(
                x=ground_x, y=ground_y, z=ground_z,
                mode='lines',
                name='Ground',
                line=dict(color='gray', width=2)
            ))
            
            # Add avatars to scene
            colors = px.colors.qualitative.Set1
            for i, avatar_id in enumerate(avatar_ids):
                if avatar_id in self.visual_states:
                    state = self.visual_states[avatar_id]
                    avatar_config = self.avatars.get(avatar_id)
                    color = colors[i % len(colors)]
                    
                    x, y, z = state.position
                    height = avatar_config.height if avatar_config else 1.75
                    
                    # Simple avatar representation as a vertical line with marker
                    fig.add_trace(go.Scatter3d(
                        x=[x, x], y=[y, y], z=[z, z + height],
                        mode='lines+markers',
                        name=avatar_id,
                        line=dict(color=color, width=8),
                        marker=dict(size=[6, 12], color=color)
                    ))
                    
                    # Add animation state annotation
                    if state.animation_state != 'idle':
                        fig.add_trace(go.Scatter3d(
                            x=[x], y=[y], z=[z + height + 0.3],
                            mode='text',
                            name=f'{avatar_id}_state',
                            text=[state.animation_state],
                            textfont=dict(color=color, size=12)
                        ))
            
            # Configure layout
            fig.update_layout(
                scene=dict(
                    xaxis_title='X Position',
                    yaxis_title='Y Position',
                    zaxis_title='Z Position',
                    aspectmode='cube',
                    camera=self.renderer_config["camera"]
                ),
                title='Digital Twin Scene Visualization',
                template=self.renderer_config["theme"],
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create scene visualization: {e}")
            return None
    
    async def create_data_dashboard(self, avatar_id: str) -> Optional[go.Figure]:
        """Create a data dashboard for an avatar"""
        if not PLOTLY_AVAILABLE or avatar_id not in self.visual_states:
            return None
        
        try:
            state = self.visual_states[avatar_id]
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Facial Expression', 'Body Pose', 'Position', 'Animation State'),
                specs=[[{'type': 'bar'}, {'type': 'bar'}],
                       [{'type': 'scatter3d'}, {'type': 'indicator'}]]
            )
            
            # Facial expression bar chart
            expressions = list(state.facial_expression.keys())
            expression_values = list(state.facial_expression.values())
            
            fig.add_trace(
                go.Bar(x=expressions, y=expression_values, name='Facial Expression'),
                row=1, col=1
            )
            
            # Body pose bar chart
            poses = list(state.body_pose.keys())
            pose_values = list(state.body_pose.values())
            
            fig.add_trace(
                go.Bar(x=poses, y=pose_values, name='Body Pose'),
                row=1, col=2
            )
            
            # 3D position
            x, y, z = state.position
            fig.add_trace(
                go.Scatter3d(
                    x=[x], y=[y], z=[z],
                    mode='markers',
                    marker=dict(size=15, color='red'),
                    name='Position'
                ),
                row=2, col=1
            )
            
            # Animation state indicator
            fig.add_trace(
                go.Indicator(
                    mode='gauge+number',
                    value=1 if state.animation_state != 'idle' else 0,
                    title={'text': f'Animation: {state.animation_state}'},
                    gauge={'axis': {'range': [None, 1]},
                          'bar': {'color': 'darkblue'},
                          'bgcolor': 'white',
                          'borderwidth': 2,
                          'bordercolor': 'gray'}
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'Avatar Dashboard: {avatar_id}',
                template=self.renderer_config["theme"],
                height=800
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create data dashboard for {avatar_id}: {e}")
            return None
    
    async def save_visualization(self, figure: go.Figure, file_path: str, format: str = 'html') -> bool:
        """Save a Plotly visualization to file"""
        try:
            if format.lower() == 'html':
                pyo.plot(figure, filename=file_path, auto_open=False)
            elif format.lower() == 'png':
                figure.write_image(file_path)
            elif format.lower() == 'pdf':
                figure.write_image(file_path)
            elif format.lower() == 'json':
                with open(file_path, 'w') as f:
                    json.dump(figure.to_dict(), f, indent=2)
            else:
                logger.error(f"Unsupported format: {format}")
                return False
            
            logger.info(f"Saved visualization to: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save visualization: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the visualization engine status"""
        return {
            "initialized": self.is_initialized,
            "active_avatars": len(self.visual_states),
            "available_avatars": len(self.avatars),
            "renderer_type": self.renderer_config.get("renderer_type", "unknown"),
            "scene_objects": len(self.scene_objects),
            "plotly_available": PLOTLY_AVAILABLE
        }
    
    # Synchronous wrapper methods for testing and simple usage
    def initialize(self):
        """Synchronous initialize method"""
        if not PLOTLY_AVAILABLE:
            logger.error("Plotly not available. Cannot initialize visualization engine.")
            return False
        
        try:
            # Simple synchronous initialization
            self.renderer_config = {
                "renderer_type": getattr(settings, 'VISUALIZATION_ENGINE', 'plotly'),
                "version": "web-based", 
                "theme": getattr(settings, 'PLOTLY_THEME', 'plotly_dark'),
                "export_path": getattr(settings, 'VISUALIZATION_EXPORT_PATH', './exports'),
                "camera": {
                    "eye": dict(x=1.5, y=1.5, z=1.5),
                    "center": dict(x=0, y=0, z=0),
                    "up": dict(x=0, y=0, z=1)
                }
            }
            
            # Create export directory
            os.makedirs(self.renderer_config["export_path"], exist_ok=True)
            
            self.is_initialized = True
            logger.info("Visualization Engine initialized successfully (sync)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Visualization Engine (sync): {e}")
            return False
    
    def create_3d_avatar_visualization(self, avatar_data: Dict[str, Any]) -> Optional[go.Figure]:
        """Create a 3D avatar visualization from data dict"""
        if not PLOTLY_AVAILABLE:
            return None
            
        try:
            # Extract data
            position = avatar_data.get('position', [0, 0, 0])
            personality = avatar_data.get('personality', {})
            health = avatar_data.get('health', {})
            emotional_state = avatar_data.get('emotional_state', 'neutral')
            
            fig = go.Figure()
            
            x, y, z = position
            avatar_height = 1.75
            
            # Create simplified humanoid representation
            # Head (sphere-like)
            head_trace = go.Scatter3d(
                x=[x], y=[y], z=[z + avatar_height - 0.1],
                mode='markers',
                name='Head',
                marker=dict(
                    size=15,
                    color='lightblue',
                    symbol='circle',
                    line=dict(color='blue', width=2)
                )
            )
            fig.add_trace(head_trace)
            
            # Body (cylinder-like)
            body_trace = go.Scatter3d(
                x=[x, x], 
                y=[y, y], 
                z=[z, z + avatar_height - 0.3],
                mode='lines+markers',
                name='Body',
                line=dict(color='blue', width=8),
                marker=dict(size=[8, 12], color='blue')
            )
            fig.add_trace(body_trace)
            
            # Add personality visualization as colored points around avatar
            if personality:
                for i, (trait, value) in enumerate(personality.items()):
                    angle = (i / len(personality)) * 2 * np.pi
                    px = x + 0.5 * np.cos(angle) * value
                    py = y + 0.5 * np.sin(angle) * value
                    pz = z + avatar_height/2
                    
                    fig.add_trace(go.Scatter3d(
                        x=[px], y=[py], z=[pz],
                        mode='markers+text',
                        name=f'{trait.title()}',
                        text=[trait[:3].upper()],
                        textposition='middle center',
                        marker=dict(
                            size=10 + value * 10,
                            color=value,
                            colorscale='Viridis',
                            opacity=0.7
                        )
                    ))
            
            # Add health indicators
            if health:
                health_y_offset = 0
                for metric, value in health.items():
                    if isinstance(value, (int, float)):
                        normalized_value = min(value / 100, 1.0) if value > 1 else value
                        fig.add_trace(go.Scatter3d(
                            x=[x + 0.3], y=[y + health_y_offset], z=[z + avatar_height/4],
                            mode='markers+text',
                            name=f'Health: {metric}',
                            text=[f'{metric[:3]}: {value}'],
                            marker=dict(
                                size=8 + normalized_value * 8,
                                color='red' if normalized_value < 0.3 else 'yellow' if normalized_value < 0.7 else 'green',
                                opacity=0.8
                            )
                        ))
                        health_y_offset += 0.1
            
            # Configure layout
            fig.update_layout(
                scene=dict(
                    xaxis_title='X Position',
                    yaxis_title='Y Position', 
                    zaxis_title='Z Position',
                    camera=self.renderer_config.get("camera", {}),
                    aspectmode='cube'
                ),
                title=f'3D Avatar Visualization ({emotional_state})',
                template=self.renderer_config.get("theme", 'plotly_dark'),
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create 3D avatar visualization: {e}")
            return None
    
    def create_3d_scene_visualization(self, scene_data: Dict[str, Any]) -> Optional[go.Figure]:
        """Create a 3D scene visualization with avatars and environment"""
        if not PLOTLY_AVAILABLE:
            return None
            
        try:
            fig = go.Figure()
            
            # Add ground plane
            ground_size = 5
            ground_x = [-ground_size, ground_size, ground_size, -ground_size, -ground_size]
            ground_y = [-ground_size, -ground_size, ground_size, ground_size, -ground_size]
            ground_z = [0, 0, 0, 0, 0]
            
            fig.add_trace(go.Scatter3d(
                x=ground_x, y=ground_y, z=ground_z,
                mode='lines',
                name='Ground',
                line=dict(color='gray', width=3)
            ))
            
            # Add avatars
            avatars = scene_data.get('avatars', [])
            colors = px.colors.qualitative.Set1
            
            for i, avatar_data in enumerate(avatars):
                position = avatar_data.get('position', [i, 0, 0])
                x, y, z = position
                color = colors[i % len(colors)]
                
                # Avatar representation
                fig.add_trace(go.Scatter3d(
                    x=[x, x], y=[y, y], z=[z, z + 1.75],
                    mode='lines+markers',
                    name=f'Avatar {i+1}',
                    line=dict(color=color, width=6),
                    marker=dict(size=[8, 12], color=color)
                ))
                
                # Add avatar head
                fig.add_trace(go.Scatter3d(
                    x=[x], y=[y], z=[z + 1.65],
                    mode='markers',
                    name=f'Avatar {i+1} Head',
                    marker=dict(size=12, color=color, symbol='circle')
                ))
            
            # Add environment elements
            environment = scene_data.get('environment', {})
            env_type = environment.get('type', 'outdoor')
            
            # Configure layout based on environment
            if env_type == 'indoor':
                # Add room boundaries
                room_size = 3
                room_height = 3
                # Floor outline
                fig.add_trace(go.Scatter3d(
                    x=[-room_size, room_size, room_size, -room_size, -room_size],
                    y=[-room_size, -room_size, room_size, room_size, -room_size],
                    z=[0, 0, 0, 0, 0],
                    mode='lines',
                    name='Room Floor',
                    line=dict(color='brown', width=4)
                ))
                # Ceiling outline
                fig.add_trace(go.Scatter3d(
                    x=[-room_size, room_size, room_size, -room_size, -room_size],
                    y=[-room_size, -room_size, room_size, room_size, -room_size],
                    z=[room_height, room_height, room_height, room_height, room_height],
                    mode='lines',
                    name='Room Ceiling',
                    line=dict(color='white', width=2)
                ))
            
            fig.update_layout(
                scene=dict(
                    xaxis_title='X Position',
                    yaxis_title='Y Position',
                    zaxis_title='Z Position',
                    camera=self.renderer_config.get("camera", {}),
                    aspectmode='cube'
                ),
                title=f'3D Scene Visualization ({env_type})',
                template=self.renderer_config.get("theme", 'plotly_dark'),
                height=700
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create 3D scene visualization: {e}")
            return None
    
    def visualize_avatar(self, twin_id: str, data: Dict[str, Any]) -> Optional[go.Figure]:
        """Create basic avatar visualization"""
        # Create avatar data structure from input
        avatar_data = {
            'position': [0, 0, 0],
            'personality': data.get('personality', {}),
            'health': data,  # Use all data as health data
            'emotional_state': 'active'
        }
        
        return self.create_3d_avatar_visualization(avatar_data)
    
    def visualize_scene(self, behavior_patterns: List[Dict[str, Any]]) -> Optional[go.Figure]:
        """Create scene visualization from behavior patterns"""
        if not PLOTLY_AVAILABLE or not behavior_patterns:
            return None
            
        try:
            fig = go.Figure()
            
            # Create timeline of behavior patterns
            times = []
            activities = []
            outcomes = []
            engagements = []
            
            for i, pattern in enumerate(behavior_patterns):
                timestamp = pattern.get('timestamp', datetime.now())
                if hasattr(timestamp, 'timestamp'):
                    times.append(timestamp.timestamp())
                else:
                    times.append(i)
                
                activities.append(pattern.get('activity_type', 'unknown'))
                outcomes.append(pattern.get('outcome', 'neutral'))
                engagements.append(pattern.get('engagement_level', 0.5))
            
            # Create 3D behavior visualization
            fig.add_trace(go.Scatter3d(
                x=times,
                y=[i for i in range(len(behavior_patterns))],
                z=engagements,
                mode='markers+lines+text',
                text=activities,
                textposition='top center',
                name='Behavior Patterns',
                marker=dict(
                    size=10,
                    color=engagements,
                    colorscale='Viridis',
                    colorbar=dict(title='Engagement Level')
                ),
                line=dict(color='blue', width=3)
            ))
            
            fig.update_layout(
                scene=dict(
                    xaxis_title='Timeline',
                    yaxis_title='Pattern Sequence',
                    zaxis_title='Engagement Level',
                    camera=self.renderer_config.get("camera", {})
                ),
                title='Behavior Patterns Visualization',
                template=self.renderer_config.get("theme", 'plotly_dark'),
                height=600
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create behavior scene visualization: {e}")
            return None
    
    def save_figure(self, figure: go.Figure, file_path: str, format: str = 'html') -> bool:
        """Save a Plotly figure to file (synchronous)"""
        try:
            if format.lower() == 'html':
                pyo.plot(figure, filename=file_path, auto_open=False)
            elif format.lower() == 'png':
                figure.write_image(file_path)
            elif format.lower() == 'pdf':
                figure.write_image(file_path)
            elif format.lower() == 'json':
                with open(file_path, 'w') as f:
                    json.dump(figure.to_dict(), f, indent=2)
            else:
                logger.error(f"Unsupported format: {format}")
                return False
            
            logger.info(f"Saved figure to: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save figure: {e}")
            return False
    
    def shutdown(self):
        """Synchronous shutdown method"""
        logger.info("Shutting down Visualization Engine (sync)...")
        
        # Clear all states
        self.visual_states.clear()
        self.avatars.clear()
        self.scene_objects.clear()
        
        self.is_initialized = False
        logger.info("Visualization Engine shutdown complete (sync)")
