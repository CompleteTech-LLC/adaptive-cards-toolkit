# Agent Toolkit for Adaptive Cards

A high-level toolkit designed for AI agents to create, validate, and deliver adaptive cards.

## Overview

The Agent Toolkit provides a simplified interface on top of the `adaptive-cards-py` library, making it easier for AI agents and developers to create, validate, and deliver adaptive cards. Whether you need to programmatically create cards or want to generate them using natural language, this toolkit offers a comprehensive solution.

Key features include:

- **High-level abstractions**: Create complex cards with minimal code
- **Pre-built templates**: Common patterns for notifications, forms, dashboards, etc.
- **Component factories**: Create elements with sensible defaults
- **Layout helpers**: Build responsive designs easily
- **Data visualization**: Convert structured data (JSON, CSV) to cards
- **Validation**: Check cards before delivery to prevent errors
- **Delivery management**: Send cards to platforms like MS Teams
- **OpenAI integration**: Generate cards using natural language

### When to use this toolkit

- **For AI agents**: When you need a high-level API to create cards programmatically
- **For developers**: When you want to simplify adaptive card creation and focus on content
- **For applications**: When you need to generate cards from user input or data sources
- **For prototype development**: When you want to quickly experiment with different card designs

## Installation

```bash
# First, install the adaptive-cards-py base library
pip install adaptive-cards-py

# For OpenAI integration (optional)
pip install openai
```

## Components

The toolkit consists of the following major components:

1. **AgentCardBuilder**: Simplified interface for creating adaptive cards
2. **ElementFactory**: Create card elements with sensible defaults
3. **LayoutHelper**: Build responsive layouts easily
4. **DataConnector**: Convert structured data to card elements
5. **TemplateFactory**: Pre-built templates for common card scenarios
6. **ValidationUtility**: Validate cards before delivery
7. **DeliveryManager**: Send cards to platforms like MS Teams
8. **OpenAI Assistant**: Generate cards using natural language

## Basic Example

```python
from tools.agent_toolkit.templates import TemplateFactory
from tools.agent_toolkit.validation_utility import ValidationUtility
from tools.agent_toolkit.delivery_manager import DeliveryManager

# Create a notification card
card = TemplateFactory.create_notification_card(
    title="System Maintenance",
    message="The system will be down for maintenance on Saturday from 2-4 PM EST.",
    level="warning"
)

# Validate the card
validator = ValidationUtility()
result = validator.validate(card)

if result["valid"]:
    # Send the card
    delivery = DeliveryManager(webhook_url="https://your-webhook-url.com")
    delivery.send(card)
```

## OpenAI Integration Example

```python
from tools.agent_toolkit.openai_agent import AdaptiveCardGenerator

# Initialize with OpenAI API key
generator = AdaptiveCardGenerator(api_key="your-openai-api-key")

# Generate card from natural language
result = generator.generate_card(
    "Create a notification about system maintenance on Saturday from 2-4 PM"
)

if result["success"]:
    card = result["card"]
    print(f"Generated card: {result['explanation']}")
    
    # Send to webhook (optional)
    generator.send_card(card, "https://your-webhook-url.com")
```

## Best Practices

1. **Start with templates** for common scenarios
2. **Validate cards** before sending to ensure compatibility 
3. **Use layout helpers** for responsive designs
4. **Structure data** with DataConnector for clean visualization
5. **Keep cards concise** to avoid size limitations
6. **Add IDs to elements** that need to be referenced or manipulated
7. **Handle delivery errors** gracefully
8. **Optimize image sizes** to reduce card size
9. **Test cards across platforms** to ensure compatibility
10. **Consider using AI generation** for rapid prototyping

## Comprehensive Documentation

For detailed documentation on all components, advanced usage examples, and best practices, see the [Comprehensive Documentation](./docs/README.md).