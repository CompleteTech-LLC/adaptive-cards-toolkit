"""Adaptive Cards Toolkit - A high-level library for creating, validating, and delivering adaptive cards."""

__version__ = '0.1.0'

# Core components
from .core import (
    AgentCardBuilder, 
    ElementFactory,
    LayoutHelper,
    DataConnector,
    ValidationUtility,
)

# Templates
from .templates import TemplateFactory

# Delivery
from .delivery import DeliveryManager

# Integrations
from .integrations import AdaptiveCardGenerator

__all__ = [
    # Core
    'AgentCardBuilder',
    'ElementFactory',
    'LayoutHelper',
    'DataConnector',
    'ValidationUtility',
    
    # Templates
    'TemplateFactory',
    
    # Delivery
    'DeliveryManager',
    
    # Integrations
    'AdaptiveCardGenerator',
]
