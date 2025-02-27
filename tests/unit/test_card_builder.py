"""Unit tests for the AgentCardBuilder class."""

import pytest
from adaptive_cards_toolkit.card_builder import AgentCardBuilder
from adaptive_cards.card import AdaptiveCard


class TestAgentCardBuilder:
    """Test cases for the AgentCardBuilder class."""
    
    def test_initialization(self):
        """Test that the builder initializes with default values."""
        builder = AgentCardBuilder()
        assert builder.version == "1.5"
        assert builder.validator is not None
    
    def test_create_basic_card(self):
        """Test creating a basic card with title and message."""
        builder = AgentCardBuilder()
        
        # Create card with required parameters
        card = builder.create_basic_card(
            title="Test Title",
            message="Test Message"
        )
        
        # Check that the card was created correctly
        assert isinstance(card, AdaptiveCard)
        
        # Check card properties
        card_json = card.to_json()
        assert "Test Title" in card_json
        assert "Test Message" in card_json
    
    def test_create_basic_card_with_image(self):
        """Test creating a basic card with an image."""
        builder = AgentCardBuilder()
        
        # Create card with an image
        card = builder.create_basic_card(
            title="Test Title",
            message="Test Message",
            image_url="https://example.com/image.png"
        )
        
        # Check that the image was added
        card_json = card.to_json()
        assert "https://example.com/image.png" in card_json
    
    def test_create_action_card(self):
        """Test creating a card with actions."""
        builder = AgentCardBuilder()
        
        # Create card with actions
        card = builder.create_action_card(
            title="Action Card",
            message="Card with actions",
            actions=[
                {
                    "type": "open_url",
                    "title": "Open URL",
                    "url": "https://example.com"
                },
                {
                    "type": "submit",
                    "title": "Submit",
                    "data": {"key": "value"}
                }
            ]
        )
        
        # Check that the actions were added
        card_json = card.to_json()
        assert "Action Card" in card_json
        assert "Card with actions" in card_json
        assert "Open URL" in card_json
        assert "https://example.com" in card_json
        assert "Submit" in card_json
        
    def test_validate_card(self):
        """Test validating a card."""
        builder = AgentCardBuilder()
        
        # Create a card to validate
        card = builder.create_basic_card(
            title="Test Card",
            message="This is a test card."
        )
        
        # Validate the card
        result = builder.validate_card(card)
        
        # Check the validation result
        assert isinstance(result, dict)
        assert "valid" in result
        assert "details" in result
        assert "size" in result
        assert result["valid"] is True
        assert result["size"] > 0
