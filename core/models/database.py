"""
Database Models
SQLAlchemy models for the Digital Twin System
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

# Note: Association tables were removed as the current design uses direct relationships
# between DigitalTwin and PersonalityProfile/HealthProfile (one-to-one)

class User(Base):
    """User model for authentication and access control"""
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    digital_twins: Mapped[List["DigitalTwin"]] = relationship("DigitalTwin", back_populates="owner")
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")

class UserSession(Base):
    """User session model for tracking active sessions"""
    __tablename__ = "user_sessions"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")

class DigitalTwin(Base):
    """Digital Twin model for storing twin information"""
    __tablename__ = "digital_twins"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    owner_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    twin_type: Mapped[str] = mapped_column(String(50), default="human")  # human, object, system
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, inactive, archived
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Configuration data
    config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="digital_twins")
    avatar: Mapped[Optional["Avatar"]] = relationship("Avatar", back_populates="digital_twin", uselist=False)
    personality_profile: Mapped[Optional["PersonalityProfile"]] = relationship("PersonalityProfile", back_populates="digital_twin", uselist=False)
    health_profile: Mapped[Optional["HealthProfile"]] = relationship("HealthProfile", back_populates="digital_twin", uselist=False)
    behavior_logs: Mapped[List["BehaviorLog"]] = relationship("BehaviorLog", back_populates="digital_twin")
    conversation_logs: Mapped[List["ConversationLog"]] = relationship("ConversationLog", back_populates="digital_twin")

class Avatar(Base):
    """Avatar model for 3D visualization"""
    __tablename__ = "avatars"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    digital_twin_id: Mapped[str] = mapped_column(String, ForeignKey("digital_twins.id"), nullable=False)
    avatar_type: Mapped[str] = mapped_column(String(50), default="human")  # human, animal, object
    model_path: Mapped[str] = mapped_column(String(255), nullable=False)
    texture_path: Mapped[Optional[str]] = mapped_column(String(255))
    skeleton_path: Mapped[Optional[str]] = mapped_column(String(255))
    
    # Physical attributes
    height: Mapped[float] = mapped_column(Float, default=1.75)
    body_type: Mapped[str] = mapped_column(String(50), default="athletic")
    skin_tone: Mapped[str] = mapped_column(String(50), default="medium")
    hair_style: Mapped[str] = mapped_column(String(50), default="short")
    eye_color: Mapped[str] = mapped_column(String(50), default="brown")
    
    # Visual state
    current_position: Mapped[Optional[Dict[str, float]]] = mapped_column(JSON)  # x, y, z
    current_rotation: Mapped[Optional[Dict[str, float]]] = mapped_column(JSON)  # quaternion
    current_scale: Mapped[Optional[Dict[str, float]]] = mapped_column(JSON)  # x, y, z
    current_animation: Mapped[Optional[str]] = mapped_column(String(100))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    digital_twin: Mapped["DigitalTwin"] = relationship("DigitalTwin", back_populates="avatar")

class PersonalityProfile(Base):
    """Personality profile model for digital twins"""
    __tablename__ = "personality_profiles"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    digital_twin_id: Mapped[str] = mapped_column(String, ForeignKey("digital_twins.id"), nullable=False)
    
    # Big Five personality traits
    openness: Mapped[float] = mapped_column(Float, default=0.5)  # 0.0 to 1.0
    conscientiousness: Mapped[float] = mapped_column(Float, default=0.5)
    extraversion: Mapped[float] = mapped_column(Float, default=0.5)
    agreeableness: Mapped[float] = mapped_column(Float, default=0.5)
    neuroticism: Mapped[float] = mapped_column(Float, default=0.5)
    
    # Additional traits
    creativity: Mapped[float] = mapped_column(Float, default=0.5)
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    empathy: Mapped[float] = mapped_column(Float, default=0.5)
    adaptability: Mapped[float] = mapped_column(Float, default=0.5)
    
    # Interests and preferences
    interests: Mapped[Optional[List[str]]] = mapped_column(JSON)
    communication_style: Mapped[str] = mapped_column(String(50), default="balanced")
    decision_making_style: Mapped[str] = mapped_column(String(50), default="analytical")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    digital_twin: Mapped["DigitalTwin"] = relationship("DigitalTwin", back_populates="personality_profile")

class HealthProfile(Base):
    """Health profile model for digital twins"""
    __tablename__ = "health_profiles"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    digital_twin_id: Mapped[str] = mapped_column(String, ForeignKey("digital_twins.id"), nullable=False)
    
    # Basic health metrics
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Vital signs baseline
    heart_rate_baseline: Mapped[float] = mapped_column(Float, default=70.0)
    blood_pressure_systolic_baseline: Mapped[float] = mapped_column(Float, default=120.0)
    blood_pressure_diastolic_baseline: Mapped[float] = mapped_column(Float, default=80.0)
    temperature_baseline: Mapped[float] = mapped_column(Float, default=98.6)
    oxygen_saturation_baseline: Mapped[float] = mapped_column(Float, default=98.0)
    
    # Health status
    overall_health_score: Mapped[float] = mapped_column(Float, default=0.8)  # 0.0 to 1.0
    energy_level: Mapped[float] = mapped_column(Float, default=0.8)
    stress_level: Mapped[float] = mapped_column(Float, default=0.3)
    sleep_quality: Mapped[float] = mapped_column(Float, default=0.7)
    
    # Medical history
    medical_conditions: Mapped[Optional[List[str]]] = mapped_column(JSON)
    medications: Mapped[Optional[List[str]]] = mapped_column(JSON)
    allergies: Mapped[Optional[List[str]]] = mapped_column(JSON)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    digital_twin: Mapped["DigitalTwin"] = relationship("DigitalTwin", back_populates="health_profile")

class BehaviorLog(Base):
    """Behavior log model for tracking twin behaviors"""
    __tablename__ = "behavior_logs"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    digital_twin_id: Mapped[str] = mapped_column(String, ForeignKey("digital_twins.id"), nullable=False)
    
    behavior_type: Mapped[str] = mapped_column(String(100), nullable=False)  # social, work, health, etc.
    behavior_description: Mapped[str] = mapped_column(Text, nullable=False)
    trigger: Mapped[Optional[str]] = mapped_column(String(200))
    context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    # Behavioral metrics
    intensity: Mapped[float] = mapped_column(Float, default=0.5)  # 0.0 to 1.0
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    success_rate: Mapped[Optional[float]] = mapped_column(Float)  # 0.0 to 1.0
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    digital_twin: Mapped["DigitalTwin"] = relationship("DigitalTwin", back_populates="behavior_logs")

class ConversationLog(Base):
    """Conversation log model for tracking interactions"""
    __tablename__ = "conversation_logs"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    digital_twin_id: Mapped[str] = mapped_column(String, ForeignKey("digital_twins.id"), nullable=False)
    
    conversation_id: Mapped[str] = mapped_column(String, nullable=False)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    twin_response: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Conversation context
    context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    sentiment: Mapped[Optional[str]] = mapped_column(String(50))  # positive, negative, neutral
    intent: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Metadata
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    user_satisfaction: Mapped[Optional[float]] = mapped_column(Float)  # 0.0 to 1.0
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    digital_twin: Mapped["DigitalTwin"] = relationship("DigitalTwin", back_populates="conversation_logs")

class SystemEvent(Base):
    """System event model for tracking system activities"""
    __tablename__ = "system_events"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)  # twin_created, health_update, etc.
    event_description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Event data
    entity_id: Mapped[Optional[str]] = mapped_column(String)  # ID of the entity involved
    entity_type: Mapped[Optional[str]] = mapped_column(String(50))  # user, twin, avatar, etc.
    event_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    # Severity and status
    severity: Mapped[str] = mapped_column(String(20), default="info")  # info, warning, error, critical
    status: Mapped[str] = mapped_column(String(20), default="completed")  # pending, completed, failed
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    # No direct relationships for system events

class SyntheticDataset(Base):
    """Synthetic dataset model for managing generated data"""
    __tablename__ = "synthetic_datasets"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(50), nullable=False)  # personality, health, behavior, etc.
    
    # Dataset metadata
    description: Mapped[Optional[str]] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    source: Mapped[str] = mapped_column(String(100), default="generated")
    
    # Data statistics
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    data_size_bytes: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Dataset configuration
    generation_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    validation_rules: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    
    # Status and lifecycle
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, archived, deprecated
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_generated: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Relationships
    # No direct relationships for synthetic datasets
