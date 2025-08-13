"""
Personality Model for Digital Twins
Handles personality traits, evolution, and decision-making
"""

import asyncio
import logging
import random
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class PersonalityState:
    """Current personality state"""
    traits: Dict[str, float]
    mood: str
    energy_level: float
    stress_level: float
    social_energy: float
    last_update: datetime
    context: Dict[str, Any]

@dataclass
class DecisionContext:
    """Context for decision-making"""
    situation: str
    options: List[str]
    current_mood: str
    social_context: str
    time_of_day: str
    recent_events: List[str]

class PersonalityModel:
    """Manages personality traits and decision-making for digital twins"""
    
    def __init__(self):
        self.base_traits = {
            "openness": 0.5,
            "conscientiousness": 0.5,
            "extraversion": 0.5,
            "agreeableness": 0.5,
            "neuroticism": 0.5,
            "emotional_stability": 0.5,
            "creativity": 0.5,
            "adaptability": 0.5,
            "confidence": 0.5,
            "empathy": 0.5
        }
        
        self.mood_states = [
            "happy", "calm", "excited", "focused", "relaxed",
            "anxious", "stressed", "tired", "irritated", "melancholy"
        ]
        
        self.decision_patterns = {
            "risk_taking": {"high": 0.3, "medium": 0.5, "low": 0.2},
            "social_preference": {"group": 0.4, "individual": 0.3, "mixed": 0.3},
            "planning_style": {"structured": 0.4, "flexible": 0.4, "spontaneous": 0.2}
        }
        
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the personality model"""
        try:
            # Load any pre-trained models or configurations
            await self._load_personality_configs()
            
            self.is_initialized = True
            logger.info("Personality Model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Personality Model: {e}")
            raise
    
    async def _load_personality_configs(self):
        """Load personality model configurations"""
        # This could load from files, databases, or external APIs
        pass
    
    def generate_personality_profile(self, age: int, occupation: str, interests: List[str]) -> Dict[str, float]:
        """Generate a personality profile based on demographics"""
        profile = self.base_traits.copy()
        
        # Age-based adjustments
        if age < 25:
            profile["openness"] += 0.2
            profile["extraversion"] += 0.1
        elif age > 50:
            profile["conscientiousness"] += 0.2
            profile["emotional_stability"] += 0.1
        
        # Occupation-based adjustments
        occupation_modifiers = {
            "engineer": {"conscientiousness": 0.3, "openness": 0.1},
            "artist": {"creativity": 0.4, "openness": 0.3},
            "teacher": {"empathy": 0.3, "agreeableness": 0.2},
            "manager": {"confidence": 0.3, "extraversion": 0.2},
            "student": {"openness": 0.2, "adaptability": 0.2}
        }
        
        if occupation in occupation_modifiers:
            for trait, modifier in occupation_modifiers[occupation].items():
                if trait in profile:
                    profile[trait] = min(1.0, profile[trait] + modifier)
        
        # Interest-based adjustments
        creative_interests = ["art", "music", "writing", "design"]
        social_interests = ["sports", "dancing", "volunteering", "clubs"]
        analytical_interests = ["science", "math", "puzzles", "programming"]
        
        if any(interest in interests for interest in creative_interests):
            profile["creativity"] += 0.2
        if any(interest in interests for interest in social_interests):
            profile["extraversion"] += 0.2
        if any(interest in interests for interest in analytical_interests):
            profile["conscientiousness"] += 0.2
        
        # Normalize all values to [0, 1]
        for trait in profile:
            profile[trait] = max(0.0, min(1.0, profile[trait]))
        
        return profile
    
    def evolve_personality(self, current_traits: Dict[str, float], experiences: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evolve personality based on experiences"""
        evolved_traits = current_traits.copy()
        
        for experience in experiences:
            experience_type = experience.get("type", "")
            intensity = experience.get("intensity", 0.1)
            
            if experience_type == "positive_social":
                evolved_traits["extraversion"] += intensity * 0.1
                evolved_traits["agreeableness"] += intensity * 0.1
            elif experience_type == "challenging_work":
                evolved_traits["conscientiousness"] += intensity * 0.1
                evolved_traits["confidence"] += intensity * 0.1
            elif experience_type == "creative_activity":
                evolved_traits["creativity"] += intensity * 0.1
                evolved_traits["openness"] += intensity * 0.1
            elif experience_type == "stressful_situation":
                evolved_traits["emotional_stability"] += intensity * 0.05
                evolved_traits["adaptability"] += intensity * 0.1
        
        # Normalize all values to [0, 1]
        for trait in evolved_traits:
            evolved_traits[trait] = max(0.0, min(1.0, evolved_traits[trait]))
        
        return evolved_traits
    
    def determine_mood(self, personality_traits: Dict[str, float], context: Dict[str, Any]) -> str:
        """Determine current mood based on personality and context"""
        # Base mood influenced by personality
        base_mood_score = 0.5
        
        # Extraversion affects social energy
        if context.get("social_interaction", False):
            base_mood_score += personality_traits.get("extraversion", 0.5) * 0.3
        
        # Emotional stability affects stress response
        if context.get("stressful", False):
            base_mood_score -= (1.0 - personality_traits.get("emotional_stability", 0.5)) * 0.4
        
        # Openness affects response to new experiences
        if context.get("new_experience", False):
            base_mood_score += personality_traits.get("openness", 0.5) * 0.2
        
        # Time of day effects
        hour = context.get("hour", 12)
        if 6 <= hour <= 10:  # Morning
            base_mood_score += 0.1
        elif 22 <= hour or hour <= 4:  # Late night
            base_mood_score -= 0.1
        
        # Determine mood category
        if base_mood_score > 0.7:
            return random.choice(["happy", "excited", "focused"])
        elif base_mood_score > 0.4:
            return random.choice(["calm", "relaxed", "focused"])
        elif base_mood_score > 0.2:
            return random.choice(["tired", "melancholy", "anxious"])
        else:
            return random.choice(["stressed", "irritated", "anxious"])
    
    def make_decision(self, personality_traits: Dict[str, float], context: DecisionContext) -> Dict[str, Any]:
        """Make a decision based on personality and context"""
        decision_factors = {}
        
        # Risk tolerance based on personality
        risk_threshold = 0.5
        if personality_traits.get("confidence", 0.5) > 0.7:
            risk_threshold -= 0.2
        if personality_traits.get("emotional_stability", 0.5) < 0.3:
            risk_threshold += 0.2
        
        # Social preference
        if personality_traits.get("extraversion", 0.5) > 0.7:
            decision_factors["social_choice"] = "group"
        elif personality_traits.get("extraversion", 0.5) < 0.3:
            decision_factors["social_choice"] = "individual"
        else:
            decision_factors["social_choice"] = "mixed"
        
        # Planning style
        if personality_traits.get("conscientiousness", 0.5) > 0.7:
            decision_factors["planning"] = "structured"
        elif personality_traits.get("adaptability", 0.5) > 0.7:
            decision_factors["planning"] = "flexible"
        else:
            decision_factors["planning"] = "spontaneous"
        
        # Decision confidence
        confidence = personality_traits.get("confidence", 0.5)
        if context.current_mood in ["happy", "excited", "focused"]:
            confidence += 0.2
        elif context.current_mood in ["tired", "anxious"]:
            confidence -= 0.2
        
        decision_factors["confidence"] = max(0.1, min(1.0, confidence))
        decision_factors["risk_tolerance"] = risk_threshold
        
        return decision_factors
    
    def predict_behavior(self, personality_traits: Dict[str, float], situation: str) -> Dict[str, Any]:
        """Predict likely behavior in a given situation"""
        prediction = {
            "likely_response": "",
            "confidence": 0.0,
            "alternative_responses": []
        }
        
        if situation == "social_gathering":
            if personality_traits.get("extraversion", 0.5) > 0.7:
                prediction["likely_response"] = "actively_engage"
                prediction["confidence"] = 0.8
                prediction["alternative_responses"] = ["observe_first", "selective_interaction"]
            else:
                prediction["likely_response"] = "observe_first"
                prediction["confidence"] = 0.7
                prediction["alternative_responses"] = ["selective_interaction", "minimal_participation"]
        
        elif situation == "work_challenge":
            if personality_traits.get("conscientiousness", 0.5) > 0.7:
                prediction["likely_response"] = "systematic_approach"
                prediction["confidence"] = 0.8
                prediction["alternative_responses"] = ["research_first", "collaborate"]
            else:
                prediction["likely_response"] = "adaptive_approach"
                prediction["confidence"] = 0.6
                prediction["alternative_responses"] = ["collaborate", "trial_and_error"]
        
        elif situation == "new_experience":
            if personality_traits.get("openness", 0.5) > 0.7:
                prediction["likely_response"] = "embrace_opportunity"
                prediction["confidence"] = 0.8
                prediction["alternative_responses"] = ["cautious_exploration", "research_first"]
            else:
                prediction["likely_response"] = "cautious_exploration"
                prediction["confidence"] = 0.7
                prediction["alternative_responses"] = ["research_first", "avoid_if_possible"]
        
        return prediction
    
    def generate_synthetic_profile(self, age: int, gender: str, occupation: str) -> Dict[str, Any]:
        """Generate a synthetic personality profile for a digital twin"""
        try:
            # Generate personality profile based on provided demographics
            profile = self.generate_personality_profile(age, occupation, [])
            
            # Add synthetic metadata
            synthetic_profile = {
                "personality_traits": profile,
                "age": age,
                "gender": gender,
                "occupation": occupation,
                "generated_at": datetime.now().isoformat(),
                "confidence": random.uniform(0.7, 0.95)
            }
            
            logger.info(f"Generated synthetic personality profile for age {age}, {gender}, {occupation}")
            return synthetic_profile
            
        except Exception as e:
            logger.error(f"Failed to generate synthetic personality profile: {e}")
            return {
                "personality_traits": self.base_traits.copy(),
                "error": str(e)
            }
    
    def evolve_traits(self, current_traits: Any, interaction_history: List[Dict[str, Any]], learning_history: List[Dict[str, Any]], time_since_last_update: timedelta) -> Dict[str, float]:
        """Evolve personality traits based on context and experiences"""
        try:
            # Convert dataclass to dict if needed
            if hasattr(current_traits, '__dict__'):
                evolved_traits = {k: v for k, v in current_traits.__dict__.items() if not k.startswith('_')}
            else:
                evolved_traits = current_traits.copy()
            
            # Interaction-based evolution
            if interaction_history:
                recent_interactions = interaction_history[-5:]  # Last 5 interactions
                positive_count = sum(1 for i in recent_interactions if i.get("outcome") == "positive")
                if positive_count > len(recent_interactions) / 2:
                    evolved_traits["confidence"] = min(1.0, evolved_traits.get("confidence", 0.5) + 0.03)
                    evolved_traits["emotional_stability"] = min(1.0, evolved_traits.get("emotional_stability", 0.5) + 0.02)
            
            # Learning-based evolution
            if learning_history:
                recent_learning = learning_history[-3:]  # Last 3 learning events
                if recent_learning:
                    evolved_traits["openness"] = min(1.0, evolved_traits.get("openness", 0.5) + 0.02)
                    evolved_traits["creativity"] = min(1.0, evolved_traits.get("creativity", 0.5) + 0.02)
            
            # Time-based evolution (subtle changes over time)
            days_since_update = time_since_last_update.days
            if days_since_update > 7:
                # Weekly evolution
                for trait in evolved_traits:
                    variation = random.uniform(-0.01, 0.01)
                    evolved_traits[trait] = max(0.0, min(1.0, evolved_traits[trait] + variation))
            
            logger.info(f"Evolved personality traits based on {len(interaction_history)} interactions and {len(learning_history)} learning events")
            return evolved_traits
            
        except Exception as e:
            logger.error(f"Failed to evolve personality traits: {e}")
            # Return as dict if possible
            if hasattr(current_traits, '__dict__'):
                return {k: v for k, v in current_traits.__dict__.items() if not k.startswith('_')}
            return current_traits
    
    async def shutdown(self):
        """Shutdown the personality model"""
        self.is_initialized = False
        logger.info("Personality Model shutdown complete")
