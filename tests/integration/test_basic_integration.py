"""Integration tests for adaptive-cards-toolkit."""

import pytest
from adaptive_cards_toolkit import (
    AgentCardBuilder,
    ElementFactory,
    ValidationUtility
)

def test_basic_card_creation_flow():
    """Test creating a basic card and validating it."""
    # Create a card builder
    builder = AgentCardBuilder()
    
    # Create a simple card
    card = builder.create_basic_card(
        title="Test Card",
        message="This is a test card.",
        image_url="https://example.com/image.png"
    )
    
    # Validate the card
    validator = ValidationUtility()
    result = validator.validate(card)
    
    # Check that the validation succeeded
    assert result["valid"] is True
    assert result["size"] > 0
    
    # Check that card contains expected elements
    card_json = card.to_json()
    assert "Test Card" in card_json
    assert "This is a test card." in card_json
    assert "https://example.com/image.png" in card_json
