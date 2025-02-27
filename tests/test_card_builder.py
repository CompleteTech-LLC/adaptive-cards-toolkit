"""Tests for the AgentCardBuilder class."""

import json
import unittest
from typing import Dict, Any

from adaptive_cards_toolkit.core.card_builder import AgentCardBuilder


class TestAgentCardBuilder(unittest.TestCase):
    """Test cases for the AgentCardBuilder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = AgentCardBuilder(version="1.5")
        
    def test_create_basic_card(self):
        """Test creating a basic card."""
        title = "Test Title"
        message = "Test Message"
        image_url = "https://example.com/image.png"
        
        card = self.builder.create_basic_card(title, message, image_url)
        
        # Convert to JSON for inspection
        card_json = json.loads(card.to_json())
        
        # Basic assertions
        self.assertEqual(card_json["type"], "AdaptiveCard")
        self.assertEqual(card_json["version"], "1.5")
        
        # Check body elements
        self.assertGreaterEqual(len(card_json["body"]), 2)  # At least title and message
        
        # Check title
        title_block = next((item for item in card_json["body"] if item.get("type") == "TextBlock" and "size" in item and item["size"] == "large"), None)
        self.assertIsNotNone(title_block)
        self.assertEqual(title_block["text"], title)
        
        # Check message
        message_block = next((item for item in card_json["body"] if item.get("type") == "TextBlock" and "wrap" in item and item["wrap"] is True), None)
        self.assertIsNotNone(message_block)
        
        # Check image
        image_block = next((item for item in card_json["body"] if item.get("type") == "Image"), None)
        self.assertIsNotNone(image_block)
        self.assertEqual(image_block["url"], image_url)
        
    def test_create_action_card(self):
        """Test creating a card with actions."""
        title = "Action Card"
        message = "Card with actions"
        actions = [
            {
                "type": "open_url",
                "title": "Open URL",
                "url": "https://example.com"
            },
            {
                "type": "submit",
                "title": "Submit Data",
                "data": {"key": "value"}
            }
        ]
        
        card = self.builder.create_action_card(title, message, actions)
        
        # Convert to JSON for inspection
        card_json = json.loads(card.to_json())
        
        # Check actions array
        self.assertIn("actions", card_json)
        self.assertEqual(len(card_json["actions"]), 2)
        
        # Check first action
        self.assertEqual(card_json["actions"][0]["type"], "Action.OpenUrl")
        self.assertEqual(card_json["actions"][0]["title"], "Open URL")
        self.assertEqual(card_json["actions"][0]["url"], "https://example.com")
        
        # Check second action
        self.assertEqual(card_json["actions"][1]["type"], "Action.Submit")
        self.assertEqual(card_json["actions"][1]["title"], "Submit Data")
        self.assertEqual(card_json["actions"][1]["data"], {"key": "value"})
    
    def test_validate_card(self):
        """Test card validation function."""
        # Create a valid card
        card = self.builder.create_basic_card("Test", "Validation")
        
        # Validate the card
        result = self.builder.validate_card(card)
        
        # Check validation results
        self.assertIsInstance(result, dict)
        self.assertIn("valid", result)
        self.assertIn("size", result)
        self.assertTrue(result["valid"])
        self.assertGreater(result["size"], 0)
        
    def test_get_json(self):
        """Test getting JSON representation of a card."""
        card = self.builder.create_basic_card("JSON Test", "Testing JSON output")
        
        # Get JSON string
        json_str = self.builder.get_json(card)
        
        # Check that it's valid JSON
        try:
            parsed = json.loads(json_str)
            self.assertIsInstance(parsed, dict)
            self.assertEqual(parsed["type"], "AdaptiveCard")
        except json.JSONDecodeError:
            self.fail("get_json() did not return valid JSON")


if __name__ == "__main__":
    unittest.main()