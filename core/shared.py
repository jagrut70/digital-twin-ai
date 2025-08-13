"""
Shared components for the Digital Twin System
"""

from typing import Optional
from core.digital_twin_engine import DigitalTwinEngine

# Global digital twin engine instance
digital_twin_engine: Optional[DigitalTwinEngine] = None

def set_engine(engine: DigitalTwinEngine):
    """Set the global engine instance"""
    global digital_twin_engine
    digital_twin_engine = engine

def get_engine() -> Optional[DigitalTwinEngine]:
    """Get the global engine instance"""
    return digital_twin_engine
