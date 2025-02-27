"""Factory for creating adaptive card elements with sensible defaults."""

from typing import List, Optional, Union

import adaptive_cards.card_types as types
from adaptive_cards.elements import Image, TextBlock
from adaptive_cards.inputs import InputChoiceSet, InputDate, InputText, InputChoice


class ElementFactory:
    """Factory for creating common adaptive card elements with sensible defaults."""
    
    @staticmethod
    def create_heading(text: str, level: int = 1) -> TextBlock:
        """Create a heading text block with appropriate size based on level.
        
        Args:
            text: The heading text.
            level: Heading level (1-3, where 1 is largest).
            
        Returns:
            A TextBlock configured as a heading.
        """
        sizes = {
            1: types.FontSize.EXTRA_LARGE,
            2: types.FontSize.LARGE,
            3: types.FontSize.MEDIUM
        }
        
        size = sizes.get(level, types.FontSize.MEDIUM)
        
        return TextBlock(
            text=text,
            size=size,
            weight=types.FontWeight.BOLDER,
            wrap=True
        )
    
    @staticmethod
    def create_text(
        text: str, 
        is_subtle: bool = False, 
        weight: Optional[types.FontWeight] = None,
        color: Optional[types.Colors] = None
    ) -> TextBlock:
        """Create a standard text block.
        
        Args:
            text: The text content.
            is_subtle: Whether the text should be displayed with subtle styling.
            weight: Optional font weight.
            color: Optional text color.
            
        Returns:
            A TextBlock with the specified properties.
        """
        return TextBlock(
            text=text,
            wrap=True,
            is_subtle=is_subtle,
            weight=weight,
            color=color
        )
    
    @staticmethod
    def create_important_text(text: str, color: types.Colors = types.Colors.ATTENTION) -> TextBlock:
        """Create a text block styled to draw attention.
        
        Args:
            text: The text content.
            color: The color to use for the text (default is attention/warning color).
            
        Returns:
            A TextBlock styled for emphasis.
        """
        return TextBlock(
            text=text,
            wrap=True,
            weight=types.FontWeight.BOLDER,
            color=color
        )
    
    @staticmethod
    def create_image(
        url: str, 
        alt_text: Optional[str] = None,
        size: Optional[types.ImageSize] = None,
        style: Optional[types.ImageStyle] = None
    ) -> Image:
        """Create an image element.
        
        Args:
            url: The image URL.
            alt_text: Optional alternate text for accessibility.
            size: Optional image size.
            style: Optional image style.
            
        Returns:
            An Image element.
        """
        return Image(
            url=url,
            alt_text=alt_text,
            size=size,
            style=style
        )
    
    @staticmethod
    def create_text_input(
        id: str,
        placeholder: Optional[str] = None,
        is_required: bool = False,
        max_length: Optional[int] = None
    ) -> InputText:
        """Create a text input element.
        
        Args:
            id: The ID for the input element.
            placeholder: Optional placeholder text.
            is_required: Whether the input is required.
            max_length: Optional maximum length for the input.
            
        Returns:
            An InputText element.
        """
        return InputText(
            id=id,
            placeholder=placeholder,
            is_required=is_required,
            max_length=max_length
        )
    
    @staticmethod
    def create_choice_set(
        id: str,
        choices: List[Union[InputChoice, dict]],
        placeholder: Optional[str] = None,
        is_required: bool = False,
        is_multi_select: bool = False
    ) -> InputChoiceSet:
        """Create a choice input element.
        
        Args:
            id: The ID for the input element.
            choices: List of InputChoice objects or dictionaries with "title" and "value" keys.
            placeholder: Optional placeholder text.
            is_required: Whether selection is required.
            is_multi_select: Whether multiple options can be selected.
            
        Returns:
            An InputChoiceSet element.
        """
        # Convert dictionaries to InputChoice objects if needed
        choice_objects = []
        for choice in choices:
            if isinstance(choice, dict):
                choice_objects.append(InputChoice(
                    title=choice["title"],
                    value=choice["value"]
                ))
            else:
                choice_objects.append(choice)
                
        return InputChoiceSet(
            id=id,
            choices=choice_objects,
            placeholder=placeholder,
            is_required=is_required,
            is_multi_select=is_multi_select
        )
    
    @staticmethod
    def create_date_input(
        id: str,
        placeholder: Optional[str] = None,
        is_required: bool = False
    ) -> InputDate:
        """Create a date input element.
        
        Args:
            id: The ID for the input element.
            placeholder: Optional placeholder text.
            is_required: Whether the input is required.
            
        Returns:
            An InputDate element.
        """
        return InputDate(
            id=id,
            placeholder=placeholder,
            is_required=is_required
        )