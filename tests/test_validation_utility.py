"""Tests for the ValidationUtility class."""

import unittest
from unittest.mock import MagicMock, patch

from adaptive_cards.card import AdaptiveCard
from adaptive_cards.validation import Result, ValidationFailure
from adaptive_cards_toolkit.core.validation_utility import ValidationUtility
from adaptive_cards_toolkit.templates.templates import TemplateFactory


class TestValidationUtility(unittest.TestCase):
    """Test cases for the ValidationUtility class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = ValidationUtility()
        
        # Create a mock validator for testing
        mock_validator = MagicMock()
        mock_validator.validate.return_value = Result.SUCCESS
        mock_validator.card_size.return_value = 10.0
        mock_validator.details.return_value = []
        
        # Apply the mock to the ValidationUtility instance
        self.validator.validator = mock_validator
        
        # Create a test card
        self.test_card = TemplateFactory.create_notification_card(
            title="Test Card",
            message="This is a test card for validation"
        )
    
    def test_initialization(self):
        """Test initialization with different target platforms."""
        # Test default initialization (teams)
        validator = ValidationUtility()
        self.assertEqual(validator.target, "teams")
        
        # Test with custom target
        validator_custom = ValidationUtility(target="other")
        self.assertEqual(validator_custom.target, "other")
    
    def test_validate_successful(self):
        """Test card validation that succeeds."""
        # Set up mock validator to return success
        self.validator.validator.validate.return_value = Result.SUCCESS
        self.validator.validator.details.return_value = []
        
        # Clear any pre-existing warnings or suggestions
        self.test_card.body = [MagicMock(id="test-id")]
        
        # Validate a card
        result = self.validator.validate(self.test_card)
        
        # Check result
        self.assertTrue(result["valid"])
        self.assertEqual(result["size"], 10.0)
        self.assertEqual(result["size_limit"], 28)
        self.assertEqual(len(result["details"]), 0)
        # Don't strictly test the warnings count as it may vary based on implementation
        self.assertEqual(len(result["suggestions"]), 0)
    
    def test_validate_failure(self):
        """Test card validation that fails."""
        # Create a mock finding for empty card
        mock_finding = MagicMock()
        mock_finding.failure = ValidationFailure.EMPTY_CARD
        
        # Set up mock validator to return failure
        self.validator.validator.validate.return_value = Result.FAILURE
        self.validator.validator.details.return_value = [mock_finding]
        
        # Validate a card
        result = self.validator.validate(self.test_card)
        
        # Check result
        self.assertFalse(result["valid"])
        self.assertEqual(result["details"], ["card body is empty"])
        self.assertGreater(len(result["suggestions"]), 0)
        self.assertIn("Card body is empty", result["suggestions"][0])
    
    def test_validate_with_size_warning(self):
        """Test validation with card size approaching limit."""
        # Set up mock validator to return success but with large size
        self.validator.validator.validate.return_value = Result.SUCCESS
        self.validator.validator.card_size.return_value = 25.0  # Just under the 28KB limit
        
        # Validate a card
        result = self.validator.validate(self.test_card)
        
        # Check result
        self.assertTrue(result["valid"])
        self.assertEqual(result["size"], 25.0)
        # At least one warning should be about the size
        size_warning = False
        for warning in result["warnings"]:
            if "approaching the limit" in warning:
                size_warning = True
                break
        self.assertTrue(size_warning, "No warning about size approaching limit")
    
    def test_get_size(self):
        """Test getting the size of a card."""
        # Set mock size value
        self.validator.validator.card_size.return_value = 15.5
        
        # Get card size
        size = self.validator.get_size(self.test_card)
        
        # Check result
        self.assertEqual(size, 15.5)
        self.validator.validator.card_size.assert_called_once_with(self.test_card)
    
    def test_suggest_optimizations(self):
        """Test suggesting optimizations for a card."""
        # Set up mock validator to return a large size
        self.validator.validator.card_size.return_value = 22.0  # > 70% of the 28KB limit
        
        # Create a test card with many elements (mock the body property)
        self.test_card.body = [MagicMock() for _ in range(15)]
        
        # Get optimization suggestions
        suggestions = self.validator.suggest_optimizations(self.test_card)
        
        # Check results
        self.assertGreater(len(suggestions), 0)
        self.assertIn("Card size", suggestions[0])
        self.assertIn("Consider reducing the number of elements", suggestions[1])
        

if __name__ == "__main__":
    unittest.main()