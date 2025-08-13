"""
Health Monitor for Digital Twins
Handles health metrics, biometric data, and health trend analysis
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
class BiometricReading:
    """Individual biometric reading"""
    timestamp: datetime
    heart_rate: float
    blood_pressure_systolic: int
    blood_pressure_diastolic: int
    temperature: float
    oxygen_saturation: float
    respiratory_rate: float
    stress_level: float
    energy_level: float
    sleep_quality: float

@dataclass
class HealthAlert:
    """Health alert information"""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    metrics: Dict[str, Any]
    recommendations: List[str]

@dataclass
class HealthTrend:
    """Health trend analysis"""
    metric_name: str
    trend_direction: str  # "improving", "stable", "declining"
    change_rate: float
    confidence: float
    time_period: str
    factors: List[str]

class HealthMonitor:
    """Monitors and analyzes health metrics for digital twins"""
    
    def __init__(self):
        self.biometric_history: List[BiometricReading] = []
        self.health_alerts: List[HealthAlert] = []
        self.health_trends: List[HealthTrend] = []
        self.alert_thresholds = {
            "heart_rate": {"low": 50, "high": 100},
            "blood_pressure_systolic": {"low": 90, "high": 140},
            "blood_pressure_diastolic": {"low": 60, "high": 90},
            "temperature": {"low": 97.0, "high": 99.0},
            "oxygen_saturation": {"low": 95.0, "high": 100.0},
            "stress_level": {"low": 0.0, "high": 0.8}
        }
        
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the health monitor"""
        try:
            # Load health configurations and thresholds
            await self._load_health_configs()
            
            # Initialize baseline health metrics
            await self._initialize_baseline_metrics()
            
            self.is_initialized = True
            logger.info("Health Monitor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Health Monitor: {e}")
            raise
    
    async def _load_health_configs(self):
        """Load health monitoring configurations"""
        # This could load from files, databases, or external APIs
        pass
    
    async def _initialize_baseline_metrics(self):
        """Initialize baseline health metrics"""
        baseline_reading = BiometricReading(
            timestamp=datetime.now(),
            heart_rate=72.0,
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80,
            temperature=98.6,
            oxygen_saturation=98.0,
            respiratory_rate=16.0,
            stress_level=0.3,
            energy_level=0.8,
            sleep_quality=0.7
        )
        
        self.biometric_history.append(baseline_reading)
    
    def generate_biometric_reading(self, age: int, gender: str, activity_level: str, time_of_day: str) -> BiometricReading:
        """Generate synthetic biometric reading based on demographics and context"""
        # Base values
        base_heart_rate = 72.0
        base_systolic = 120
        base_diastolic = 80
        base_temperature = 98.6
        base_oxygen = 98.0
        base_respiratory = 16.0
        
        # Age adjustments
        if age < 25:
            base_heart_rate += random.uniform(-5, 5)
            base_systolic += random.uniform(-10, 10)
        elif age > 50:
            base_heart_rate += random.uniform(-3, 3)
            base_systolic += random.uniform(5, 20)
        
        # Gender adjustments
        if gender == "female":
            base_heart_rate += random.uniform(2, 8)
            base_systolic += random.uniform(-5, 5)
        
        # Activity level adjustments
        if activity_level == "high":
            base_heart_rate += random.uniform(10, 30)
            base_systolic += random.uniform(10, 25)
            base_temperature += random.uniform(0.5, 1.5)
        elif activity_level == "low":
            base_heart_rate += random.uniform(-5, 5)
            base_temperature += random.uniform(-0.5, 0.5)
        
        # Time of day adjustments
        if time_of_day == "morning":
            base_heart_rate += random.uniform(-3, 3)
            base_oxygen += random.uniform(0.5, 1.0)
        elif time_of_day == "night":
            base_heart_rate += random.uniform(-5, 2)
            base_temperature += random.uniform(-0.5, 0.2)
        
        # Add realistic variation
        heart_rate = max(50, min(120, base_heart_rate + random.uniform(-5, 5)))
        systolic = max(90, min(160, base_systolic + random.uniform(-8, 8)))
        diastolic = max(60, min(100, base_diastolic + random.uniform(-5, 5)))
        temperature = max(97.0, min(100.0, base_temperature + random.uniform(-0.3, 0.3)))
        oxygen = max(95.0, min(100.0, base_oxygen + random.uniform(-1.0, 1.0)))
        respiratory = max(12, min(20, base_respiratory + random.uniform(-2, 2)))
        
        # Generate derived metrics
        stress_level = self._calculate_stress_level(heart_rate, systolic, diastolic, time_of_day)
        energy_level = self._calculate_energy_level(heart_rate, oxygen, time_of_day, activity_level)
        sleep_quality = self._calculate_sleep_quality(time_of_day, stress_level, energy_level)
        
        return BiometricReading(
            timestamp=datetime.now(),
            heart_rate=heart_rate,
            blood_pressure_systolic=systolic,
            blood_pressure_diastolic=diastolic,
            temperature=temperature,
            oxygen_saturation=oxygen,
            respiratory_rate=respiratory,
            stress_level=stress_level,
            energy_level=energy_level,
            sleep_quality=sleep_quality
        )
    
    def _calculate_stress_level(self, heart_rate: float, systolic: int, diastolic: int, time_of_day: str) -> float:
        """Calculate stress level based on biometric indicators"""
        stress_score = 0.0
        
        # Heart rate stress indicator
        if heart_rate > 90:
            stress_score += 0.3
        elif heart_rate > 80:
            stress_score += 0.2
        
        # Blood pressure stress indicator
        if systolic > 130 or diastolic > 85:
            stress_score += 0.3
        elif systolic > 120 or diastolic > 80:
            stress_score += 0.1
        
        # Time of day stress factors
        if time_of_day in ["morning", "evening"]:
            stress_score += 0.1  # Rush hour stress
        
        return min(1.0, stress_score + random.uniform(-0.1, 0.1))
    
    def _calculate_energy_level(self, heart_rate: float, oxygen: float, time_of_day: str, activity_level: str) -> float:
        """Calculate energy level based on biometric indicators"""
        energy_score = 0.8
        
        # Oxygen saturation effect
        if oxygen < 96:
            energy_score -= 0.2
        elif oxygen > 99:
            energy_score += 0.1
        
        # Heart rate effect (moderate is good)
        if 60 <= heart_rate <= 80:
            energy_score += 0.1
        elif heart_rate > 100:
            energy_score -= 0.2
        
        # Time of day effect
        if time_of_day == "morning":
            energy_score += 0.1
        elif time_of_day == "afternoon":
            energy_score += 0.05
        elif time_of_day == "evening":
            energy_score -= 0.1
        elif time_of_day == "night":
            energy_score -= 0.3
        
        # Activity level effect
        if activity_level == "high":
            energy_score -= 0.2  # Tired after activity
        elif activity_level == "low":
            energy_score += 0.1  # Rested
        
        return max(0.1, min(1.0, energy_score + random.uniform(-0.1, 0.1)))
    
    def _calculate_sleep_quality(self, time_of_day: str, stress_level: float, energy_level: float) -> float:
        """Calculate sleep quality based on context"""
        sleep_score = 0.7
        
        # Stress affects sleep
        if stress_level > 0.7:
            sleep_score -= 0.3
        elif stress_level < 0.3:
            sleep_score += 0.2
        
        # Energy level affects sleep
        if energy_level < 0.4:
            sleep_score += 0.2  # Tired, likely to sleep well
        elif energy_level > 0.8:
            sleep_score -= 0.1  # High energy, might affect sleep
        
        # Time of day affects sleep quality
        if time_of_day == "night":
            sleep_score += 0.1  # Natural sleep time
        elif time_of_day == "morning":
            sleep_score -= 0.2  # Just woke up
        
        return max(0.1, min(1.0, sleep_score + random.uniform(-0.1, 0.1)))
    
    async def update_health_metrics(self, twin_id: str, context: Dict[str, Any]) -> BiometricReading:
        """Update health metrics for a digital twin"""
        try:
            # Generate new biometric reading
            age = context.get("age", 25)
            gender = context.get("gender", "unspecified")
            activity_level = context.get("activity_level", "moderate")
            time_of_day = context.get("time_of_day", "afternoon")
            
            new_reading = self.generate_biometric_reading(age, gender, activity_level, time_of_day)
            
            # Add to history
            self.biometric_history.append(new_reading)
            
            # Check for health alerts
            await self._check_health_alerts(new_reading, twin_id)
            
            # Update health trends
            await self._update_health_trends()
            
            logger.info(f"Updated health metrics for twin {twin_id}")
            return new_reading
            
        except Exception as e:
            logger.error(f"Failed to update health metrics for twin {twin_id}: {e}")
            raise
    
    async def _check_health_alerts(self, reading: BiometricReading, twin_id: str):
        """Check for health alerts based on biometric readings"""
        alerts = []
        
        # Check heart rate
        if reading.heart_rate < self.alert_thresholds["heart_rate"]["low"]:
            alerts.append(HealthAlert(
                alert_id=f"alert_{len(self.health_alerts) + 1}",
                alert_type="low_heart_rate",
                severity="moderate",
                message=f"Low heart rate detected: {reading.heart_rate} bpm",
                timestamp=reading.timestamp,
                metrics={"heart_rate": reading.heart_rate},
                recommendations=["Consider light exercise", "Check for underlying conditions"]
            ))
        elif reading.heart_rate > self.alert_thresholds["heart_rate"]["high"]:
            alerts.append(HealthAlert(
                alert_id=f"alert_{len(self.health_alerts) + 1}",
                alert_type="high_heart_rate",
                severity="moderate",
                message=f"Elevated heart rate detected: {reading.heart_rate} bpm",
                timestamp=reading.timestamp,
                metrics={"heart_rate": reading.heart_rate},
                recommendations=["Rest and relax", "Consider stress management techniques"]
            ))
        
        # Check blood pressure
        if reading.blood_pressure_systolic > self.alert_thresholds["blood_pressure_systolic"]["high"]:
            alerts.append(HealthAlert(
                alert_id=f"alert_{len(self.health_alerts) + 1}",
                alert_type="high_blood_pressure",
                severity="high",
                message=f"High blood pressure detected: {reading.blood_pressure_systolic}/{reading.blood_pressure_diastolic}",
                timestamp=reading.timestamp,
                metrics={"systolic": reading.blood_pressure_systolic, "diastolic": reading.blood_pressure_diastolic},
                recommendations=["Monitor regularly", "Consider lifestyle changes", "Consult healthcare provider"]
            ))
        
        # Check stress level
        if reading.stress_level > self.alert_thresholds["stress_level"]["high"]:
            alerts.append(HealthAlert(
                alert_id=f"alert_{len(self.health_alerts) + 1}",
                alert_type="high_stress",
                severity="moderate",
                message=f"High stress level detected: {reading.stress_level:.2f}",
                timestamp=reading.timestamp,
                metrics={"stress_level": reading.stress_level},
                recommendations=["Practice relaxation techniques", "Take breaks", "Consider stress management"]
            ))
        
        # Add new alerts
        self.health_alerts.extend(alerts)
        
        if alerts:
            logger.info(f"Generated {len(alerts)} health alerts for twin {twin_id}")
    
    async def _update_health_trends(self):
        """Update health trend analysis"""
        if len(self.biometric_history) < 3:
            return
        
        # Analyze trends for each metric
        metrics = ["heart_rate", "blood_pressure_systolic", "blood_pressure_diastolic", 
                  "temperature", "oxygen_saturation", "stress_level", "energy_level"]
        
        for metric in metrics:
            recent_readings = [getattr(reading, metric) for reading in self.biometric_history[-5:]]
            
            if len(recent_readings) >= 3:
                trend = self._analyze_trend(recent_readings, metric)
                if trend:
                    self.health_trends.append(trend)
    
    def _analyze_trend(self, values: List[float], metric_name: str) -> Optional[HealthTrend]:
        """Analyze trend in a series of values"""
        if len(values) < 3:
            return None
        
        # Calculate change rate
        change_rate = (values[-1] - values[0]) / len(values)
        
        # Determine trend direction
        if abs(change_rate) < 0.01:  # Threshold for "stable"
            trend_direction = "stable"
        elif change_rate > 0:
            trend_direction = "improving" if metric_name in ["energy_level", "sleep_quality", "oxygen_saturation"] else "declining"
        else:
            trend_direction = "declining" if metric_name in ["energy_level", "sleep_quality", "oxygen_saturation"] else "improving"
        
        # Calculate confidence based on consistency
        variance = np.var(values)
        confidence = max(0.1, min(1.0, 1.0 - variance / 100))
        
        return HealthTrend(
            metric_name=metric_name,
            trend_direction=trend_direction,
            change_rate=change_rate,
            confidence=confidence,
            time_period="recent",
            factors=["biometric_variation", "lifestyle_changes"]
        )
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get a summary of current health status"""
        if not self.biometric_history:
            return {"status": "no_data"}
        
        latest = self.biometric_history[-1]
        
        return {
            "status": "healthy",
            "latest_reading": {
                "timestamp": latest.timestamp.isoformat(),
                "heart_rate": latest.heart_rate,
                "blood_pressure": f"{latest.blood_pressure_systolic}/{latest.blood_pressure_diastolic}",
                "temperature": latest.temperature,
                "oxygen_saturation": latest.oxygen_saturation,
                "stress_level": latest.stress_level,
                "energy_level": latest.energy_level,
                "sleep_quality": latest.sleep_quality
            },
            "alerts_count": len([a for a in self.health_alerts if a.timestamp > datetime.now() - timedelta(hours=24)]),
            "trends_count": len(self.health_trends)
        }
    
    def get_health_alerts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get health alerts from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_alerts = [a for a in self.health_alerts if a.timestamp > cutoff_time]
        
        return [
            {
                "alert_id": alert.alert_id,
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "recommendations": alert.recommendations
            }
            for alert in recent_alerts
        ]
    
    def generate_health_data(self, twin_id: str) -> Dict[str, Any]:
        """Generate synthetic health data for a digital twin"""
        try:
            # Generate realistic biometric readings
            heart_rate = random.uniform(60.0, 100.0)
            blood_pressure_systolic = random.randint(100, 140)
            blood_pressure_diastolic = random.randint(60, 90)
            temperature = random.uniform(97.5, 99.2)
            oxygen_saturation = random.uniform(96.0, 99.5)
            respiratory_rate = random.uniform(12.0, 20.0)
            stress_level = random.uniform(0.1, 0.7)
            energy_level = random.uniform(0.3, 0.9)
            sleep_quality = random.uniform(0.4, 0.95)
            
            health_data = {
                "twin_id": twin_id,
                "timestamp": datetime.now().isoformat(),
                "heart_rate": round(heart_rate, 1),
                "blood_pressure": f"{blood_pressure_systolic}/{blood_pressure_diastolic}",
                "temperature": round(temperature, 1),
                "oxygen_saturation": round(oxygen_saturation, 1),
                "respiratory_rate": round(respiratory_rate, 1),
                "stress_level": round(stress_level, 2),
                "energy_level": round(energy_level, 2),
                "sleep_quality": round(sleep_quality, 2),
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Generated synthetic health data for twin {twin_id}")
            return health_data
            
        except Exception as e:
            logger.error(f"Failed to generate health data: {e}")
            return {
                "twin_id": twin_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_synthetic_baseline(self, age: int, gender: str) -> Dict[str, Any]:
        """Generate a synthetic health baseline for a digital twin"""
        try:
            # Generate baseline health metrics based on age and gender
            if age < 25:
                heart_rate = random.uniform(65.0, 85.0)
                energy_level = random.uniform(0.7, 0.95)
            elif age < 50:
                heart_rate = random.uniform(70.0, 90.0)
                energy_level = random.uniform(0.6, 0.85)
            else:
                heart_rate = random.uniform(75.0, 95.0)
                energy_level = random.uniform(0.5, 0.75)
            
            baseline_health = {
                "heart_rate": round(heart_rate, 1),
                "blood_pressure_systolic": random.randint(100, 140),
                "blood_pressure_diastolic": random.randint(60, 90),
                "temperature": random.uniform(97.5, 99.2),
                "oxygen_saturation": random.uniform(96.0, 99.5),
                "respiratory_rate": random.uniform(12.0, 20.0),
                "stress_level": random.uniform(0.1, 0.6),
                "energy_level": round(energy_level, 2),
                "sleep_quality": random.uniform(0.5, 0.9),
                "age": age,
                "gender": gender,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Generated synthetic health baseline for age {age}, {gender}")
            return baseline_health
            
        except Exception as e:
            logger.error(f"Failed to generate synthetic health baseline: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def generate_synthetic_update(self, current_metrics: Any, personality_traits: Any, time_since_last_update: timedelta) -> Dict[str, Any]:
        """Generate a synthetic health update for a digital twin"""
        try:
            # Generate incremental health changes based on current metrics
            variation = random.uniform(-0.1, 0.1)
            
            # Personality influence on health - handle both dict and dataclass objects
            stress_modifier = 0.0
            if hasattr(personality_traits, 'neuroticism'):
                if personality_traits.neuroticism > 0.7:
                    stress_modifier += 0.1
            elif isinstance(personality_traits, dict) and personality_traits.get("neuroticism", 0.5) > 0.7:
                stress_modifier += 0.1
                
            if hasattr(personality_traits, 'emotional_stability'):
                if personality_traits.emotional_stability < 0.3:
                    stress_modifier += 0.1
            elif isinstance(personality_traits, dict) and personality_traits.get("emotional_stability", 0.5) < 0.3:
                stress_modifier += 0.1
            
            # Time-based health changes
            days_since_update = time_since_last_update.days
            if days_since_update > 1:
                # Daily health variation
                health_update = {
                    "heart_rate": max(50, min(120, 72 + random.uniform(-5, 5) + variation * 10)),
                    "stress_level": max(0.0, min(1.0, 0.3 + stress_modifier + variation)),
                    "energy_level": max(0.0, min(1.0, 0.8 + variation)),
                    "sleep_quality": max(0.0, min(1.0, 0.7 + variation)),
                    "update_type": "synthetic",
                    "update_reason": "background_monitoring",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Hourly health variation
                health_update = {
                    "heart_rate": max(50, min(120, 72 + random.uniform(-3, 3))),
                    "stress_level": max(0.0, min(1.0, 0.3 + stress_modifier + random.uniform(-0.05, 0.05))),
                    "energy_level": max(0.0, min(1.0, 0.8 + random.uniform(-0.1, 0.1))),
                    "update_type": "synthetic",
                    "update_reason": "hourly_monitoring",
                    "timestamp": datetime.now().isoformat()
                }
            
            logger.info(f"Generated synthetic health update based on {days_since_update} days since last update")
            return health_update
            
        except Exception as e:
            logger.error(f"Failed to generate synthetic health update: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def shutdown(self):
        """Shutdown the health monitor"""
        self.is_initialized = False
        logger.info("Health Monitor shutdown complete")
