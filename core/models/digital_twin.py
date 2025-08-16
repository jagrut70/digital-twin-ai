"""
Digital Twin Model
Represents an individual digital twin instance
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from uuid import uuid4

from .personality import PersonalityModel
from .health_monitor import HealthMonitor
from .behavior_simulator import BehaviorSimulator
from .conversation_engine import ConversationEngine
from .visualization_engine import VisualizationEngine

logger = logging.getLogger(__name__)

@dataclass
class TwinProfile:
    """Digital twin profile information"""
    name: str
    description: str
    age: int = 25
    gender: str = "unspecified"
    occupation: str = "student"
    interests: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    location: str = "unknown"
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class HealthMetrics:
    """Health and biometric metrics"""
    heart_rate: float = 72.0
    blood_pressure_systolic: int = 120
    blood_pressure_diastolic: int = 80
    temperature: float = 98.6
    oxygen_saturation: float = 98.0
    respiratory_rate: float = 16.0
    stress_level: float = 0.3
    energy_level: float = 0.8
    sleep_quality: float = 0.7
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PersonalityTraits:
    """Personality characteristics"""
    openness: float = 0.6
    conscientiousness: float = 0.7
    extraversion: float = 0.5
    agreeableness: float = 0.8
    neuroticism: float = 0.3
    emotional_stability: float = 0.7
    creativity: float = 0.6
    adaptability: float = 0.8
    confidence: float = 0.7
    empathy: float = 0.8

@dataclass
class BehaviorPattern:
    """Behavior pattern information"""
    pattern_type: str
    description: str
    frequency: float
    triggers: List[str]
    responses: List[str]
    confidence: float
    last_observed: datetime
    context: Dict[str, Any]

class DigitalTwin:
    """Main digital twin class"""
    
    def __init__(
        self,
        twin_id: str,
        name: str,
        description: str = "",
        personality_profile: Optional[Dict[str, Any]] = None,
        health_profile: Optional[Dict[str, Any]] = None,
        visual_profile: Optional[Dict[str, Any]] = None
    ):
        self.twin_id = twin_id
        self.profile = TwinProfile(name=name, description=description)
        
        # Initialize profiles
        self.personality_traits = PersonalityTraits()
        if personality_profile:
            self._update_personality_traits(personality_profile)
        
        self.health_metrics = HealthMetrics()
        if health_profile:
            self._update_health_metrics(health_profile)
        
        self.visual_profile = visual_profile or {}
        
        # Component references
        self.personality_model: Optional[PersonalityModel] = None
        self.health_monitor: Optional[HealthMonitor] = None
        self.behavior_simulator: Optional[BehaviorSimulator] = None
        self.conversation_engine: Optional[ConversationEngine] = None
        self.visualization_engine: Optional[VisualizationEngine] = None
        
        # State tracking
        self.behavior_patterns: List[BehaviorPattern] = []
        self.conversation_history: List[Dict[str, Any]] = []
        self.interaction_log: List[Dict[str, Any]] = []
        self.learning_history: List[Dict[str, Any]] = []
        
        # Timestamps
        self.created_at = datetime.now()
        self.last_interaction = datetime.now()
        self.last_health_update = datetime.now()
        self.last_personality_update = datetime.now()
        self.last_behavior_update = datetime.now()
        
        # Status
        self.is_active = True
        self.current_mood = "neutral"
        self.current_activity = "idle"
        self.energy_level = 0.8
        
        logger.info(f"Created digital twin: {twin_id} ({name})")
    
    async def initialize(
        self,
        personality_model: PersonalityModel,
        health_monitor: HealthMonitor,
        behavior_simulator: BehaviorSimulator,
        conversation_engine: ConversationEngine,
        visualization_engine: VisualizationEngine
    ):
        """Initialize the digital twin with all components"""
        self.personality_model = personality_model
        self.health_monitor = health_monitor
        self.behavior_simulator = behavior_simulator
        self.conversation_engine = conversation_engine
        self.visualization_engine = visualization_engine
        
        # Initialize synthetic data for the twin
        self._initialize_synthetic_data()
        
        logger.info(f"Initialized digital twin: {self.twin_id}")
    
    def _initialize_synthetic_data(self):
        """Initialize synthetic data for the twin"""
        try:
            # Generate synthetic personality data
            if self.personality_model:
                synthetic_personality = self.personality_model.generate_synthetic_profile(
                    age=self.profile.age,
                    gender=self.profile.gender,
                    occupation=self.profile.occupation
                )
                self._update_personality_traits(synthetic_personality)
            
            # Generate synthetic health baseline
            if self.health_monitor:
                synthetic_health = self.health_monitor.generate_synthetic_baseline(
                    age=self.profile.age,
                    gender=self.profile.gender
                )
                self._update_health_metrics(synthetic_health)
            
            # Generate synthetic behavior patterns
            if self.behavior_simulator:
                synthetic_behaviors = self.behavior_simulator.generate_synthetic_patterns(
                    personality_traits=self.personality_traits,
                    interests=self.profile.interests
                )
                self.behavior_patterns = synthetic_behaviors
            
            logger.info(f"Initialized synthetic data for twin: {self.twin_id}")
            
        except Exception as e:
            logger.error(f"Failed to initialize synthetic data for twin {self.twin_id}: {e}")
    
    def _update_personality_traits(self, traits: Dict[str, Any]):
        """Update personality traits from external data"""
        for key, value in traits.items():
            if hasattr(self.personality_traits, key):
                setattr(self.personality_traits, key, value)
    
    def _update_health_metrics(self, metrics: Dict[str, Any]):
        """Update health metrics from external data"""
        for key, value in metrics.items():
            if hasattr(self.health_metrics, key):
                setattr(self.health_metrics, key, value)
    
    async def update(self, updates: Dict[str, Any]):
        """Update the digital twin with new information"""
        try:
            # Update profile
            if "profile" in updates:
                profile_updates = updates["profile"]
                for key, value in profile_updates.items():
                    if hasattr(self.profile, key):
                        setattr(self.profile, key, value)
                self.profile.last_updated = datetime.now()
            
            # Update personality
            if "personality" in updates:
                self._update_personality_traits(updates["personality"])
                self.last_personality_update = datetime.now()
            
            # Update health
            if "health" in updates:
                self._update_health_metrics(updates["health"])
                self.last_health_update = datetime.now()
            
            # Update visual profile
            if "visual" in updates:
                self.visual_profile.update(updates["visual"])
            
            logger.info(f"Updated digital twin: {self.twin_id}")
            
        except Exception as e:
            logger.error(f"Failed to update twin {self.twin_id}: {e}")
            raise
    
    async def process_interaction(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an interaction with the digital twin"""
        try:
            interaction_id = str(uuid4())
            timestamp = datetime.now()
            
            # Log interaction
            interaction_log = {
                "interaction_id": interaction_id,
                "timestamp": timestamp,
                "type": interaction_data.get("type", "unknown"),
                "data": interaction_data,
                "twin_state": {
                    "mood": self.current_mood,
                    "activity": self.current_activity,
                    "energy": self.energy_level
                }
            }
            self.interaction_log.append(interaction_log)
            
            # Process based on interaction type
            response = await self._handle_interaction(interaction_data)
            
            # Update twin state based on interaction
            await self._update_state_from_interaction(interaction_data, response)
            
            # Update last interaction time
            self.last_interaction = timestamp
            
            return {
                "interaction_id": interaction_id,
                "response": response,
                "twin_state": {
                    "mood": self.current_mood,
                    "activity": self.current_activity,
                    "energy": self.energy_level,
                    "timestamp": timestamp.isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process interaction for twin {self.twin_id}: {e}")
            return {"error": str(e)}
    
    async def _handle_interaction(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle different types of interactions"""
        interaction_type = interaction_data.get("type", "unknown")
        
        if interaction_type == "conversation":
            return await self._handle_conversation(interaction_data)
        elif interaction_type == "health_query":
            return await self._handle_health_query(interaction_data)
        elif interaction_type == "behavior_request":
            return await self._handle_behavior_request(interaction_data)
        elif interaction_type == "visual_update":
            return await self._handle_visual_update(interaction_data)
        else:
            return {"message": "Unknown interaction type", "type": interaction_type}
    
    async def _handle_conversation(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle conversational interactions"""
        if not self.conversation_engine:
            return {"message": "Conversation engine not available"}
        
        message = interaction_data.get("message", "")
        context = interaction_data.get("context", {})
        sender = interaction_data.get("sender", "user")
        
        # Add twin state to context
        enhanced_context = {
            **context,
            "twin_state": {
                "mood": self.current_mood,
                "activity": self.current_activity,
                "energy": self.energy_level
            }
        }
        
        # Generate unique conversation ID for this twin
        conversation_id = f"twin_{self.twin_id}_{sender}"
        
        # Convert personality traits to dictionary if needed
        personality_dict = self.personality_traits
        if hasattr(self.personality_traits, '__dict__'):
            personality_dict = self.personality_traits.__dict__
        elif hasattr(self.personality_traits, '_asdict'):
            personality_dict = self.personality_traits._asdict()
        
        # Generate response using conversation engine
        response = self.conversation_engine.generate_response(
            personality_traits=personality_dict,
            message=message,
            sender=sender,
            conversation_id=conversation_id,
            context=enhanced_context
        )
        
        # Extract response text from response dict
        if isinstance(response, dict):
            response_text = response.get("response", "I'm here to help.")
            response_data = response
        else:
            response_text = str(response)
            response_data = {"response": response_text, "confidence": 0.7}
        
        # Log conversation
        conversation_entry = {
            "timestamp": datetime.now(),
            "user_message": message,
            "twin_response": response_text,
            "context": enhanced_context,
            "conversation_id": conversation_id,
            "metadata": response_data
        }
        self.conversation_history.append(conversation_entry)
        
        return {
            "response": response_text,
            "type": "conversation",
            "conversation_id": conversation_id,
            "metadata": response_data
        }
    
    async def _handle_health_query(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle health-related queries"""
        if not self.health_monitor:
            return {"message": "Health monitor not available"}
        
        query_type = interaction_data.get("query_type", "current_status")
        
        if query_type == "current_status":
            return {
                "health_metrics": {
                    "heart_rate": self.health_metrics.heart_rate,
                    "blood_pressure": f"{self.health_metrics.blood_pressure_systolic}/{self.health_metrics.blood_pressure_diastolic}",
                    "temperature": self.health_metrics.temperature,
                    "oxygen_saturation": self.health_metrics.oxygen_saturation,
                    "stress_level": self.health_metrics.stress_level,
                    "energy_level": self.health_metrics.energy_level
                },
                "timestamp": self.last_health_update.isoformat()
            }
        elif query_type == "trends":
            # Return health trends (would need historical data)
            return {"message": "Health trends analysis not yet implemented"}
        else:
            return {"message": "Unknown health query type"}
    
    async def _handle_behavior_request(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle behavior simulation requests"""
        if not self.behavior_simulator:
            return {"message": "Behavior simulator not available"}
        
        behavior_type = interaction_data.get("behavior_type", "current_patterns")
        
        if behavior_type == "current_patterns":
            return {
                "behavior_patterns": [
                    {
                        "type": pattern.pattern_type,
                        "description": pattern.description,
                        "frequency": pattern.frequency,
                        "confidence": pattern.confidence
                    }
                    for pattern in self.behavior_patterns
                ]
            }
        elif behavior_type == "simulate":
            # Simulate new behavior
            new_behavior = await self.behavior_simulator.simulate_behavior(
                personality_traits=self.personality_traits,
                current_context=interaction_data.get("context", {}),
                twin_state={
                    "mood": self.current_mood,
                    "activity": self.current_activity,
                    "energy": self.energy_level
                }
            )
            return {"simulated_behavior": new_behavior}
        else:
            return {"message": "Unknown behavior request type"}
    
    async def _handle_visual_update(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle visual representation updates"""
        if not self.visualization_engine:
            return {"message": "Visualization engine not available"}
        
        update_type = interaction_data.get("update_type", "current_state")
        
        if update_type == "current_state":
            return {
                "visual_state": self.visual_profile,
                "current_activity": self.current_activity,
                "mood_visualization": self.current_mood
            }
        elif update_type == "update":
            # Update visual representation
            visual_updates = interaction_data.get("visual_data", {})
            self.visual_profile.update(visual_updates)
            return {"message": "Visual profile updated", "new_state": self.visual_profile}
        else:
            return {"message": "Unknown visual update type"}
    
    async def _update_state_from_interaction(self, interaction_data: Dict[str, Any], response: Dict[str, Any]):
        """Update twin state based on interaction outcome"""
        # Update mood based on interaction
        if "mood_change" in response:
            self.current_mood = response["mood_change"]
        
        # Update activity
        if "activity_change" in response:
            self.current_activity = response["activity_change"]
        
        # Update energy level
        if "energy_change" in response:
            self.energy_level = max(0.0, min(1.0, self.energy_level + response["energy_change"]))
    
    def update_health_metrics(self):
        """Update health metrics using synthetic data"""
        if not self.health_monitor:
            return
        
        try:
            new_metrics = self.health_monitor.generate_synthetic_update(
                current_metrics=self.health_metrics,
                personality_traits=self.personality_traits,
                time_since_last_update=datetime.now() - self.last_health_update
            )
            
            self._update_health_metrics(new_metrics)
            self.last_health_update = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to update health metrics for twin {self.twin_id}: {e}")
    
    def evolve_personality(self):
        """Evolve personality traits over time"""
        if not self.personality_model:
            return
        
        try:
            evolution = self.personality_model.evolve_traits(
                current_traits=self.personality_traits,
                interaction_history=self.interaction_log,
                learning_history=self.learning_history,
                time_since_last_update=datetime.now() - self.last_personality_update
            )
            
            self._update_personality_traits(evolution)
            self.last_personality_update = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to evolve personality for twin {self.twin_id}: {e}")
    
    def simulate_behavior(self):
        """Simulate behavior patterns"""
        if not self.behavior_simulator:
            return
        
        try:
            new_patterns = self.behavior_simulator.simulate_patterns(
                personality_traits=self.personality_traits,
                current_patterns=self.behavior_patterns,
                twin_state={
                    "mood": self.current_mood,
                    "activity": self.current_activity,
                    "energy": self.energy_level
                }
            )
            
            # Update behavior patterns
            self.behavior_patterns = new_patterns
            self.last_behavior_update = datetime.now()
            
        except Exception as e:
            logger.error(f"Failed to simulate behavior for twin {self.twin_id}: {e}")
    
    def get_health_status(self) -> str:
        """Get current health status"""
        # Simple health status based on metrics
        if self.health_metrics.stress_level > 0.8:
            return "high_stress"
        elif self.health_metrics.energy_level < 0.3:
            return "low_energy"
        elif self.health_metrics.heart_rate > 100:
            return "elevated_heart_rate"
        else:
            return "healthy"
    
    def get_personality_state(self) -> Dict[str, Any]:
        """Get current personality state"""
        return {
            "traits": {
                "openness": self.personality_traits.openness,
                "conscientiousness": self.personality_traits.conscientiousness,
                "extraversion": self.personality_traits.extraversion,
                "agreeableness": self.personality_traits.agreeableness,
                "neuroticism": self.personality_traits.neuroticism
            },
            "current_mood": self.current_mood,
            "last_update": self.last_personality_update.isoformat()
        }
    
    def get_behavior_patterns(self) -> List[str]:
        """Get current behavior patterns"""
        return [pattern.pattern_type for pattern in self.behavior_patterns]
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history[-10:]  # Last 10 conversations
    
    def get_visual_state(self) -> Dict[str, Any]:
        """Get current visual state"""
        return {
            "profile": self.visual_profile,
            "current_activity": self.current_activity,
            "mood": self.current_mood,
            "energy_level": self.energy_level
        }
    
    async def shutdown(self):
        """Shutdown the digital twin"""
        self.is_active = False
        logger.info(f"Shutdown digital twin: {self.twin_id}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert twin to dictionary representation"""
        return {
            "twin_id": self.twin_id,
            "profile": {
                "name": self.profile.name,
                "description": self.profile.description,
                "age": self.profile.age,
                "gender": self.profile.gender,
                "occupation": self.profile.occupation,
                "interests": self.profile.interests,
                "skills": self.profile.skills,
                "location": self.profile.location,
                "created_at": self.profile.created_at.isoformat(),
                "last_updated": self.profile.last_updated.isoformat()
            },
            "personality_traits": {
                "openness": self.personality_traits.openness,
                "conscientiousness": self.personality_traits.conscientiousness,
                "extraversion": self.personality_traits.extraversion,
                "agreeableness": self.personality_traits.agreeableness,
                "neuroticism": self.personality_traits.neuroticism
            },
            "health_metrics": {
                "heart_rate": self.health_metrics.heart_rate,
                "blood_pressure": f"{self.health_metrics.blood_pressure_systolic}/{self.health_metrics.blood_pressure_diastolic}",
                "temperature": self.health_metrics.temperature,
                "energy_level": self.health_metrics.energy_level,
                "stress_level": self.health_metrics.stress_level
            },
            "current_state": {
                "mood": self.current_mood,
                "activity": self.current_activity,
                "energy": self.energy_level,
                "is_active": self.is_active
            },
            "timestamps": {
                "created_at": self.created_at.isoformat(),
                "last_interaction": self.last_interaction.isoformat(),
                "last_health_update": self.last_health_update.isoformat(),
                "last_personality_update": self.last_personality_update.isoformat()
            }
        }
