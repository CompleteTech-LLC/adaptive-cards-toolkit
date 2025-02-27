"""Tests for the DeliveryManager class."""

import unittest
from unittest.mock import MagicMock, patch

from requests import Response

from adaptive_cards.card import AdaptiveCard
from adaptive_cards_toolkit.delivery.delivery_manager import DeliveryManager
from adaptive_cards_toolkit.templates.templates import TemplateFactory


class TestDeliveryManager(unittest.TestCase):
    """Test cases for the DeliveryManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock TeamsClient
        self.mock_client = MagicMock()
        
        # Create a test webhook URL
        self.webhook_url = "https://example.com/webhook"
        
        # Create a test card
        self.test_card = TemplateFactory.create_notification_card(
            title="Test Card",
            message="This is a test card for delivery"
        )
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    def test_initialization(self, mock_teams_client):
        """Test initialization with webhook URL."""
        # Set up mock
        mock_teams_instance = MagicMock()
        mock_teams_client.return_value = mock_teams_instance
        
        # Initialize with URL
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Check initialization
        self.assertEqual(manager.platform, "teams")
        self.assertEqual(manager.webhook_url, self.webhook_url)
        mock_teams_client.assert_called_once_with(self.webhook_url)
        
        # Initialize without URL
        manager_no_url = DeliveryManager()
        self.assertIsNone(manager_no_url.client)
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    def test_set_webhook_url(self, mock_teams_client):
        """Test setting the webhook URL."""
        # Set up mock
        mock_teams_instance = MagicMock()
        mock_teams_client.return_value = mock_teams_instance
        
        # Initialize without URL
        manager = DeliveryManager()
        self.assertIsNone(manager.client)
        
        # Set URL later
        manager.set_webhook_url(self.webhook_url)
        self.assertEqual(manager.webhook_url, self.webhook_url)
        mock_teams_client.assert_called_once_with(self.webhook_url)
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.ValidationUtility')
    def test_validate_before_send(self, mock_validation_utility, mock_teams_client):
        """Test validating a card before sending."""
        # Set up mocks
        mock_validator = MagicMock()
        mock_validation_result = {"valid": True, "size": 10.0}
        mock_validator.validate.return_value = mock_validation_result
        mock_validation_utility.return_value = mock_validator
        
        # Initialize manager
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Validate a card
        result = manager.validate_before_send(self.test_card)
        
        # Check result
        self.assertEqual(result, mock_validation_result)
        mock_validator.validate.assert_called_once_with(self.test_card)
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.ValidationUtility')
    def test_send_with_validation_success(self, mock_validation_utility, mock_teams_client):
        """Test sending a card with successful validation."""
        # Set up validation mock
        mock_validator = MagicMock()
        mock_validator.validate.return_value = {"valid": True}
        mock_validation_utility.return_value = mock_validator
        
        # Set up client mock
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_teams_instance = MagicMock()
        mock_teams_instance.send.return_value = mock_response
        mock_teams_client.return_value = mock_teams_instance
        
        # Initialize manager
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Send card with validation
        result = manager.send(self.test_card, validate=True)
        
        # Check result
        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertIn("validation", result)
        mock_validator.validate.assert_called_once_with(self.test_card)
        mock_teams_instance.send.assert_called_once_with(self.test_card)
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.ValidationUtility')
    def test_send_with_validation_failure(self, mock_validation_utility, mock_teams_client):
        """Test sending a card with failed validation."""
        # Set up validation mock
        mock_validator = MagicMock()
        mock_validator.validate.return_value = {"valid": False, "details": ["error"]}
        mock_validation_utility.return_value = mock_validator
        
        # Set up client mock (should not be called)
        mock_teams_instance = MagicMock()
        mock_teams_client.return_value = mock_teams_instance
        
        # Initialize manager
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Send card with validation that fails
        result = manager.send(self.test_card, validate=True)
        
        # Check result
        self.assertFalse(result["success"])
        self.assertIn("validation", result)
        self.assertIn("Card validation failed", result["message"])
        mock_teams_instance.send.assert_not_called()
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    def test_send_without_validation(self, mock_teams_client):
        """Test sending a card without validation."""
        # Set up client mock
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_teams_instance = MagicMock()
        mock_teams_instance.send.return_value = mock_response
        mock_teams_client.return_value = mock_teams_instance
        
        # Initialize manager
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Send card without validation
        result = manager.send(self.test_card, validate=False)
        
        # Check result
        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)
        self.assertNotIn("validation", result)
        mock_teams_instance.send.assert_called_once_with(self.test_card)
    
    @patch('adaptive_cards_toolkit.delivery.delivery_manager.TeamsClient')
    def test_send_error_handling(self, mock_teams_client):
        """Test error handling when sending a card."""
        # Set up client mock to raise an exception
        mock_teams_instance = MagicMock()
        mock_teams_instance.send.side_effect = Exception("Network error")
        mock_teams_client.return_value = mock_teams_instance
        
        # Initialize manager
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Send card with exception
        result = manager.send(self.test_card, validate=False)
        
        # Check result
        self.assertFalse(result["success"])
        self.assertIn("Error delivering card", result["message"])
    
    def test_send_without_client(self):
        """Test sending without a client configured."""
        # Initialize manager without webhook URL
        manager = DeliveryManager()
        
        # Try to send without setting URL
        result = manager.send(self.test_card)
        
        # Check result
        self.assertFalse(result["success"])
        self.assertIn("No webhook URL configured", result["message"])
    
    def test_get_delivery_status(self):
        """Test getting delivery status."""
        # Initialize manager
        manager = DeliveryManager(webhook_url=self.webhook_url)
        
        # Get status
        result = manager.get_delivery_status("test-id")
        
        # This is a placeholder method, should return a message
        self.assertIn("message", result)
        self.assertIn("not currently supported", result["message"])


if __name__ == "__main__":
    unittest.main()