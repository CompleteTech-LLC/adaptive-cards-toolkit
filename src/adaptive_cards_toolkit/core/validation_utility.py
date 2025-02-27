"""Utility for validating adaptive cards before submission."""

from typing import Any, Dict, List, Optional, Union

from adaptive_cards.card import AdaptiveCard
from adaptive_cards.validation import CardValidator, CardValidatorFactory, Result, ValidationFailure


class ValidationUtility:
    """Utility for validating and optimizing adaptive cards."""
    
    def __init__(self, target: str = "teams"):
        """Initialize the validation utility.
        
        Args:
            target: The target platform for validation (default: "teams").
        """
        self.target = target
        
        if target.lower() == "teams":
            self.validator = CardValidatorFactory.create_validator_microsoft_teams()
        else:
            # Use Teams validator as default
            self.validator = CardValidatorFactory.create_validator_microsoft_teams()
            
    def validate(self, card: AdaptiveCard) -> Dict[str, Any]:
        """Validate a card against the target platform's schema.
        
        Args:
            card: The AdaptiveCard to validate.
            
        Returns:
            A dictionary with validation results:
                "valid": Boolean indicating if validation passed
                "details": List of validation failure details (if any)
                "size": The card size in KB
                "size_limit": The size limit for the target platform in KB
                "warnings": List of warnings (if any)
                "suggestions": List of optimization suggestions (if any)
        """
        # Run validation
        result = self.validator.validate(card)
        card_size = self.validator.card_size(card)
        details = self.validator.details()
        
        # Prepare response
        response = {
            "valid": result == Result.SUCCESS,
            "details": [finding.failure.value for finding in details],
            "size": card_size,
            "size_limit": 28 if self.target.lower() == "teams" else 40,  # Teams webhook limit is 28KB
            "warnings": [],
            "suggestions": []
        }
        
        # Add specific suggestions based on validation findings
        for finding in details:
            if finding.failure == ValidationFailure.EMPTY_CARD:
                response["suggestions"].append(
                    "Card body is empty. Add at least one element to the card."
                )
            elif finding.failure == ValidationFailure.INVALID_FIELD_VERSION:
                response["suggestions"].append(
                    f"Some elements or fields require a newer schema version than '{card.version}'. "
                    f"Consider upgrading the card version or removing incompatible elements."
                )
            elif finding.failure == ValidationFailure.SIZE_LIMIT_EXCEEDED:
                response["suggestions"].extend([
                    "Card size exceeds the limit for the target platform.",
                    "Consider reducing the number of elements or simplifying complex elements.",
                    "Minimize the use of images or use lower resolution images.",
                    "Break content into multiple smaller cards if possible."
                ])
                
        # Add size-related warnings
        size_limit = response["size_limit"]
        if card_size > size_limit * 0.8 and card_size <= size_limit:
            response["warnings"].append(
                f"Card size ({card_size:.2f}KB) is approaching the limit ({size_limit}KB)."
            )
            response["suggestions"].append(
                "Consider optimizing the card to reduce its size."
            )
            
        # Check for common issues even if validation passed
        if not any(item.id for item in card.body or []):
            response["warnings"].append(
                "No elements have IDs, which may limit interactivity and accessibility."
            )
            
        return response
    
    def get_size(self, card: AdaptiveCard) -> float:
        """Get the size of a card in KB.
        
        Args:
            card: The AdaptiveCard to measure.
            
        Returns:
            The card size in KB.
        """
        return self.validator.card_size(card)
    
    def suggest_optimizations(self, card: AdaptiveCard) -> List[str]:
        """Suggest optimizations for a card.
        
        Args:
            card: The AdaptiveCard to optimize.
            
        Returns:
            A list of optimization suggestions.
        """
        suggestions = []
        
        # Check card size
        card_size = self.validator.card_size(card)
        size_limit = 28 if self.target.lower() == "teams" else 40
        
        if card_size > size_limit * 0.7:
            suggestions.append(f"Card size ({card_size:.2f}KB) is {card_size/size_limit*100:.1f}% of the limit.")
            
            # Suggest specific optimizations
            if len(card.body or []) > 10:
                suggestions.append("Consider reducing the number of elements in the card.")
                
            # Check for large images
            image_count = sum(1 for item in card.body or [] if hasattr(item, "url"))
            if image_count > 0:
                suggestions.append(f"Card contains {image_count} images. Consider reducing image count or size.")
                
            # Check for complex nested structures
            container_count = sum(1 for item in card.body or [] if hasattr(item, "items"))
            if container_count > 3:
                suggestions.append(f"Card contains {container_count} containers. Consider simplifying the structure.")
                
        return suggestions