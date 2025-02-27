"""Tests for the LayoutHelper class."""

import unittest

import adaptive_cards.card_types as types
from adaptive_cards_toolkit.core.layout_helper import LayoutHelper
from adaptive_cards_toolkit.core.element_factory import ElementFactory
from adaptive_cards.containers import Container, Column, ColumnSet


class TestLayoutHelper(unittest.TestCase):
    """Test cases for the LayoutHelper class."""
    
    def test_create_container(self):
        """Test creating a container with various properties."""
        # Create test elements
        heading = ElementFactory.create_heading("Container Test")
        text = ElementFactory.create_text("Container content")
        
        # Basic container
        container = LayoutHelper.create_container([heading, text])
        self.assertIsInstance(container, Container)
        self.assertEqual(len(container.items), 2)
        self.assertEqual(container.items[0], heading)
        self.assertEqual(container.items[1], text)
        
        # Container with style and spacing
        styled_container = LayoutHelper.create_container(
            [heading],
            style=types.ContainerStyle.EMPHASIS,
            spacing=types.Spacing.LARGE,
            separator=True,
            id="test-container"
        )
        self.assertEqual(styled_container.style, types.ContainerStyle.EMPHASIS)
        self.assertEqual(styled_container.spacing, types.Spacing.LARGE)
        self.assertTrue(styled_container.separator)
        self.assertEqual(styled_container.id, "test-container")
    
    def test_create_column(self):
        """Test creating a column with various properties."""
        # Create test elements
        heading = ElementFactory.create_heading("Column Test")
        text = ElementFactory.create_text("Column content")
        
        # Basic column
        column = LayoutHelper.create_column([heading, text])
        self.assertIsInstance(column, Column)
        self.assertEqual(len(column.items), 2)
        self.assertEqual(column.width, "auto")  # Default value
        
        # Column with custom width and style
        styled_column = LayoutHelper.create_column(
            [heading],
            width="stretch",
            spacing=types.Spacing.SMALL,
            vertical_content_alignment=types.VerticalAlignment.CENTER,
            style=types.ContainerStyle.ACCENT
        )
        self.assertEqual(styled_column.width, "stretch")
        self.assertEqual(styled_column.spacing, types.Spacing.SMALL)
        self.assertEqual(styled_column.vertical_content_alignment, types.VerticalAlignment.CENTER)
        self.assertEqual(styled_column.style, types.ContainerStyle.ACCENT)
    
    def test_create_column_set(self):
        """Test creating a column set with various properties."""
        # Create test columns
        column1 = LayoutHelper.create_column([ElementFactory.create_text("Column 1")])
        column2 = LayoutHelper.create_column([ElementFactory.create_text("Column 2")])
        
        # Basic column set
        column_set = LayoutHelper.create_column_set([column1, column2])
        self.assertIsInstance(column_set, ColumnSet)
        self.assertEqual(len(column_set.columns), 2)
        
        # Column set with spacing and separator
        styled_column_set = LayoutHelper.create_column_set(
            [column1, column2],
            spacing=types.Spacing.EXTRA_LARGE,
            separator=True,
            id="test-column-set"
        )
        self.assertEqual(styled_column_set.spacing, types.Spacing.EXTRA_LARGE)
        self.assertTrue(styled_column_set.separator)
        self.assertEqual(styled_column_set.id, "test-column-set")
    
    def test_create_equal_columns(self):
        """Test creating a column set with equal-width columns."""
        # Create content for each column
        col1_content = [ElementFactory.create_heading("Column 1")]
        col2_content = [ElementFactory.create_heading("Column 2")]
        col3_content = [ElementFactory.create_heading("Column 3")]
        
        # Create equal columns
        column_set = LayoutHelper.create_equal_columns(
            [col1_content, col2_content, col3_content],
            spacing=types.Spacing.MEDIUM
        )
        
        self.assertIsInstance(column_set, ColumnSet)
        self.assertEqual(len(column_set.columns), 3)
        self.assertEqual(column_set.spacing, types.Spacing.MEDIUM)
        
        # Check that all columns have equal width
        for column in column_set.columns:
            self.assertEqual(column.width, 1)
    
    def test_create_two_column_layout(self):
        """Test creating a two-column layout."""
        # Create content for each column
        left_content = [ElementFactory.create_heading("Left Side")]
        right_content = [ElementFactory.create_heading("Right Side")]
        
        # Create two-column layout with default widths
        column_set = LayoutHelper.create_two_column_layout(
            left_content, 
            right_content
        )
        
        self.assertIsInstance(column_set, ColumnSet)
        self.assertEqual(len(column_set.columns), 2)
        self.assertEqual(column_set.columns[0].width, 1)
        self.assertEqual(column_set.columns[1].width, 1)
        
        # Create two-column layout with custom widths
        custom_column_set = LayoutHelper.create_two_column_layout(
            left_content,
            right_content,
            left_width="stretch",
            right_width="auto",
            spacing=types.Spacing.LARGE
        )
        
        self.assertEqual(custom_column_set.columns[0].width, "stretch")
        self.assertEqual(custom_column_set.columns[1].width, "auto")
        self.assertEqual(custom_column_set.spacing, types.Spacing.LARGE)
    
    def test_create_header_body_footer_layout(self):
        """Test creating a header-body-footer layout."""
        # Create content for each section
        header_items = [ElementFactory.create_heading("Header")]
        body_items = [ElementFactory.create_text("Body content")]
        footer_items = [ElementFactory.create_text("Footer content", is_subtle=True)]
        
        # Create layout with all sections
        containers = LayoutHelper.create_header_body_footer_layout(
            header_items,
            body_items,
            footer_items
        )
        
        self.assertIsInstance(containers, list)
        self.assertEqual(len(containers), 3)
        
        # Check header container
        header = containers[0]
        self.assertEqual(header.style, types.ContainerStyle.EMPHASIS)
        self.assertTrue(header.bleed)
        
        # Check body container
        body = containers[1]
        self.assertEqual(body.spacing, types.Spacing.MEDIUM)
        
        # Check footer container
        footer = containers[2]
        self.assertEqual(footer.style, types.ContainerStyle.ACCENT)
        self.assertEqual(footer.spacing, types.Spacing.MEDIUM)
        self.assertTrue(footer.separator)
        
        # Test without footer
        containers_no_footer = LayoutHelper.create_header_body_footer_layout(
            header_items,
            body_items
        )
        
        self.assertEqual(len(containers_no_footer), 2)


if __name__ == "__main__":
    unittest.main()