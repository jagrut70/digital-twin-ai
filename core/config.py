"""
Configuration settings for the Digital Twin System
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    WORKERS: int = Field(default=4, env="WORKERS")
    RELOAD: bool = Field(default=False, env="RELOAD")
    
    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite:///./digital_twin.db",
        env="DATABASE_URL"
    )
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # AI/ML settings
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, env="HUGGINGFACE_API_KEY")
    MODEL_CACHE_DIR: str = Field(default="./models", env="MODEL_CACHE_DIR")
    USE_GPU: bool = Field(default=False, env="USE_GPU")
    MODEL_DEVICE: str = Field(default="cpu", env="MODEL_DEVICE")
    
    # Synthetic data settings
    SYNTHETIC_DATA_PATH: str = Field(
        default="./data/synthetic",
        env="SYNTHETIC_DATA_PATH"
    )
    SYNBODY_DATASET_PATH: str = Field(
        default="./data/synbody",
        env="SYNBODY_DATASET_PATH"
    )
    ARIA_DATASET_PATH: str = Field(
        default="./data/aria",
        env="ARIA_DATASET_PATH"
    )
    SIPHER_DATASET_PATH: str = Field(
        default="./data/sipher",
        env="SIPHER_DATASET_PATH"
    )
    SYNTHETIC_DATA_ENABLED: bool = Field(default=True, env="SYNTHETIC_DATA_ENABLED")
    SYNTHETIC_DATA_UPDATE_INTERVAL: int = Field(default=3600, env="SYNTHETIC_DATA_UPDATE_INTERVAL")
    
    # Security settings
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # 3D Visualization settings
    UNITY_BUILD_PATH: str = Field(
        default="./visualization/unity_builds",
        env="UNITY_BUILD_PATH"
    )
    VISUALIZATION_ENGINE: str = Field(default="plotly", env="VISUALIZATION_ENGINE")
    PLOTLY_THEME: str = Field(default="plotly_dark", env="PLOTLY_THEME")
    VISUALIZATION_EXPORT_PATH: str = Field(
        default="./visualization/exports",
        env="VISUALIZATION_EXPORT_PATH"
    )
    
    # Health monitoring settings
    HEALTH_UPDATE_INTERVAL: int = Field(default=60, env="HEALTH_UPDATE_INTERVAL")
    BIOMETRIC_SAMPLING_RATE: int = Field(default=100, env="BIOMETRIC_SAMPLING_RATE")
    HEALTH_CHECK_INTERVAL: int = Field(default=300, env="HEALTH_CHECK_INTERVAL")
    HEALTH_ALERT_THRESHOLD: float = Field(default=0.8, env="HEALTH_ALERT_THRESHOLD")
    
    # Behavior simulation settings
    PERSONALITY_UPDATE_INTERVAL: int = Field(default=300, env="PERSONALITY_UPDATE_INTERVAL")
    DECISION_MAKING_THRESHOLD: float = Field(default=0.7, env="DECISION_MAKING_THRESHOLD")
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="./logs/digital_twin.log", env="LOG_FILE")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # Performance settings
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    REQUEST_TIMEOUT: int = Field(default=30, env="REQUEST_TIMEOUT")
    CACHE_TTL: int = Field(default=3600, env="CACHE_TTL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Ensure required directories exist
os.makedirs(settings.SYNTHETIC_DATA_PATH, exist_ok=True)
os.makedirs(settings.SYNBODY_DATASET_PATH, exist_ok=True)
os.makedirs(settings.ARIA_DATASET_PATH, exist_ok=True)
os.makedirs(settings.SIPHER_DATASET_PATH, exist_ok=True)
os.makedirs(settings.UNITY_BUILD_PATH, exist_ok=True)
os.makedirs(settings.VISUALIZATION_EXPORT_PATH, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
