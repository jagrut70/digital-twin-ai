"""
Synthetic Data Manager
Handles generation and management of synthetic datasets for digital twins
"""

import asyncio
import logging
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import numpy as np
from faker import Faker

from ..config import settings

logger = logging.getLogger(__name__)

class SyntheticDataManager:
    """Manages synthetic data generation and storage"""
    
    def __init__(self):
        self.faker = Faker()
        self.data_cache: Dict[str, Any] = {}
        self.generation_rules: Dict[str, Any] = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the synthetic data manager"""
        try:
            # Load generation rules
            await self._load_generation_rules()
            
            # Initialize data directories
            await self._initialize_directories()
            
            # Generate initial synthetic datasets
            await self._generate_initial_datasets()
            
            self.is_initialized = True
            logger.info("Synthetic Data Manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Synthetic Data Manager: {e}")
            raise
    
    async def _load_generation_rules(self):
        """Load rules for synthetic data generation"""
        self.generation_rules = {
            "personality": {
                "age_ranges": {
                    "teen": (13, 19),
                    "young_adult": (20, 29),
                    "adult": (30, 49),
                    "senior": (50, 80)
                },
                "occupation_personality_mapping": {
                    "student": {"openness": 0.8, "conscientiousness": 0.6},
                    "engineer": {"openness": 0.7, "conscientiousness": 0.9},
                    "artist": {"openness": 0.9, "creativity": 0.9},
                    "manager": {"extraversion": 0.8, "confidence": 0.8}
                }
            },
            "health": {
                "baseline_ranges": {
                    "heart_rate": (60, 100),
                    "blood_pressure_systolic": (90, 140),
                    "blood_pressure_diastolic": (60, 90),
                    "temperature": (97.0, 99.0),
                    "oxygen_saturation": (95.0, 100.0)
                },
                "age_health_factors": {
                    "teen": {"energy": 0.9, "stress": 0.4},
                    "young_adult": {"energy": 0.8, "stress": 0.5},
                    "adult": {"energy": 0.7, "stress": 0.6},
                    "senior": {"energy": 0.6, "stress": 0.3}
                }
            },
            "behavior": {
                "pattern_types": [
                    "social_interaction", "work_habits", "leisure_activities",
                    "health_behaviors", "learning_patterns", "emotional_responses"
                ],
                "trigger_categories": [
                    "time_based", "social_cues", "environmental", "emotional",
                    "task_completion", "health_status"
                ]
            }
        }
    
    async def _initialize_directories(self):
        """Initialize data storage directories"""
        directories = [
            settings.SYNTHETIC_DATA_PATH,
            settings.SYNBODY_DATASET_PATH,
            settings.ARIA_DATASET_PATH,
            settings.SIPHER_DATASET_PATH
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    async def _generate_initial_datasets(self):
        """Generate initial synthetic datasets"""
        try:
            # Generate sample personality profiles
            await self._generate_personality_profiles()
            
            # Generate sample health baselines
            await self._generate_health_baselines()
            
            # Generate sample behavior patterns
            await self._generate_behavior_patterns()
            
            logger.info("Generated initial synthetic datasets")
            
        except Exception as e:
            logger.error(f"Failed to generate initial datasets: {e}")
    
    async def _generate_personality_profiles(self):
        """Generate synthetic personality profiles"""
        profiles = []
        
        for i in range(100):
            age = random.randint(18, 65)
            age_group = self._get_age_group(age)
            occupation = random.choice(list(self.generation_rules["personality"]["occupation_personality_mapping"].keys()))
            
            profile = {
                "profile_id": f"personality_{i+1}",
                "age": age,
                "age_group": age_group,
                "occupation": occupation,
                "personality_traits": self._generate_personality_traits(age_group, occupation),
                "interests": self._generate_interests(age_group, occupation),
                "skills": self._generate_skills(occupation),
                "created_at": datetime.now().isoformat()
            }
            profiles.append(profile)
        
        # Save to file
        file_path = os.path.join(settings.SYNTHETIC_DATA_PATH, "personality_profiles.json")
        with open(file_path, 'w') as f:
            json.dump(profiles, f, indent=2)
        
        self.data_cache["personality_profiles"] = profiles
        logger.info(f"Generated {len(profiles)} personality profiles")
    
    async def _generate_health_baselines(self):
        """Generate synthetic health baselines"""
        baselines = []
        
        for i in range(100):
            age = random.randint(18, 65)
            age_group = self._get_age_group(age)
            gender = random.choice(["male", "female", "other"])
            
            baseline = {
                "baseline_id": f"health_{i+1}",
                "age": age,
                "age_group": age_group,
                "gender": gender,
                "health_metrics": self._generate_health_metrics(age_group, gender),
                "health_factors": self.generation_rules["health"]["age_health_factors"][age_group],
                "created_at": datetime.now().isoformat()
            }
            baselines.append(baseline)
        
        # Save to file
        file_path = os.path.join(settings.SYNTHETIC_DATA_PATH, "health_baselines.json")
        with open(file_path, 'w') as f:
            json.dump(baselines, f, indent=2)
        
        self.data_cache["health_baselines"] = baselines
        logger.info(f"Generated {len(baselines)} health baselines")
    
    async def _generate_behavior_patterns(self):
        """Generate synthetic behavior patterns"""
        patterns = []
        
        for i in range(50):
            pattern_type = random.choice(self.generation_rules["behavior"]["pattern_types"])
            trigger_category = random.choice(self.generation_rules["behavior"]["trigger_categories"])
            
            pattern = {
                "pattern_id": f"behavior_{i+1}",
                "pattern_type": pattern_type,
                "description": f"Synthetic {pattern_type} pattern",
                "frequency": random.uniform(0.1, 1.0),
                "triggers": self._generate_triggers(trigger_category),
                "responses": self._generate_responses(pattern_type),
                "confidence": random.uniform(0.6, 0.95),
                "context": self._generate_behavior_context(pattern_type),
                "created_at": datetime.now().isoformat()
            }
            patterns.append(pattern)
        
        # Save to file
        file_path = os.path.join(settings.SYNTHETIC_DATA_PATH, "behavior_patterns.json")
        with open(file_path, 'w') as f:
            json.dump(patterns, f, indent=2)
        
        self.data_cache["behavior_patterns"] = patterns
        logger.info(f"Generated {len(patterns)} behavior patterns")
    
    def _get_age_group(self, age: int) -> str:
        """Get age group based on age"""
        if age < 20:
            return "teen"
        elif age < 30:
            return "young_adult"
        elif age < 50:
            return "adult"
        else:
            return "senior"
    
    def _generate_personality_traits(self, age_group: str, occupation: str) -> Dict[str, float]:
        """Generate personality traits based on age group and occupation"""
        base_traits = {
            "openness": random.uniform(0.3, 0.9),
            "conscientiousness": random.uniform(0.3, 0.9),
            "extraversion": random.uniform(0.3, 0.9),
            "agreeableness": random.uniform(0.3, 0.9),
            "neuroticism": random.uniform(0.1, 0.7),
            "emotional_stability": random.uniform(0.4, 0.9),
            "creativity": random.uniform(0.3, 0.9),
            "adaptability": random.uniform(0.4, 0.9),
            "confidence": random.uniform(0.3, 0.9),
            "empathy": random.uniform(0.4, 0.9)
        }
        
        # Apply occupation-based adjustments
        if occupation in self.generation_rules["personality"]["occupation_personality_mapping"]:
            occupation_adjustments = self.generation_rules["personality"]["occupation_personality_mapping"][occupation]
            for trait, adjustment in occupation_adjustments.items():
                if trait in base_traits:
                    base_traits[trait] = adjustment
        
        return base_traits
    
    def _generate_interests(self, age_group: str, occupation: str) -> List[str]:
        """Generate interests based on age group and occupation"""
        all_interests = [
            "technology", "sports", "music", "reading", "travel", "cooking",
            "art", "gaming", "fitness", "photography", "writing", "dancing",
            "hiking", "swimming", "painting", "programming", "design", "science"
        ]
        
        # Select random interests
        num_interests = random.randint(3, 8)
        return random.sample(all_interests, num_interests)
    
    def _generate_skills(self, occupation: str) -> List[str]:
        """Generate skills based on occupation"""
        occupation_skills = {
            "student": ["research", "writing", "critical_thinking", "time_management"],
            "engineer": ["programming", "problem_solving", "mathematics", "design"],
            "artist": ["creativity", "visual_design", "color_theory", "composition"],
            "manager": ["leadership", "communication", "planning", "decision_making"]
        }
        
        base_skills = occupation_skills.get(occupation, ["communication", "problem_solving"])
        additional_skills = ["adaptability", "teamwork", "learning", "organization"]
        
        return base_skills + random.sample(additional_skills, 2)
    
    def _generate_health_metrics(self, age_group: str = "adult", gender: str = "unspecified") -> Dict[str, float]:
        """Generate health metrics based on age group and gender"""
        ranges = self.generation_rules["health"]["baseline_ranges"]
        
        metrics = {
            "heart_rate": random.uniform(ranges["heart_rate"][0], ranges["heart_rate"][1]),
            "blood_pressure_systolic": random.randint(ranges["blood_pressure_systolic"][0], ranges["blood_pressure_systolic"][1]),
            "blood_pressure_diastolic": random.randint(ranges["blood_pressure_diastolic"][0], ranges["blood_pressure_diastolic"][1]),
            "temperature": random.uniform(ranges["temperature"][0], ranges["temperature"][1]),
            "oxygen_saturation": random.uniform(ranges["oxygen_saturation"][0], ranges["oxygen_saturation"][1]),
            "respiratory_rate": random.uniform(12.0, 20.0),
            "stress_level": random.uniform(0.1, 0.8),
            "energy_level": random.uniform(0.4, 0.9),
            "sleep_quality": random.uniform(0.3, 0.9)
        }
        
        return metrics
    
    def _generate_triggers(self, trigger_category: str) -> List[str]:
        """Generate triggers for behavior patterns"""
        trigger_templates = {
            "time_based": ["morning", "afternoon", "evening", "weekend"],
            "social_cues": ["friend_contact", "work_meeting", "family_gathering"],
            "environmental": ["weather_change", "noise_level", "crowded_space"],
            "emotional": ["stress", "happiness", "sadness", "excitement"],
            "task_completion": ["work_done", "goal_achieved", "deadline_met"],
            "health_status": ["low_energy", "good_health", "illness"]
        }
        
        base_triggers = trigger_templates.get(trigger_category, ["general"])
        return random.sample(base_triggers, min(3, len(base_triggers)))
    
    def _generate_responses(self, pattern_type: str) -> List[str]:
        """Generate responses for behavior patterns"""
        response_templates = {
            "social_interaction": ["initiate_conversation", "withdraw", "observe", "participate"],
            "work_habits": ["focus_intensely", "take_breaks", "collaborate", "work_independently"],
            "leisure_activities": ["exercise", "read", "socialize", "relax"],
            "health_behaviors": ["eat_healthy", "exercise", "meditate", "sleep_well"],
            "learning_patterns": ["research", "practice", "ask_questions", "experiment"],
            "emotional_responses": ["express_feelings", "suppress_emotions", "seek_support", "self_reflect"]
        }
        
        base_responses = response_templates.get(pattern_type, ["adapt", "respond", "react"])
        return random.sample(base_responses, min(2, len(base_responses)))
    
    def _generate_behavior_context(self, pattern_type: str) -> Dict[str, Any]:
        """Generate context for behavior patterns"""
        return {
            "environment": random.choice(["home", "work", "public", "social"]),
            "time_of_day": random.choice(["morning", "afternoon", "evening", "night"]),
            "social_setting": random.choice(["alone", "small_group", "large_group", "one_on_one"]),
            "emotional_state": random.choice(["calm", "excited", "stressed", "happy", "sad"]),
            "energy_level": random.uniform(0.3, 0.9)
        }
    
    async def generate_new_data(self):
        """Generate new synthetic data"""
        try:
            # Generate new personality profiles
            await self._generate_personality_profiles()
            
            # Generate new health baselines
            await self._generate_health_baselines()
            
            # Generate new behavior patterns
            await self._generate_behavior_patterns()
            
            logger.info("Generated new synthetic data")
            
        except Exception as e:
            logger.error(f"Failed to generate new data: {e}")
    
    async def get_synthetic_profile(self, profile_type: str, criteria: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get a synthetic profile based on criteria"""
        if profile_type not in self.data_cache:
            return None
        
        profile_list = self.data_cache[profile_type]
        
        # Simple matching based on criteria
        for profile in profile_list:
            if self._matches_criteria(profile, criteria):
                return profile
        
        return None
    
    def _matches_criteria(self, profile: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if profile matches given criteria"""
        for key, value in criteria.items():
            if key in profile:
                if isinstance(value, (int, float)):
                    # Allow some tolerance for numeric values
                    if abs(profile[key] - value) > 0.1:
                        return False
                elif profile[key] != value:
                    return False
            else:
                return False
        return True
    
    def _generate_personality_profile(self) -> Dict[str, Any]:
        """Generate a single personality profile"""
        age = random.randint(18, 75)
        gender = random.choice(["male", "female", "non-binary", "prefer_not_to_say"])
        occupation = random.choice(["student", "engineer", "artist", "teacher", "doctor", "entrepreneur"])
        
        return {
            "age": age,
            "gender": gender,
            "occupation": occupation,
            "personality_traits": {
                "openness": random.uniform(0.3, 0.9),
                "conscientiousness": random.uniform(0.3, 0.9),
                "extraversion": random.uniform(0.3, 0.9),
                "agreeableness": random.uniform(0.3, 0.9),
                "neuroticism": random.uniform(0.1, 0.7),
                "emotional_stability": random.uniform(0.3, 0.9),
                "creativity": random.uniform(0.3, 0.9),
                "adaptability": random.uniform(0.3, 0.9),
                "confidence": random.uniform(0.3, 0.9),
                "empathy": random.uniform(0.3, 0.9)
            }
        }
    

    
    def _generate_behavior_pattern(self) -> Dict[str, Any]:
        """Generate behavior pattern"""
        return {
            "pattern_type": random.choice(["social_interaction", "work_habits", "leisure_activities"]),
            "frequency": random.uniform(0.3, 0.9),
            "triggers": random.sample(["time_based", "social_cues", "environmental", "emotional"], 2),
            "responses": random.sample(["immediate", "delayed", "adaptive", "planned"], 2),
            "confidence": random.uniform(0.6, 0.9)
        }
    
    def generate_synthetic_data(self, twin_id: str) -> Dict[str, Any]:
        """Generate synthetic data for a specific digital twin"""
        try:
            # Generate comprehensive synthetic data
            synthetic_data = {
                "twin_id": twin_id,
                "personality": self._generate_personality_profile(),
                "health": self._generate_health_metrics(),
                "behavior": self._generate_behavior_pattern(),
                "generated_at": datetime.now().isoformat(),
                "data_quality": random.uniform(0.8, 0.98)
            }
            
            # Add to cache
            if twin_id not in self.data_cache:
                self.data_cache[twin_id] = {}
            self.data_cache[twin_id].update(synthetic_data)
            
            logger.info(f"Generated synthetic data for twin {twin_id}")
            return synthetic_data
            
        except Exception as e:
            logger.error(f"Failed to generate synthetic data for twin {twin_id}: {e}")
            return {
                "twin_id": twin_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def shutdown(self):
        """Shutdown the synthetic data manager"""
        self.is_initialized = False
        logger.info("Synthetic Data Manager shutdown")
