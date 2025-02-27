"""Tests for the TemplateFactory class."""

import json
import unittest

from adaptive_cards.card import AdaptiveCard
from adaptive_cards_toolkit.templates.templates import TemplateFactory


class TestTemplateFactory(unittest.TestCase):
    """Test cases for the TemplateFactory class."""
    
    def test_create_notification_card(self):
        """Test creating notification cards."""
        # Basic notification
        card = TemplateFactory.create_notification_card(
            title="Test Notification",
            message="This is a test notification"
        )
        
        self.assertIsInstance(card, AdaptiveCard)
        card_json = json.loads(card.to_json())
        
        # Validate basic structure
        self.assertEqual(card_json["type"], "AdaptiveCard")
        
        # Check title and message
        has_title = False
        has_message = False
        
        for item in card_json["body"]:
            if item.get("type") == "TextBlock" and item.get("text") == "Test Notification":
                has_title = True
            if item.get("type") == "TextBlock" and item.get("text") == "This is a test notification":
                has_message = True
        
        self.assertTrue(has_title)
        self.assertTrue(has_message)
        
        # Test with all options
        full_card = TemplateFactory.create_notification_card(
            title="Warning",
            message="System alert",
            level="warning",
            icon_url="https://example.com/icon.png",
            action_url="https://example.com"
        )
        
        full_json = json.loads(full_card.to_json())
        
        # Check for action
        self.assertIn("actions", full_json)
        self.assertEqual(len(full_json["actions"]), 1)
        self.assertEqual(full_json["actions"][0]["type"], "Action.OpenUrl")
        self.assertEqual(full_json["actions"][0]["url"], "https://example.com")
        
        # Check for icon
        has_image = False
        for item in full_json["body"]:
            if item.get("type") == "ColumnSet":
                for column in item.get("columns", []):
                    for content in column.get("items", []):
                        if content.get("type") == "Image" and content.get("url") == "https://example.com/icon.png":
                            has_image = True
        
        self.assertTrue(has_image)
    
    def test_create_form_card(self):
        """Test creating form cards."""
        # Create form fields
        fields = [
            {
                "type": "text",
                "id": "name",
                "label": "Your Name",
                "placeholder": "Enter your name",
                "required": True
            },
            {
                "type": "choice",
                "id": "rating",
                "label": "Rating",
                "choices": [
                    {"title": "Good", "value": "good"},
                    {"title": "Bad", "value": "bad"}
                ]
            }
        ]
        
        # Create form card
        card = TemplateFactory.create_form_card(
            title="Feedback Form",
            fields=fields,
            submit_label="Send Feedback",
            subtitle="Please provide your feedback"
        )
        
        self.assertIsInstance(card, AdaptiveCard)
        card_json = json.loads(card.to_json())
        
        # Check form title and subtitle
        titles = [item.get("text") for item in card_json["body"] if item.get("type") == "TextBlock"]
        self.assertIn("Feedback Form", titles)
        self.assertIn("Please provide your feedback", titles)
        
        # Check for input fields
        input_types = []
        for item in card_json["body"]:
            if item.get("type").startswith("Input."):
                input_types.append(item.get("type"))
        
        self.assertIn("Input.Text", input_types)
        self.assertIn("Input.ChoiceSet", input_types)
        
        # Check submit button
        self.assertIn("actions", card_json)
        self.assertEqual(len(card_json["actions"]), 1)
        self.assertEqual(card_json["actions"][0]["type"], "Action.Submit")
        self.assertEqual(card_json["actions"][0]["title"], "Send Feedback")
    
    def test_create_article_card(self):
        """Test creating article cards."""
        # Basic article
        card = TemplateFactory.create_article_card(
            title="Test Article",
            content="This is the article content."
        )
        
        self.assertIsInstance(card, AdaptiveCard)
        card_json = json.loads(card.to_json())
        
        # Check title and content
        titles = [item.get("text") for item in card_json["body"] if item.get("type") == "TextBlock"]
        self.assertIn("Test Article", titles)
        self.assertIn("This is the article content.", titles)
        
        # Test with all options
        full_card = TemplateFactory.create_article_card(
            title="Full Article",
            content="Complete article content.",
            image_url="https://example.com/image.jpg",
            author="John Doe",
            date="2023-05-15",
            action_url="https://example.com/article"
        )
        
        full_json = json.loads(full_card.to_json())
        
        # Check for image
        has_image = False
        for item in full_json["body"]:
            if item.get("type") == "Image" and item.get("url") == "https://example.com/image.jpg":
                has_image = True
        
        self.assertTrue(has_image)
        
        # Check for action
        self.assertIn("actions", full_json)
        self.assertEqual(full_json["actions"][0]["type"], "Action.OpenUrl")
        self.assertEqual(full_json["actions"][0]["url"], "https://example.com/article")
        
        # Check for metadata
        metadata_text = None
        for item in full_json["body"]:
            if item.get("type") == "TextBlock" and item.get("isSubtle") is True:
                metadata_text = item.get("text")
        
        self.assertIsNotNone(metadata_text)
        self.assertIn("John Doe", metadata_text)
        self.assertIn("2023-05-15", metadata_text)
    
    def test_create_dashboard_card(self):
        """Test creating dashboard cards."""
        # Create metrics
        metrics = {
            "Total Users": "1,234",
            "New Users": "+56",
            "Engagement": "78%"
        }
        
        # Create dashboard card
        card = TemplateFactory.create_dashboard_card(
            title="Performance Dashboard",
            metrics=metrics,
            description="Monthly performance metrics",
            chart_image_url="https://example.com/chart.png"
        )
        
        self.assertIsInstance(card, AdaptiveCard)
        card_json = json.loads(card.to_json())
        
        # Check header container
        has_header = False
        for item in card_json["body"]:
            if item.get("type") == "Container" and item.get("style") == "emphasis":
                has_header = True
        
        self.assertTrue(has_header)
        
        # Check for facts
        has_fact_set = False
        for item in card_json["body"]:
            if item.get("type") == "FactSet":
                has_fact_set = True
                fact_titles = [fact.get("title") for fact in item.get("facts", [])]
                fact_values = [fact.get("value") for fact in item.get("facts", [])]
                
                # Check facts content
                self.assertIn("Total Users", fact_titles)
                self.assertIn("New Users", fact_titles)
                self.assertIn("Engagement", fact_titles)
                self.assertIn("1,234", fact_values)
                self.assertIn("+56", fact_values)
                self.assertIn("78%", fact_values)
        
        self.assertTrue(has_fact_set)
        
        # Check for chart image
        has_chart = False
        for item in card_json["body"]:
            if item.get("type") == "Image" and item.get("url") == "https://example.com/chart.png":
                has_chart = True
        
        self.assertTrue(has_chart)
    
    def test_create_confirmation_card(self):
        """Test creating confirmation cards."""
        # Create confirmation card
        card = TemplateFactory.create_confirmation_card(
            title="Confirm Action",
            message="Are you sure you want to proceed?",
            confirm_button_text="Yes, Proceed",
            cancel_button_text="No, Cancel"
        )
        
        self.assertIsInstance(card, AdaptiveCard)
        card_json = json.loads(card.to_json())
        
        # Check title and message
        titles = [item.get("text") for item in card_json["body"] if item.get("type") == "TextBlock"]
        self.assertIn("Confirm Action", titles)
        self.assertIn("Are you sure you want to proceed?", titles)
        
        # Check buttons
        self.assertIn("actions", card_json)
        self.assertEqual(len(card_json["actions"]), 2)
        
        action_titles = [action.get("title") for action in card_json["actions"]]
        self.assertIn("Yes, Proceed", action_titles)
        self.assertIn("No, Cancel", action_titles)
        
        # Check button types and styles
        for action in card_json["actions"]:
            if action.get("title") == "Yes, Proceed":
                self.assertEqual(action.get("style"), "positive")
                self.assertIn("action", action.get("data"))
                self.assertEqual(action.get("data").get("action"), "confirm")
            elif action.get("title") == "No, Cancel":
                self.assertIn("action", action.get("data"))
                self.assertEqual(action.get("data").get("action"), "cancel")


if __name__ == "__main__":
    unittest.main()