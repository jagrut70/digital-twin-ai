"""
Behavior Simulator for Digital Twins
Handles behavior patterns, decision-making, and behavioral simulation
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
class BehaviorEvent:
    """Individual behavior event"""
    event_id: str
    event_type: str
    timestamp: datetime
    context: Dict[str, Any]
    personality_influence: Dict[str, float]
    outcome: str
    duration: float
    energy_consumed: float

@dataclass
class BehaviorPattern:
    """Identified behavior pattern"""
    pattern_id: str
    pattern_type: str
    frequency: float
    triggers: List[str]
    responses: List[str]
    confidence: float
    last_observed: datetime
    context: Dict[str, Any]

@dataclass
class DecisionPoint:
    """Decision point in behavior simulation"""
    decision_id: str
    situation: str
    options: List[str]
    personality_factors: Dict[str, float]
    context_factors: Dict[str, Any]
    chosen_option: str
    confidence: float
    reasoning: str

class BehaviorSimulator:
    """Simulates realistic behavior patterns for digital twins"""
    
    def __init__(self):
        self.behavior_history: List[BehaviorEvent] = []
        self.behavior_patterns: List[BehaviorPattern] = []
        self.decision_history: List[DecisionPoint] = []
        
        self.behavior_types = [
            "social_interaction", "work_activity", "leisure_activity",
            "health_behavior", "learning_activity", "emotional_response",
            "routine_activity", "adaptive_behavior", "creative_activity"
        ]
        
        self.trigger_categories = [
            "time_based", "social_cues", "environmental", "emotional",
            "task_completion", "health_status", "external_events"
        ]
        
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the behavior simulator"""
        try:
            # Load behavior configurations
            await self._load_behavior_configs()
            
            # Initialize default behavior patterns
            await self._initialize_default_patterns()
            
            self.is_initialized = True
            logger.info("Behavior Simulator initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Behavior Simulator: {e}")
            raise
    
    async def _load_behavior_configs(self):
        """Load behavior simulation configurations"""
        # This could load from files, databases, or external APIs
        pass
    
    async def _initialize_default_patterns(self):
        """Initialize default behavior patterns"""
        default_patterns = [
            BehaviorPattern(
                pattern_id="morning_routine",
                pattern_type="routine_activity",
                frequency=0.9,
                triggers=["time_morning", "wake_up"],
                responses=["hygiene", "breakfast", "planning"],
                confidence=0.8,
                last_observed=datetime.now(),
                context={"time_of_day": "morning", "energy_level": "high"}
            ),
            BehaviorPattern(
                pattern_id="work_focus",
                pattern_type="work_activity",
                frequency=0.8,
                triggers=["work_time", "deadline", "task_assignment"],
                responses=["concentrated_work", "task_prioritization", "collaboration"],
                confidence=0.7,
                last_observed=datetime.now(),
                context={"environment": "work", "stress_level": "moderate"}
            ),
            BehaviorPattern(
                pattern_id="social_engagement",
                pattern_type="social_interaction",
                frequency=0.6,
                triggers=["social_opportunity", "shared_interest", "emotional_need"],
                responses=["active_participation", "listening", "sharing"],
                confidence=0.6,
                last_observed=datetime.now(),
                context={"social_context": "group", "mood": "positive"}
            )
        ]
        
        self.behavior_patterns.extend(default_patterns)
    
    async def simulate_behavior(self, personality_traits: Dict[str, float], context: Dict[str, Any]) -> BehaviorEvent:
        """Simulate a behavior event based on personality and context"""
        try:
            # Determine behavior type based on context and personality
            behavior_type = self._select_behavior_type(context, personality_traits)
            
            # Generate behavior context
            behavior_context = self._generate_behavior_context(behavior_type, context)
            
            # Calculate personality influence
            personality_influence = self._calculate_personality_influence(behavior_type, personality_traits)
            
            # Simulate behavior outcome
            outcome = self._simulate_behavior_outcome(behavior_type, personality_influence, context)
            
            # Calculate energy consumption
            energy_consumed = self._calculate_energy_consumption(behavior_type, context)
            
            # Create behavior event
            event = BehaviorEvent(
                event_id=f"event_{len(self.behavior_history) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                event_type=behavior_type,
                timestamp=datetime.now(),
                context=behavior_context,
                personality_influence=personality_influence,
                outcome=outcome,
                duration=random.uniform(0.5, 4.0),  # Hours
                energy_consumed=energy_consumed
            )
            
            # Add to history
            self.behavior_history.append(event)
            
            # Update behavior patterns
            await self._update_behavior_patterns(event)
            
            logger.info(f"Simulated behavior: {behavior_type} with outcome: {outcome}")
            return event
            
        except Exception as e:
            logger.error(f"Failed to simulate behavior: {e}")
            raise
    
    def _select_behavior_type(self, context: Dict[str, Any], personality_traits: Dict[str, float]) -> str:
        """Select behavior type based on context and personality"""
        # Time-based behavior selection
        time_of_day = context.get("time_of_day", "afternoon")
        hour = context.get("hour", 12)
        
        if 6 <= hour <= 9:  # Morning
            if random.random() < 0.7:
                return "routine_activity"
            elif random.random() < 0.5:
                return "work_activity"
            else:
                return "health_behavior"
        
        elif 9 <= hour <= 17:  # Work hours
            if random.random() < 0.6:
                return "work_activity"
            elif random.random() < 0.3:
                return "social_interaction"
            else:
                return "learning_activity"
        
        elif 17 <= hour <= 21:  # Evening
            if random.random() < 0.5:
                return "leisure_activity"
            elif random.random() < 0.4:
                return "social_interaction"
            else:
                return "health_behavior"
        
        else:  # Night
            if random.random() < 0.6:
                return "routine_activity"
            elif random.random() < 0.3:
                return "health_behavior"
            else:
                return "leisure_activity"
    
    def _generate_behavior_context(self, behavior_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed context for behavior simulation"""
        behavior_context = context.copy()
        
        if behavior_type == "social_interaction":
            behavior_context.update({
                "interaction_type": random.choice(["conversation", "collaboration", "social_event"]),
                "participants": random.randint(2, 8),
                "setting": random.choice(["work", "social", "casual", "formal"]),
                "topic": random.choice(["work", "personal", "hobbies", "current_events"])
            })
        
        elif behavior_type == "work_activity":
            behavior_context.update({
                "task_type": random.choice(["analysis", "creation", "collaboration", "planning"]),
                "complexity": random.choice(["simple", "moderate", "complex"]),
                "deadline_pressure": random.uniform(0.1, 0.9),
                "autonomy_level": random.uniform(0.3, 1.0)
            })
        
        elif behavior_type == "leisure_activity":
            behavior_context.update({
                "activity_category": random.choice(["entertainment", "hobbies", "sports", "relaxation"]),
                "social_component": random.choice([True, False]),
                "energy_level_required": random.uniform(0.2, 0.8),
                "duration_preference": random.choice(["short", "medium", "long"])
            })
        
        elif behavior_type == "health_behavior":
            behavior_context.update({
                "health_focus": random.choice(["exercise", "nutrition", "mental_health", "prevention"]),
                "intensity": random.choice(["light", "moderate", "intense"]),
                "consistency_level": random.uniform(0.3, 1.0)
            })
        
        return behavior_context
    
    def _calculate_personality_influence(self, behavior_type: str, personality_traits: Dict[str, float]) -> Dict[str, float]:
        """Calculate how personality traits influence behavior"""
        influence = {}
        
        if behavior_type == "social_interaction":
            influence["extraversion"] = personality_traits.get("extraversion", 0.5)
            influence["agreeableness"] = personality_traits.get("agreeableness", 0.5)
            influence["empathy"] = personality_traits.get("empathy", 0.5)
        
        elif behavior_type == "work_activity":
            influence["conscientiousness"] = personality_traits.get("conscientiousness", 0.5)
            influence["confidence"] = personality_traits.get("confidence", 0.5)
            influence["adaptability"] = personality_traits.get("adaptability", 0.5)
        
        elif behavior_type == "leisure_activity":
            influence["openness"] = personality_traits.get("openness", 0.5)
            influence["creativity"] = personality_traits.get("creativity", 0.5)
            influence["extraversion"] = personality_traits.get("extraversion", 0.5)
        
        elif behavior_type == "health_behavior":
            influence["conscientiousness"] = personality_traits.get("conscientiousness", 0.5)
            influence["emotional_stability"] = personality_traits.get("emotional_stability", 0.5)
            influence["adaptability"] = personality_traits.get("adaptability", 0.5)
        
        # Normalize influence values
        for trait in influence:
            influence[trait] = max(0.0, min(1.0, influence[trait]))
        
        return influence
    
    def _simulate_behavior_outcome(self, behavior_type: str, personality_influence: Dict[str, float], context: Dict[str, Any]) -> str:
        """Simulate the outcome of a behavior based on personality and context"""
        # Base success probability
        base_success = 0.6
        
        # Adjust based on personality influence
        avg_influence = sum(personality_influence.values()) / len(personality_influence) if personality_influence else 0.5
        success_probability = base_success + (avg_influence - 0.5) * 0.3
        
        # Context adjustments
        if context.get("stress_level", 0.5) > 0.7:
            success_probability -= 0.2
        if context.get("energy_level", 0.5) < 0.3:
            success_probability -= 0.2
        if context.get("supportive_environment", False):
            success_probability += 0.1
        
        # Determine outcome
        if random.random() < success_probability:
            if success_probability > 0.8:
                return "excellent_success"
            elif success_probability > 0.6:
                return "good_success"
            else:
                return "moderate_success"
        else:
            if success_probability < 0.3:
                return "significant_failure"
            else:
                return "minor_failure"
    
    def _calculate_energy_consumption(self, behavior_type: str, context: Dict[str, Any]) -> float:
        """Calculate energy consumption for a behavior"""
        base_energy = {
            "social_interaction": 0.3,
            "work_activity": 0.4,
            "leisure_activity": 0.2,
            "health_behavior": 0.5,
            "learning_activity": 0.4,
            "routine_activity": 0.1,
            "creative_activity": 0.3
        }
        
        energy = base_energy.get(behavior_type, 0.3)
        
        # Context adjustments
        if context.get("intensity", "moderate") == "high":
            energy *= 1.5
        elif context.get("intensity", "moderate") == "low":
            energy *= 0.7
        
        if context.get("duration", "medium") == "long":
            energy *= 1.3
        elif context.get("duration", "medium") == "short":
            energy *= 0.8
        
        # Stress and energy level effects
        if context.get("stress_level", 0.5) > 0.7:
            energy *= 1.2
        if context.get("energy_level", 0.5) < 0.3:
            energy *= 1.3
        
        return min(1.0, energy)
    
    async def _update_behavior_patterns(self, event: BehaviorEvent):
        """Update behavior patterns based on new events"""
        # Check if this event matches existing patterns
        for pattern in self.behavior_patterns:
            if self._matches_pattern(event, pattern):
                pattern.frequency = min(1.0, pattern.frequency + 0.1)
                pattern.last_observed = event.timestamp
                pattern.confidence = min(1.0, pattern.confidence + 0.05)
                return
        
        # Create new pattern if none matches
        new_pattern = BehaviorPattern(
            pattern_id=f"pattern_{len(self.behavior_patterns) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            pattern_type=event.event_type,
            frequency=0.1,
            triggers=[event.context.get("trigger", "unknown")],
            responses=[event.outcome],
            confidence=0.3,
            last_observed=event.timestamp,
            context=event.context
        )
        
        self.behavior_patterns.append(new_pattern)
    
    def _matches_pattern(self, event: BehaviorEvent, pattern: BehaviorPattern) -> bool:
        """Check if an event matches a behavior pattern"""
        # Basic type matching
        if event.event_type != pattern.pattern_type:
            return False
        
        # Context similarity check
        context_similarity = 0.0
        for key in event.context:
            if key in pattern.context:
                if isinstance(event.context[key], (int, float)) and isinstance(pattern.context[key], (int, float)):
                    # Numeric similarity
                    diff = abs(event.context[key] - pattern.context[key])
                    if diff < 0.2:  # Threshold for similarity
                        context_similarity += 0.2
                elif event.context[key] == pattern.context[key]:
                    context_similarity += 0.3
        
        return context_similarity > 0.3
    
    def make_decision(self, personality_traits: Dict[str, float], context: Dict[str, Any]) -> DecisionPoint:
        """Make a decision based on personality and context"""
        # Identify decision options
        options = self._identify_decision_options(context)
        
        # Calculate personality factors
        personality_factors = self._calculate_decision_factors(personality_traits, context)
        
        # Select option based on personality and context
        chosen_option = self._select_decision_option(options, personality_factors, context)
        
        # Calculate confidence
        confidence = self._calculate_decision_confidence(personality_factors, context)
        
        # Generate reasoning
        reasoning = self._generate_decision_reasoning(chosen_option, personality_factors, context)
        
        # Create decision point
        decision = DecisionPoint(
            decision_id=f"decision_{len(self.decision_history) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            situation=context.get("situation", "unknown"),
            options=options,
            personality_factors=personality_factors,
            context_factors=context,
            chosen_option=chosen_option,
            confidence=confidence,
            reasoning=reasoning
        )
        
        # Add to history
        self.decision_history.append(decision)
        
        return decision
    
    def _identify_decision_options(self, context: Dict[str, Any]) -> List[str]:
        """Identify possible decision options based on context"""
        situation = context.get("situation", "general")
        
        if situation == "work_challenge":
            return ["tackle_immediately", "plan_approach", "seek_help", "delegate"]
        elif situation == "social_conflict":
            return ["confront_directly", "mediate", "avoid", "seek_compromise"]
        elif situation == "health_decision":
            return ["immediate_action", "research_first", "consult_expert", "wait_and_observe"]
        elif situation == "creative_block":
            return ["push_through", "take_break", "change_approach", "seek_inspiration"]
        else:
            return ["option_1", "option_2", "option_3"]
    
    def _calculate_decision_factors(self, personality_traits: Dict[str, float], context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate decision-making factors based on personality"""
        factors = {}
        
        # Risk tolerance
        factors["risk_tolerance"] = 1.0 - personality_traits.get("emotional_stability", 0.5)
        
        # Social preference
        factors["social_preference"] = personality_traits.get("extraversion", 0.5)
        
        # Planning preference
        factors["planning_preference"] = personality_traits.get("conscientiousness", 0.5)
        
        # Adaptability
        factors["adaptability"] = personality_traits.get("adaptability", 0.5)
        
        # Confidence
        factors["confidence"] = personality_traits.get("confidence", 0.5)
        
        return factors
    
    def _select_decision_option(self, options: List[str], personality_factors: Dict[str, float], context: Dict[str, Any]) -> str:
        """Select decision option based on personality factors"""
        # Calculate scores for each option
        option_scores = {}
        
        for option in options:
            score = 0.0
            
            if "immediate" in option or "directly" in option:
                score += personality_factors.get("risk_tolerance", 0.5) * 0.3
                score += personality_factors.get("confidence", 0.5) * 0.2
            
            if "plan" in option or "approach" in option:
                score += personality_factors.get("planning_preference", 0.5) * 0.4
            
            if "help" in option or "consult" in option:
                score += personality_factors.get("social_preference", 0.5) * 0.3
            
            if "break" in option or "wait" in option:
                score += personality_factors.get("adaptability", 0.5) * 0.3
            
            option_scores[option] = score
        
        # Select option with highest score
        return max(option_scores, key=option_scores.get)
    
    def _calculate_decision_confidence(self, personality_factors: Dict[str, float], context: Dict[str, Any]) -> float:
        """Calculate confidence in the decision"""
        base_confidence = 0.6
        
        # Personality influence
        confidence_trait = personality_factors.get("confidence", 0.5)
        base_confidence += (confidence_trait - 0.5) * 0.3
        
        # Context influence
        if context.get("stress_level", 0.5) < 0.3:
            base_confidence += 0.1
        elif context.get("stress_level", 0.5) > 0.7:
            base_confidence -= 0.2
        
        if context.get("energy_level", 0.5) > 0.7:
            base_confidence += 0.1
        elif context.get("energy_level", 0.5) < 0.3:
            base_confidence -= 0.1
        
        return max(0.1, min(1.0, base_confidence))
    
    def _generate_decision_reasoning(self, chosen_option: str, personality_factors: Dict[str, float], context: Dict[str, Any]) -> str:
        """Generate reasoning for the chosen decision"""
        reasoning_templates = {
            "tackle_immediately": "High confidence and energy levels suggest immediate action is appropriate.",
            "plan_approach": "Conscientious personality traits favor careful planning and systematic approaches.",
            "seek_help": "Social preferences and current context suggest collaboration would be beneficial.",
            "mediate": "High empathy and agreeableness indicate mediation skills and conflict resolution approach.",
            "take_break": "Current stress levels and adaptability suggest a brief pause would be beneficial.",
            "research_first": "Planning preferences and current energy levels suggest thorough research before action."
        }
        
        return reasoning_templates.get(chosen_option, f"Chosen {chosen_option} based on personality factors and current context.")
    
    def get_behavior_summary(self) -> Dict[str, Any]:
        """Get a summary of behavior patterns and history"""
        return {
            "total_events": len(self.behavior_history),
            "pattern_count": len(self.behavior_patterns),
            "decision_count": len(self.decision_history),
            "recent_activity": [
                {
                    "type": event.event_type,
                    "outcome": event.outcome,
                    "timestamp": event.timestamp.isoformat()
                }
                for event in self.behavior_history[-5:]  # Last 5 events
            ],
            "top_patterns": sorted(
                self.behavior_patterns,
                key=lambda x: x.frequency,
                reverse=True
            )[:3]
        }
    
    def generate_synthetic_patterns(self, personality_traits: Any, interests: List[str]) -> List[Dict[str, Any]]:
        """Generate synthetic behavior patterns for a digital twin"""
        try:
            patterns = []
            
            # Handle both dict and dataclass personality traits
            extraversion_value = 0.5
            conscientiousness_value = 0.5
            
            if hasattr(personality_traits, 'extraversion'):
                extraversion_value = personality_traits.extraversion
            elif isinstance(personality_traits, dict):
                extraversion_value = personality_traits.get("extraversion", 0.5)
                
            if hasattr(personality_traits, 'conscientiousness'):
                conscientiousness_value = personality_traits.conscientiousness
            elif isinstance(personality_traits, dict):
                conscientiousness_value = personality_traits.get("conscientiousness", 0.5)
            
            # Generate patterns based on personality traits
            if extraversion_value > 0.7:
                patterns.append({
                    "pattern_type": "social_interaction",
                    "description": "High engagement in social activities",
                    "frequency": random.uniform(0.7, 0.9),
                    "triggers": ["social_gathering", "friend_contact", "work_meeting"],
                    "responses": ["initiate_conversation", "actively_participate", "organize_events"],
                    "confidence": random.uniform(0.8, 0.95),
                    "last_observed": datetime.now(),
                    "context": {"setting": "social", "energy_level": "high"}
                })
            
            if conscientiousness_value > 0.7:
                patterns.append({
                    "pattern_type": "work_habits",
                    "description": "Systematic and organized work approach",
                    "frequency": random.uniform(0.8, 0.95),
                    "triggers": ["work_deadline", "project_start", "task_assignment"],
                    "responses": ["plan_ahead", "create_schedule", "follow_procedures"],
                    "confidence": random.uniform(0.8, 0.95),
                    "last_observed": datetime.now(),
                    "context": {"setting": "work", "stress_level": "low"}
                })
            
            if interests:
                for interest in interests[:3]:  # Top 3 interests
                    patterns.append({
                        "pattern_type": "leisure_activity",
                        "description": f"Engagement in {interest} activities",
                        "frequency": random.uniform(0.5, 0.8),
                        "triggers": [f"{interest}_opportunity", "free_time", "mood_boost"],
                        "responses": ["seek_opportunities", "dedicate_time", "share_experiences"],
                        "confidence": random.uniform(0.7, 0.9),
                        "last_observed": datetime.now(),
                        "context": {"setting": "leisure", "interest": interest}
                    })
            
            # Add default patterns if none generated
            if not patterns:
                patterns.append({
                    "pattern_type": "adaptive_behavior",
                    "description": "General adaptive behavior pattern",
                    "frequency": random.uniform(0.4, 0.6),
                    "triggers": ["environmental_change", "new_situation", "stress"],
                    "responses": ["observe", "adapt", "learn"],
                    "confidence": random.uniform(0.6, 0.8),
                    "last_observed": datetime.now(),
                    "context": {"setting": "general", "adaptability": "moderate"}
                })
            
            logger.info(f"Generated {len(patterns)} synthetic behavior patterns")
            return patterns
            
        except Exception as e:
            logger.error(f"Failed to generate synthetic behavior patterns: {e}")
            return []
    
    def simulate_patterns(self, personality_traits: Any, current_patterns: List[Any], twin_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Simulate behavior patterns based on personality and current state"""
        try:
            new_patterns = []
            
            # Analyze current patterns and generate variations
            if current_patterns:
                for pattern in current_patterns[-3:]:  # Last 3 patterns
                    # Create variation of existing pattern
                    variation = {
                        "pattern_type": pattern.pattern_type if hasattr(pattern, 'pattern_type') else "unknown",
                        "description": f"Variation of {pattern.pattern_type if hasattr(pattern, 'pattern_type') else 'previous'} pattern",
                        "frequency": min(1.0, (pattern.frequency if hasattr(pattern, 'frequency') else 0.5) + random.uniform(-0.1, 0.1)),
                        "triggers": pattern.triggers if hasattr(pattern, 'triggers') else ["general"],
                        "responses": pattern.responses if hasattr(pattern, 'responses') else ["adapt"],
                        "confidence": random.uniform(0.6, 0.9),
                        "last_observed": datetime.now(),
                        "context": twin_state
                    }
                    new_patterns.append(variation)
            
            # Generate new patterns based on personality and state
            if twin_state.get("energy_level", 0.5) > 0.7:
                new_patterns.append({
                    "pattern_type": "high_energy_activity",
                    "description": "High energy behavior pattern",
                    "frequency": random.uniform(0.6, 0.8),
                    "triggers": ["high_energy", "positive_mood", "free_time"],
                    "responses": ["engage_activity", "socialize", "exercise"],
                    "confidence": random.uniform(0.7, 0.9),
                    "last_observed": datetime.now(),
                    "context": twin_state
                })
            
            # Handle personality traits - support both dict and dataclass objects
            extraversion_value = 0.5
            if hasattr(personality_traits, 'extraversion'):
                extraversion_value = personality_traits.extraversion
            elif isinstance(personality_traits, dict):
                extraversion_value = personality_traits.get("extraversion", 0.5)
            
            if extraversion_value > 0.7:
                new_patterns.append({
                    "pattern_type": "social_engagement",
                    "description": "Active social engagement pattern",
                    "frequency": random.uniform(0.7, 0.9),
                    "triggers": ["social_opportunity", "group_activity", "communication"],
                    "responses": ["initiate_interaction", "participate_actively", "lead_activity"],
                    "confidence": random.uniform(0.8, 0.95),
                    "last_observed": datetime.now(),
                    "context": twin_state
                })
            
            # If no new patterns generated, create a default adaptive pattern
            if not new_patterns:
                new_patterns.append({
                    "pattern_type": "adaptive_behavior",
                    "description": "General adaptive behavior pattern",
                    "frequency": random.uniform(0.4, 0.6),
                    "triggers": ["environmental_change", "new_situation"],
                    "responses": ["observe", "adapt", "learn"],
                    "confidence": random.uniform(0.6, 0.8),
                    "last_observed": datetime.now(),
                    "context": twin_state
                })
            
            logger.info(f"Simulated {len(new_patterns)} behavior patterns based on personality and state")
            return new_patterns
            
        except Exception as e:
            logger.error(f"Failed to simulate behavior patterns: {e}")
            return []
    
    async def shutdown(self):
        """Shutdown the behavior simulator"""
        self.is_initialized = False
        logger.info("Behavior Simulator shutdown complete")
