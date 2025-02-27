"""High-level interface for agents to create adaptive cards."""

from typing import Any, Dict, List, Optional, Union

import adaptive_cards.card_types as types
from adaptive_cards.actions import ActionOpenUrl, ActionSubmit
from adaptive_cards.card import AdaptiveCard
from adaptive_cards.elements import Image, TextBlock
from adaptive_cards.validation import CardValidator, CardValidatorFactory, Result


class AgentCardBuilder:
    """Simplified interface for agents to create adaptive cards."""

    def __init__(self, version: str = "1.5"):
        """Initialize the card builder with a default version.
        
        Args:
            version: The version of the adaptive card schema to use.
        """
        self.version = version
        self.validator = CardValidatorFactory.create_validator_microsoft_teams()

    def create_basic_card(
        self, 
        title: str, 
        message: str, 
        image_url: Optional[str] = None
    ) -> AdaptiveCard:
        """Create a simple card with title, message and optional image.
        
        Args:
            title: The card title.
            message: The main message content.
            image_url: Optional URL for an image to display.
            
        Returns:
            An AdaptiveCard instance.
        """
        card = AdaptiveCard.new().version(self.version)
        
        # Add title
        card.add_item(TextBlock(
            text=title,
            size=types.FontSize.LARGE,
            weight=types.FontWeight.BOLDER
        ))
        
        # Add message
        card.add_item(TextBlock(
            text=message,
            wrap=True
        ))
        
        # Add image if provided
        if image_url:
            card.add_item(Image(url=image_url))
            
        return card.create()
    
    def create_action_card(
        self, 
        title: str, 
        message: str, 
        actions: List[Dict[str, Any]],
        image_url: Optional[str] = None
    ) -> AdaptiveCard:
        """Create a card with title, message and action buttons.
        
        Args:
            title: The card title.
            message: The main message content.
            actions: List of action dictionaries, each with at least "type" and "title" keys.
                For ActionOpenUrl, include a "url" key.
                For ActionSubmit, include an optional "data" dictionary.
            image_url: Optional URL for an image to display.
            
        Returns:
            An AdaptiveCard instance with actions.
        """
        # Start with a basic card
        card = self.create_basic_card(title, message, image_url)
        action_items = []
        
        # Add each action
        for action in actions:
            if action["type"] == "open_url":
                action_items.append(ActionOpenUrl(
                    title=action["title"],
                    url=action["url"]
                ))
            elif action["type"] == "submit":
                action_items.append(ActionSubmit(
                    title=action["title"],
                    data=action.get("data", {})
                ))
                
        # Set the actions on the card
        card.actions = action_items
        return card
    
    def validate_card(self, card: AdaptiveCard) -> Dict[str, Any]:
        """Validate a card against the Microsoft Teams schema.
        
        Args:
            card: The AdaptiveCard to validate.
            
        Returns:
            A dictionary with validation results:
                "valid": Boolean indicating if validation passed
                "details": List of validation failure details (if any)
                "size": The card size in KB
        """
        result = self.validator.validate(card)
        card_size = self.validator.card_size(card)
        
        return {
            "valid": result == Result.SUCCESS,
            "details": [finding.failure.value for finding in self.validator.details()],
            "size": card_size
        }
    
    def get_json(self, card: AdaptiveCard) -> str:
        """Get the JSON representation of a card.
        
        Args:
            card: The AdaptiveCard to convert to JSON.
            
        Returns:
            JSON string representation of the card.
        """
        return card.to_json()