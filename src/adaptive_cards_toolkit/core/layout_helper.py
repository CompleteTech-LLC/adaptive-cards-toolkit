"""Helper for creating responsive layouts in adaptive cards."""

from typing import Any, List, Optional, Union

import adaptive_cards.card_types as types
from adaptive_cards.containers import Column, ColumnSet, Container
from adaptive_cards.elements import Element
from adaptive_cards.inputs import InputTypes


class LayoutHelper:
    """Helper for creating common layout patterns in adaptive cards."""
    
    @staticmethod
    def create_container(
        items: List[Union[Element, 'Container', InputTypes]],
        style: Optional[types.ContainerStyle] = None,
        spacing: Optional[types.Spacing] = None,
        separator: bool = False,
        id: Optional[str] = None
    ) -> Container:
        """Create a container with the given items.
        
        Args:
            items: List of elements to include in the container.
            style: Optional style for the container.
            spacing: Optional spacing to apply.
            separator: Whether to include a separator before the container.
            id: Optional ID for the container.
            
        Returns:
            A Container with the specified elements and properties.
        """
        return Container(
            items=items,
            style=style,
            spacing=spacing,
            separator=separator,
            id=id
        )
    
    @staticmethod
    def create_column_set(
        columns: List[Column],
        spacing: Optional[types.Spacing] = None,
        separator: bool = False,
        id: Optional[str] = None
    ) -> ColumnSet:
        """Create a column set with the given columns.
        
        Args:
            columns: List of columns to include in the set.
            spacing: Optional spacing to apply.
            separator: Whether to include a separator before the column set.
            id: Optional ID for the column set.
            
        Returns:
            A ColumnSet with the specified columns and properties.
        """
        return ColumnSet(
            columns=columns,
            spacing=spacing,
            separator=separator,
            id=id
        )
    
    @staticmethod
    def create_column(
        items: List[Union[Element, 'Container', InputTypes]],
        width: Union[int, str] = "auto",
        spacing: Optional[types.Spacing] = None,
        vertical_content_alignment: Optional[types.VerticalAlignment] = None,
        style: Optional[types.ContainerStyle] = None
    ) -> Column:
        """Create a column with the given items.
        
        Args:
            items: List of elements to include in the column.
            width: Width of the column, either "auto", "stretch", or a number for weighted distribution.
            spacing: Optional spacing to apply.
            vertical_content_alignment: Optional vertical alignment of content.
            style: Optional style for the column.
            
        Returns:
            A Column with the specified elements and properties.
        """
        return Column(
            items=items,
            width=width,
            spacing=spacing,
            vertical_content_alignment=vertical_content_alignment,
            style=style
        )
    
    @staticmethod
    def create_equal_columns(
        column_contents: List[List[Union[Element, 'Container', InputTypes]]],
        spacing: Optional[types.Spacing] = None
    ) -> ColumnSet:
        """Create a column set with equal-width columns.
        
        Args:
            column_contents: List of lists, where each inner list is the contents of a column.
            spacing: Optional spacing to apply to the column set.
            
        Returns:
            A ColumnSet with equal-width columns.
        """
        columns = []
        for content in column_contents:
            columns.append(Column(
                items=content,
                width=1  # Equal weighting
            ))
            
        return LayoutHelper.create_column_set(columns, spacing)
    
    @staticmethod
    def create_two_column_layout(
        left_content: List[Union[Element, 'Container', InputTypes]],
        right_content: List[Union[Element, 'Container', InputTypes]],
        left_width: Union[int, str] = 1,
        right_width: Union[int, str] = 1,
        spacing: Optional[types.Spacing] = None
    ) -> ColumnSet:
        """Create a common two-column layout.
        
        Args:
            left_content: List of elements for the left column.
            right_content: List of elements for the right column.
            left_width: Width of the left column.
            right_width: Width of the right column.
            spacing: Optional spacing to apply to the column set.
            
        Returns:
            A ColumnSet with two columns.
        """
        columns = [
            Column(items=left_content, width=left_width),
            Column(items=right_content, width=right_width)
        ]
        
        return LayoutHelper.create_column_set(columns, spacing)
    
    @staticmethod
    def create_header_body_footer_layout(
        header_items: List[Union[Element, 'Container', InputTypes]],
        body_items: List[Union[Element, 'Container', InputTypes]],
        footer_items: Optional[List[Union[Element, 'Container', InputTypes]]] = None,
        header_style: Optional[types.ContainerStyle] = types.ContainerStyle.EMPHASIS,
        body_style: Optional[types.ContainerStyle] = None,
        footer_style: Optional[types.ContainerStyle] = types.ContainerStyle.ACCENT
    ) -> List[Container]:
        """Create a common layout with header, body, and optional footer.
        
        Args:
            header_items: List of elements for the header.
            body_items: List of elements for the body.
            footer_items: Optional list of elements for the footer.
            header_style: Optional style for the header container.
            body_style: Optional style for the body container.
            footer_style: Optional style for the footer container.
            
        Returns:
            A list of Containers representing the layout.
        """
        containers = [
            Container(items=header_items, style=header_style, bleed=True),
            Container(items=body_items, style=body_style, spacing=types.Spacing.MEDIUM)
        ]
        
        if footer_items:
            containers.append(Container(
                items=footer_items,
                style=footer_style,
                spacing=types.Spacing.MEDIUM,
                separator=True
            ))
            
        return containers