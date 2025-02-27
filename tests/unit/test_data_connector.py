"""Tests for the DataConnector class."""

import json
import unittest

from adaptive_cards.containers import FactSet, ColumnSet
from adaptive_cards.elements import TextBlock
from tools.agent_toolkit.data_connector import DataConnector


class TestDataConnector(unittest.TestCase):
    """Test cases for the DataConnector class."""
    
    def test_create_fact_set(self):
        """Test creating a fact set from a dictionary."""
        # Create test data
        facts = {
            "Name": "John Doe",
            "Email": "john@example.com",
            "Role": "Developer"
        }
        
        # Create fact set
        fact_set = DataConnector.create_fact_set(facts)
        
        # Check result
        self.assertIsInstance(fact_set, FactSet)
        self.assertEqual(len(fact_set.facts), 3)
        
        # Convert to dict for easier checking
        fact_dict = {fact.title: fact.value for fact in fact_set.facts}
        self.assertEqual(fact_dict["Name"], "John Doe")
        self.assertEqual(fact_dict["Email"], "john@example.com")
        self.assertEqual(fact_dict["Role"], "Developer")
    
    def test_create_list(self):
        """Test creating a list of text blocks."""
        # Create test data
        items = ["Item 1", "Item 2", "Item 3"]
        
        # Create list as bullet points
        bullet_list = DataConnector.create_list(items)
        
        # Check bullet list
        self.assertIsInstance(bullet_list, list)
        self.assertEqual(len(bullet_list), 3)
        
        for i, item in enumerate(bullet_list):
            self.assertIsInstance(item, TextBlock)
            self.assertTrue(item.text.startswith("•"))
            self.assertIn(f"Item {i+1}", item.text)
        
        # Create numbered list
        numbered_list = DataConnector.create_list(items, is_numbered=True)
        
        # Check numbered list
        for i, item in enumerate(numbered_list):
            self.assertIsInstance(item, TextBlock)
            self.assertTrue(item.text.startswith(f"{i+1}."))
            self.assertIn(f"Item {i+1}", item.text)
    
    def test_create_table(self):
        """Test creating a table from headers and rows."""
        # Create test data
        headers = ["Name", "Age", "Role"]
        rows = [
            ["John", "30", "Developer"],
            ["Jane", "28", "Designer"]
        ]
        
        # Create table with default settings
        table = DataConnector.create_table(headers, rows)
        
        # Check table structure
        self.assertIsInstance(table, list)
        self.assertGreaterEqual(len(table), 3)  # Header container + 2 row containers
        
        # Check header
        self.assertEqual(table[0].style, "emphasis")
        
        # Create table with custom settings
        custom_table = DataConnector.create_table(
            headers,
            rows,
            column_widths=["stretch", 1, 2],
            has_header_row=False,
            alternate_row_style=False
        )
        
        # No header styling when has_header_row is False
        self.assertNotEqual(custom_table[0].style, "emphasis")
    
    def test_from_json_dict(self):
        """Test converting a dictionary to card elements."""
        # Create test data
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "scores": [90, 85, 92]
        }
        
        # Convert from dictionary
        elements = DataConnector.from_json(data)
        
        # Should create a fact set
        self.assertGreaterEqual(len(elements), 1)
        self.assertIsInstance(elements[0], FactSet)
    
    def test_from_json_list(self):
        """Test converting a list to card elements."""
        # Create test data
        data = ["Item 1", "Item 2", "Item 3"]
        
        # Convert from list
        elements = DataConnector.from_json(data)
        
        # Should create text blocks
        self.assertEqual(len(elements), 3)
        for element in elements:
            self.assertIsInstance(element, TextBlock)
    
    def test_from_json_list_of_dicts(self):
        """Test converting a list of dictionaries to a table."""
        # Create test data - list of dictionaries
        data = [
            {"name": "John", "age": 30, "role": "Developer"},
            {"name": "Jane", "age": 28, "role": "Designer"}
        ]
        
        # Convert from list of dicts
        elements = DataConnector.from_json(data)
        
        # Should create a table (multiple containers)
        self.assertGreater(len(elements), 1)
    
    def test_from_json_string(self):
        """Test converting a JSON string to card elements."""
        # Create test JSON string
        json_str = '{"name": "John", "email": "john@example.com"}'
        
        # Convert from JSON string
        elements = DataConnector.from_json(json_str)
        
        # Should create a fact set
        self.assertGreaterEqual(len(elements), 1)
        self.assertIsInstance(elements[0], FactSet)
        
        # Test invalid JSON
        invalid_json = '{not valid json'
        elements = DataConnector.from_json(invalid_json)
        
        # Should return error message
        self.assertEqual(len(elements), 1)
        self.assertIsInstance(elements[0], TextBlock)
        self.assertIn("Invalid JSON data", elements[0].text)
    
    def test_from_csv(self):
        """Test converting CSV data to card elements."""
        # Create test CSV
        csv_data = "Name,Age,Role\nJohn,30,Developer\nJane,28,Designer"
        
        # Convert from CSV
        elements = DataConnector.from_csv(csv_data)
        
        # Should create a table (multiple containers)
        self.assertGreater(len(elements), 1)
        
        # Check for headers
        header_container = elements[0]
        header_column_set = next((item for item in header_container.items if isinstance(item, ColumnSet)), None)
        self.assertIsNotNone(header_column_set)
        
        # Test empty CSV
        empty_csv = ""
        elements = DataConnector.from_csv(empty_csv)
        
        # Should return error message
        self.assertEqual(len(elements), 1)
        self.assertIsInstance(elements[0], TextBlock)
        self.assertIn("Empty CSV data", elements[0].text)
    
    def test_key_value_pairs_to_columns(self):
        """Test converting a dictionary to a two-column layout."""
        # Create test data
        data = {
            "Name": "John Doe",
            "Email": "john@example.com",
            "Role": "Developer"
        }
        
        # Convert to columns
        column_set = DataConnector.key_value_pairs_to_columns(data)
        
        # Check result
        self.assertIsInstance(column_set, ColumnSet)
        self.assertEqual(len(column_set.columns), 2)
        
        # First column should have keys
        key_column = column_set.columns[0]
        self.assertEqual(len(key_column.items), 3)
        
        # Second column should have values
        value_column = column_set.columns[1]
        self.assertEqual(len(value_column.items), 3)
        
        # Check custom widths
        custom_columns = DataConnector.key_value_pairs_to_columns(
            data,
            key_width="stretch",
            value_width="auto"
        )
        
        self.assertEqual(custom_columns.columns[0].width, "stretch")
        self.assertEqual(custom_columns.columns[1].width, "auto")


if __name__ == "__main__":
    unittest.main()