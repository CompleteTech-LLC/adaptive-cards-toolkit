"""Manage the delivery of adaptive cards to various platforms."""

from typing import Any, Dict, List, Optional, Union

from requests import Response

from adaptive_cards.card import AdaptiveCard
from adaptive_cards.client import TeamsClient
from adaptive_cards_toolkit.core.validation_utility import ValidationUtility


class DeliveryManager:
    """Manage the delivery of adaptive cards to various platforms."""
    
    def __init__(self, webhook_url: Optional[str] = None, platform: str = "teams"):
        """Initialize the delivery manager.
        
        Args:
            webhook_url: Optional webhook URL for the target platform.
            platform: Target platform (currently only "teams" is supported).
        """
        self.platform = platform.lower()
        self.webhook_url = webhook_url
        self.validation_utility = ValidationUtility(target=platform)
        
        # Initialize client if webhook_url is provided
        self.client = None
        if webhook_url:
            self._initialize_client()
            
    def _initialize_client(self) -> None:
        """Initialize the appropriate client based on the platform."""
        if self.platform == "teams":
            self.client = TeamsClient(self.webhook_url)
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")
            
    def set_webhook_url(self, webhook_url: str) -> None:
        """Set or update the webhook URL.
        
        Args:
            webhook_url: The new webhook URL.
        """
        self.webhook_url = webhook_url
        self._initialize_client()
        
    def validate_before_send(self, card: AdaptiveCard) -> Dict[str, Any]:
        """Validate a card before sending it.
        
        Args:
            card: The AdaptiveCard to validate.
            
        Returns:
            A dictionary with validation results.
        """
        return self.validation_utility.validate(card)
        
    def send(
        self, 
        card: AdaptiveCard, 
        validate: bool = True
    ) -> Dict[str, Any]:
        """Send a card to the target platform.
        
        Args:
            card: The AdaptiveCard to send.
            validate: Whether to validate the card before sending.
            
        Returns:
            A dictionary with delivery results:
                "success": Boolean indicating if delivery was successful
                "status_code": HTTP status code from the response
                "message": Success or error message
                "validation": Validation results (if validate=True)
        """
        if not self.client:
            return {
                "success": False,
                "status_code": None,
                "message": "No webhook URL configured. Use set_webhook_url() first."
            }
            
        result = {}
        
        # Validate if requested
        if validate:
            validation_result = self.validate_before_send(card)
            result["validation"] = validation_result
            
            # Don't send if validation failed
            if not validation_result["valid"]:
                result["success"] = False
                result["message"] = "Card validation failed. See validation details."
                return result
        
        # Send the card
        try:
            response: Response = self.client.send(card)
            
            # Process response
            result["success"] = 200 <= response.status_code < 300
            result["status_code"] = response.status_code
            
            if result["success"]:
                result["message"] = "Card delivered successfully"
            else:
                result["message"] = f"Delivery failed: {response.text}"
                
        except Exception as e:
            result["success"] = False
            result["message"] = f"Error delivering card: {str(e)}"
            
        return result
    
    def get_delivery_status(self, delivery_id: str) -> Dict[str, Any]:
        """Get the status of a previous delivery.
        
        Args:
            delivery_id: The ID of the delivery to check.
            
        Returns:
            A dictionary with delivery status (platform-dependent).
        """
        # This is a placeholder for future implementation
        # Most webhook implementations don't provide status tracking
        return {
            "message": "Delivery status tracking is not currently supported by the target platform"
        }