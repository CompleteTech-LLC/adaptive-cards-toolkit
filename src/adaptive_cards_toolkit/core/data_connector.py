"""Convert structured data to adaptive card elements."""

import csv
import io
import json
from typing import Any, Dict, List, Optional, Tuple, Union

import adaptive_cards.card_types as types
from adaptive_cards.containers import Column, ColumnSet, Container, Fact, FactSet
from adaptive_cards.elements import Element, TextBlock

from adaptive_cards_toolkit.core.element_factory import ElementFactory


class DataConnector:
    """Utility for converting structured data to adaptive card elements."""
    
    @staticmethod
    def create_fact_set(facts: Dict[str, str]) -> FactSet:
        """Create a fact set from a dictionary.
        
        Args:
            facts: Dictionary where keys are titles and values are facts.
            
        Returns:
            A FactSet element.
        """
        fact_items = []
        for title, value in facts.items():
            fact_items.append(Fact(title=title, value=value))
            
        return FactSet(facts=fact_items)
    
    @staticmethod
    def create_list(items: List[str], is_numbered: bool = False) -> List[TextBlock]:
        """Create a list of text blocks.
        
        Args:
            items: List of strings to display.
            is_numbered: Whether to create a numbered list.
            
        Returns:
            A list of TextBlock elements.
        """
        text_blocks = []
        for i, item in enumerate(items, 1):
            prefix = f"{i}. " if is_numbered else "• "
            text_blocks.append(TextBlock(
                text=f"{prefix}{item}",
                wrap=True
            ))
            
        return text_blocks
    
    @staticmethod
    def create_table(
        headers: List[str],
        rows: List[List[str]],
        column_widths: Optional[List[Union[int, str]]] = None,
        has_header_row: bool = True,
        alternate_row_style: bool = True
    ) -> List[Element]:
        """Create a table-like structure using column sets.
        
        Args:
            headers: List of column headers.
            rows: List of rows, where each row is a list of strings.
            column_widths: Optional list of column widths.
            has_header_row: Whether to style the first row as a header.
            alternate_row_style: Whether to use alternating background styles for rows.
            
        Returns:
            A list of elements representing a table.
        """
        table_elements = []
        
        # Use equal column widths if not specified
        if column_widths is None:
            column_widths = [1] * len(headers)
            
        # Create header row if needed
        if has_header_row:
            header_columns = []
            for i, header in enumerate(headers):
                header_columns.append(Column(
                    items=[ElementFactory.create_text(header, weight=types.FontWeight.BOLDER)],
                    width=column_widths[i]
                ))
                
            table_elements.append(Container(
                items=[ColumnSet(columns=header_columns)],
                style=types.ContainerStyle.EMPHASIS,
                separator=True
            ))
        
        # Create data rows
        for row_idx, row in enumerate(rows):
            row_columns = []
            
            for col_idx, cell in enumerate(row):
                if col_idx < len(column_widths):  # Ensure we don't go out of bounds
                    row_columns.append(Column(
                        items=[ElementFactory.create_text(cell)],
                        width=column_widths[col_idx]
                    ))
            
            # Apply alternating style if requested
            style = None
            if alternate_row_style and row_idx % 2 == 1:
                style = types.ContainerStyle.ACCENT
                
            table_elements.append(Container(
                items=[ColumnSet(columns=row_columns)],
                style=style
            ))
            
        return table_elements
    
    @staticmethod
    def from_json(json_data: Union[str, Dict[str, Any], List[Dict[str, Any]]]) -> List[Element]:
        """Convert JSON data to card elements.
        
        Args:
            json_data: JSON string or parsed JSON object.
            
        Returns:
            A list of elements representing the JSON data.
        """
        # Parse JSON if it's a string
        if isinstance(json_data, str):
            try:
                data = json.loads(json_data)
            except json.JSONDecodeError:
                return [ElementFactory.create_text("Invalid JSON data", color=types.Colors.ATTENTION)]
        else:
            data = json_data
            
        elements = []
        
        # Handle dictionary
        if isinstance(data, dict):
            elements.append(DataConnector.create_fact_set(
                {k: str(v) if not isinstance(v, (dict, list)) else json.dumps(v, indent=2) 
                for k, v in data.items()}
            ))
        
        # Handle list of dictionaries (table-like)
        elif isinstance(data, list) and data and all(isinstance(item, dict) for item in data):
            # Extract all unique keys as headers
            all_keys = set()
            for item in data:
                all_keys.update(item.keys())
                
            headers = list(all_keys)
            rows = []
            
            for item in data:
                row = [str(item.get(key, "")) for key in headers]
                rows.append(row)
                
            elements.extend(DataConnector.create_table(headers, rows))
        
        # Handle simple list
        elif isinstance(data, list):
            elements.extend(DataConnector.create_list([str(item) for item in data]))
        
        return elements
    
    @staticmethod
    def from_csv(csv_data: str) -> List[Element]:
        """Convert CSV data to card elements.
        
        Args:
            csv_data: CSV string.
            
        Returns:
            A list of elements representing the CSV data as a table.
        """
        try:
            # Parse CSV
            csv_reader = csv.reader(io.StringIO(csv_data))
            rows = list(csv_reader)
            
            if not rows:
                return [ElementFactory.create_text("Empty CSV data", color=types.Colors.ATTENTION)]
                
            # First row as headers
            headers = rows[0]
            data_rows = rows[1:]
            
            return DataConnector.create_table(headers, data_rows)
            
        except Exception as e:
            return [ElementFactory.create_text(f"Error parsing CSV: {str(e)}", color=types.Colors.ATTENTION)]
    
    @staticmethod
    def key_value_pairs_to_columns(
        data: Dict[str, Any], 
        key_width: Union[int, str] = 1,
        value_width: Union[int, str] = 2
    ) -> ColumnSet:
        """Convert a dictionary to a two-column layout with keys and values.
        
        Args:
            data: Dictionary of key-value pairs.
            key_width: Width for the key column.
            value_width: Width for the value column.
            
        Returns:
            A ColumnSet with keys and values.
        """
        key_column_items = []
        value_column_items = []
        
        for key, value in data.items():
            key_column_items.append(ElementFactory.create_text(
                str(key), 
                weight=types.FontWeight.BOLDER
            ))
            
            # Handle different types of values
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, indent=2)
            else:
                value_str = str(value)
                
            value_column_items.append(ElementFactory.create_text(value_str))
            
        return ColumnSet(columns=[
            Column(items=key_column_items, width=key_width),
            Column(items=value_column_items, width=value_width)
        ])