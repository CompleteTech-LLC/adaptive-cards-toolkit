"""Tests for the ElementFactory class."""

import unittest
from dataclasses_json import dataclass_json

import adaptive_cards.card_types as types
from tools.agent_toolkit.element_factory import ElementFactory
from adaptive_cards.elements import TextBlock, Image
from adaptive_cards.inputs import InputText, InputChoice, InputChoiceSet, InputDate


class TestElementFactory(unittest.TestCase):
    """Test cases for the ElementFactory class."""
    
    def test_create_heading(self):
        """Test creating heading elements with different levels."""
        # Level 1 heading
        heading1 = ElementFactory.create_heading("Level 1 Heading", level=1)
        self.assertIsInstance(heading1, TextBlock)
        self.assertEqual(heading1.text, "Level 1 Heading")
        self.assertEqual(heading1.size, types.FontSize.EXTRA_LARGE)
        self.assertEqual(heading1.weight, types.FontWeight.BOLDER)
        self.assertTrue(heading1.wrap)
        
        # Level 2 heading
        heading2 = ElementFactory.create_heading("Level 2 Heading", level=2)
        self.assertIsInstance(heading2, TextBlock)
        self.assertEqual(heading2.text, "Level 2 Heading")
        self.assertEqual(heading2.size, types.FontSize.LARGE)
        
        # Level 3 heading
        heading3 = ElementFactory.create_heading("Level 3 Heading", level=3)
        self.assertIsInstance(heading3, TextBlock)
        self.assertEqual(heading3.text, "Level 3 Heading")
        self.assertEqual(heading3.size, types.FontSize.MEDIUM)
        
        # Invalid level (should default to medium)
        heading_invalid = ElementFactory.create_heading("Invalid Level", level=10)
        self.assertEqual(heading_invalid.size, types.FontSize.MEDIUM)
    
    def test_create_text(self):
        """Test creating text elements with different properties."""
        # Basic text
        text = ElementFactory.create_text("Basic text")
        self.assertIsInstance(text, TextBlock)
        self.assertEqual(text.text, "Basic text")
        self.assertTrue(text.wrap)
        self.assertFalse(text.is_subtle)
        
        # Subtle text
        subtle_text = ElementFactory.create_text("Subtle text", is_subtle=True)
        self.assertTrue(subtle_text.is_subtle)
        
        # Text with weight
        bold_text = ElementFactory.create_text("Bold text", weight=types.FontWeight.BOLDER)
        self.assertEqual(bold_text.weight, types.FontWeight.BOLDER)
    
    def test_create_important_text(self):
        """Test creating important text with different colors."""
        # Default important text (attention color)
        important = ElementFactory.create_important_text("Important message")
        self.assertIsInstance(important, TextBlock)
        self.assertEqual(important.text, "Important message")
        self.assertEqual(important.color, types.Colors.ATTENTION)
        self.assertEqual(important.weight, types.FontWeight.BOLDER)
        
        # Important text with custom color
        warning = ElementFactory.create_important_text("Warning message", color=types.Colors.WARNING)
        self.assertEqual(warning.color, types.Colors.WARNING)
    
    def test_create_image(self):
        """Test creating image elements."""
        url = "https://example.com/image.png"
        alt_text = "Example image"
        
        # Basic image
        image = ElementFactory.create_image(url)
        self.assertIsInstance(image, Image)
        self.assertEqual(image.url, url)
        
        # Image with alt text
        image_with_alt = ElementFactory.create_image(url, alt_text=alt_text)
        self.assertEqual(image_with_alt.alt_text, alt_text)
        
        # Image with size and style
        styled_image = ElementFactory.create_image(
            url, 
            size=types.ImageSize.MEDIUM,
            style=types.ImageStyle.PERSON
        )
        self.assertEqual(styled_image.size, types.ImageSize.MEDIUM)
        self.assertEqual(styled_image.style, types.ImageStyle.PERSON)
    
    def test_create_text_input(self):
        """Test creating text input elements."""
        # Basic text input
        text_input = ElementFactory.create_text_input("name")
        self.assertIsInstance(text_input, InputText)
        self.assertEqual(text_input.id, "name")
        self.assertFalse(text_input.is_required)
        
        # Required text input with placeholder and max length
        required_input = ElementFactory.create_text_input(
            "email",
            placeholder="Enter your email",
            is_required=True,
            max_length=100
        )
        self.assertEqual(required_input.placeholder, "Enter your email")
        self.assertTrue(required_input.is_required)
        self.assertEqual(required_input.max_length, 100)
    
    def test_create_choice_set(self):
        """Test creating choice set input elements."""
        choices = [
            {"title": "Option 1", "value": "1"},
            {"title": "Option 2", "value": "2"}
        ]
        
        # Basic choice set
        choice_set = ElementFactory.create_choice_set("options", choices)
        self.assertIsInstance(choice_set, InputChoiceSet)
        self.assertEqual(choice_set.id, "options")
        self.assertEqual(len(choice_set.choices), 2)
        
        # Check that choices are properly created
        self.assertIsInstance(choice_set.choices[0], InputChoice)
        self.assertEqual(choice_set.choices[0].title, "Option 1")
        self.assertEqual(choice_set.choices[0].value, "1")
        
        # Multi-select choice set
        multi_select = ElementFactory.create_choice_set(
            "multi",
            choices,
            is_multi_select=True,
            placeholder="Select options"
        )
        self.assertTrue(multi_select.is_multi_select)
        self.assertEqual(multi_select.placeholder, "Select options")
    
    def test_create_date_input(self):
        """Test creating date input elements."""
        # Basic date input
        date_input = ElementFactory.create_date_input("date")
        self.assertIsInstance(date_input, InputDate)
        self.assertEqual(date_input.id, "date")
        
        # Required date input with placeholder
        required_date = ElementFactory.create_date_input(
            "required_date",
            placeholder="Select a date",
            is_required=True
        )
        self.assertEqual(required_date.placeholder, "Select a date")
        self.assertTrue(required_date.is_required)


if __name__ == "__main__":
    unittest.main()