"""
Core Digital Twin Engine
Manages the main digital twin functionality and coordination
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

from .config import settings
from .models.digital_twin import DigitalTwin
from .models.personality import PersonalityModel
from .models.health_monitor import HealthMonitor
from .models.behavior_simulator import BehaviorSimulator
from .models.conversation_engine import ConversationEngine
# Visualization engine temporarily disabled due to OpenGL compatibility issues on macOS
# from .models.visualization_engine import VisualizationEngine
VISUALIZATION_AVAILABLE = False
VisualizationEngine = None
from .data.synthetic_data_manager import SyntheticDataManager
from .database import db_manager
from .auth import auth_manager

logger = logging.getLogger(__name__)

@dataclass
class TwinState:
    """Digital twin state information"""
    twin_id: str
    last_update: datetime
    health_status: str
    personality_state: Dict[str, Any]
    behavior_patterns: List[str]
    conversation_history: List[Dict[str, Any]]
    visual_state: Dict[str, Any]

class DigitalTwinEngine:
    """Main digital twin engine that coordinates all components"""
    
    def __init__(self):
        self.twins: Dict[str, DigitalTwin] = {}
        self.synthetic_data_manager: Optional[SyntheticDataManager] = None
        self.personality_model: Optional[PersonalityModel] = None
        self.health_monitor: Optional[HealthMonitor] = None
        self.behavior_simulator: Optional[BehaviorSimulator] = None
        self.conversation_engine: Optional[ConversationEngine] = None
        self.visualization_engine: Optional[VisualizationEngine] = None
        
        # Background tasks
        self.background_tasks: List[asyncio.Task] = []
        self.running = False
        
    async def initialize(self):
        """Initialize the digital twin engine"""
        logger.info("Initializing Digital Twin Engine...")
        
        try:
            # Initialize database manager
            await db_manager.initialize()
            logger.info("Database manager initialized")
            
            # Initialize synthetic data manager
            self.synthetic_data_manager = SyntheticDataManager()
            await self.synthetic_data_manager.initialize()
            
            # Initialize AI/ML models
            self.personality_model = PersonalityModel()
            await self.personality_model.initialize()
            
            self.health_monitor = HealthMonitor()
            await self.health_monitor.initialize()
            
            self.behavior_simulator = BehaviorSimulator()
            await self.behavior_simulator.initialize()
            
            # Initialize conversation engine
            self.conversation_engine = ConversationEngine()
            await self.conversation_engine.initialize()
            
            # Initialize visualization engine (optional - may fail on macOS)
            if VISUALIZATION_AVAILABLE and VisualizationEngine is not None:
                try:
                    self.visualization_engine = VisualizationEngine()
                    await self.visualization_engine.initialize()
                    logger.info("Visualization engine initialized successfully")
                except Exception as e:
                    logger.warning(f"Visualization engine initialization failed: {e}")
                    logger.info("Continuing without visualization engine (this is normal on macOS)")
                    self.visualization_engine = None
            else:
                logger.info("Visualization engine not available - continuing without it")
                self.visualization_engine = None
            
            # Start background tasks
            await self._start_background_tasks()
            
            self.running = True
            logger.info("Digital Twin Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Digital Twin Engine: {e}")
            raise
    
    async def shutdown(self):
        """Shutdown the digital twin engine"""
        logger.info("Shutting down Digital Twin Engine...")
        
        self.running = False
        
        # Cancel background tasks
        for task in self.background_tasks:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        
        # Shutdown components
        if self.synthetic_data_manager:
            await self.synthetic_data_manager.shutdown()
        if self.personality_model:
            await self.personality_model.shutdown()
        if self.health_monitor:
            await self.health_monitor.shutdown()
        if self.behavior_simulator:
            await self.behavior_simulator.shutdown()
        if self.conversation_engine:
            await self.conversation_engine.shutdown()
        if self.visualization_engine:
            await self.visualization_engine.shutdown()
        
        # Shutdown database manager
        await db_manager.shutdown()
        
        logger.info("Digital Twin Engine shutdown complete")
    
    async def create_twin(self, twin_config: Dict[str, Any]) -> str:
        """Create a new digital twin"""
        try:
            twin_id = f"twin_{len(self.twins) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create digital twin instance
            twin = DigitalTwin(
                twin_id=twin_id,
                name=twin_config.get("name", "Unnamed Twin"),
                description=twin_config.get("description", ""),
                personality_profile=twin_config.get("personality_profile", {}),
                health_profile=twin_config.get("health_profile", {}),
                visual_profile=twin_config.get("visual_profile", {})
            )
            
            # Initialize twin components
            await twin.initialize(
                personality_model=self.personality_model,
                health_monitor=self.health_monitor,
                behavior_simulator=self.behavior_simulator,
                conversation_engine=self.conversation_engine,
                visualization_engine=self.visualization_engine
            )
            
            self.twins[twin_id] = twin
            logger.info(f"Created digital twin: {twin_id}")
            
            return twin_id
            
        except Exception as e:
            logger.error(f"Failed to create digital twin: {e}")
            raise
    
    async def get_twin(self, twin_id: str) -> Optional[DigitalTwin]:
        """Get a digital twin by ID"""
        return self.twins.get(twin_id)
    
    async def update_twin(self, twin_id: str, updates: Dict[str, Any]) -> bool:
        """Update a digital twin"""
        twin = self.twins.get(twin_id)
        if not twin:
            return False
        
        try:
            await twin.update(updates)
            logger.info(f"Updated digital twin: {twin_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update digital twin {twin_id}: {e}")
            return False
    
    async def delete_twin(self, twin_id: str) -> bool:
        """Delete a digital twin"""
        twin = self.twins.get(twin_id)
        if not twin:
            return False
        
        try:
            await twin.shutdown()
            del self.twins[twin_id]
            logger.info(f"Deleted digital twin: {twin_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete digital twin {twin_id}: {e}")
            return False
    
    async def get_twin_state(self, twin_id: str) -> Optional[TwinState]:
        """Get the current state of a digital twin"""
        twin = self.twins.get(twin_id)
        if not twin:
            return None
        
        try:
            return TwinState(
                twin_id=twin_id,
                last_update=datetime.now(),
                            health_status=twin.get_health_status(),
            personality_state=twin.get_personality_state(),
            behavior_patterns=twin.get_behavior_patterns(),
            conversation_history=twin.get_conversation_history(),
            visual_state=twin.get_visual_state()
            )
        except Exception as e:
            logger.error(f"Failed to get twin state for {twin_id}: {e}")
            return None
    
    async def process_interaction(self, twin_id: str, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an interaction with a digital twin"""
        twin = self.twins.get(twin_id)
        if not twin:
            return {"error": "Twin not found"}
        
        try:
            response = await twin.process_interaction(interaction_data)
            return response
        except Exception as e:
            logger.error(f"Failed to process interaction for twin {twin_id}: {e}")
            return {"error": str(e)}
    
    async def _start_background_tasks(self):
        """Start background tasks for continuous operation"""
        # Health monitoring task
        health_task = asyncio.create_task(self._health_monitoring_loop())
        self.background_tasks.append(health_task)
        
        # Personality evolution task
        personality_task = asyncio.create_task(self._personality_evolution_loop())
        self.background_tasks.append(personality_task)
        
        # Behavior simulation task
        behavior_task = asyncio.create_task(self._behavior_simulation_loop())
        self.background_tasks.append(behavior_task)
        
        # Synthetic data generation task
        data_task = asyncio.create_task(self._synthetic_data_generation_loop())
        self.background_tasks.append(data_task)
        
        logger.info("Started background tasks")
    
    async def _health_monitoring_loop(self):
        """Background loop for health monitoring"""
        while self.running:
            try:
                for twin in self.twins.values():
                    twin.update_health_metrics()
                
                await asyncio.sleep(settings.HEALTH_UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(10)
    
    async def _personality_evolution_loop(self):
        """Background loop for personality evolution"""
        while self.running:
            try:
                for twin in self.twins.values():
                    twin.evolve_personality()
                
                await asyncio.sleep(settings.PERSONALITY_UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"Personality evolution error: {e}")
                await asyncio.sleep(10)
    
    async def _behavior_simulation_loop(self):
        """Background loop for behavior simulation"""
        while self.running:
            try:
                for twin in self.twins.values():
                    twin.simulate_behavior()
                
                await asyncio.sleep(30)  # More frequent updates
            except Exception as e:
                logger.error(f"Behavior simulation error: {e}")
                await asyncio.sleep(10)
    
    async def _synthetic_data_generation_loop(self):
        """Background loop for synthetic data generation"""
        while self.running:
            try:
                if self.synthetic_data_manager:
                    await self.synthetic_data_manager.generate_new_data()
                
                await asyncio.sleep(300)  # Generate new data every 5 minutes
            except Exception as e:
                logger.error(f"Synthetic data generation error: {e}")
                await asyncio.sleep(60)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the overall system status"""
        return {
            "status": "running" if self.running else "stopped",
            "active_twins": len(self.twins),
            "twin_ids": list(self.twins.keys()),
            "background_tasks": len(self.background_tasks),
            "components_initialized": {
                "synthetic_data_manager": self.synthetic_data_manager is not None,
                "personality_model": self.personality_model is not None,
                "health_monitor": self.health_monitor is not None,
                "behavior_simulator": self.behavior_simulator is not None,
                "conversation_engine": self.conversation_engine is not None,
                "visualization_engine": self.visualization_engine is not None
            }
        }
