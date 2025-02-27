"""Pre-built templates for common adaptive card scenarios."""

from typing import Any, Dict, List, Optional, Union

import adaptive_cards.card_types as types
from adaptive_cards.actions import ActionOpenUrl, ActionSubmit
from adaptive_cards.card import AdaptiveCard
from adaptive_cards.containers import Container, FactSet, Fact
from adaptive_cards.elements import Image, TextBlock
from adaptive_cards.inputs import InputText as TextInput, InputDate as DateInput, InputChoiceSet as ChoiceSet, InputChoice as Choice

from adaptive_cards_toolkit.core.element_factory import ElementFactory
from adaptive_cards_toolkit.core.layout_helper import LayoutHelper


class TemplateFactory:
    """Factory for pre-built adaptive card templates."""
    
    @staticmethod
    def create_notification_card(
        title: str,
        message: str,
        level: Optional[str] = None,
        icon_url: Optional[str] = None,
        action_url: Optional[str] = None
    ) -> AdaptiveCard:
        """Create a simple notification card.
        
        Args:
            title: The notification title.
            message: The notification message.
            level: Optional notification level ("info", "warning", "success", "danger").
            icon_url: Optional URL for an icon.
            action_url: Optional URL for the card's action.
            
        Returns:
            An AdaptiveCard configured as a notification.
        """
        # Map notification levels to colors
        color_map = {
            "info": types.Colors.ACCENT,
            "warning": types.Colors.WARNING,
            "success": types.Colors.GOOD,
            "danger": types.Colors.ATTENTION
        }
        
        card = AdaptiveCard.new().version("1.5")
        
        # Create header with icon if provided
        if icon_url:
            header_items = LayoutHelper.create_two_column_layout(
                left_content=[ElementFactory.create_heading(title)],
                right_content=[ElementFactory.create_image(icon_url, size=types.ImageSize.SMALL)],
                left_width="stretch",
                right_width="auto"
            )
            card.add_item(header_items)
        else:
            card.add_item(ElementFactory.create_heading(title))
        
        # Add message with appropriate styling
        message_text = TextBlock(
            text=message,
            wrap=True,
            color=color_map.get(level) if level in color_map else None
        )
        card.add_item(message_text)
        
        # Add action if URL provided
        if action_url:
            card.add_action(ActionOpenUrl(
                title="View Details",
                url=action_url
            ))
        
        return card.create()
    
    @staticmethod
    def create_form_card(
        title: str,
        fields: List[Dict[str, Any]],
        submit_label: str = "Submit",
        subtitle: Optional[str] = None
    ) -> AdaptiveCard:
        """Create a form card with input fields.
        
        Args:
            title: The form title.
            fields: List of field dictionaries with these keys:
                - type: Field type ("text", "date", "choice")
                - id: Field ID
                - label: Field label
                - placeholder: Optional placeholder text
                - required: Whether the field is required (default: False)
                - choices: List of choices for choice fields (list of dicts with "title" and "value" keys)
                - multi_select: Whether multiple choices can be selected (default: False)
            submit_label: Label for the submit button.
            subtitle: Optional subtitle for the form.
            
        Returns:
            An AdaptiveCard configured as a form.
        """
        card = AdaptiveCard.new().version("1.5")
        
        # Add title
        card.add_item(ElementFactory.create_heading(title))
        
        # Add subtitle if provided
        if subtitle:
            card.add_item(ElementFactory.create_text(subtitle, is_subtle=True))
            
        # Add each field
        for field in fields:
            # Add label
            card.add_item(TextBlock(
                text=field.get("label", ""),
                wrap=True,
                spacing=types.Spacing.MEDIUM
            ))
            
            field_type = field.get("type", "text").lower()
            field_id = field.get("id", "")
            is_required = field.get("required", False)
            placeholder = field.get("placeholder", "")
            
            # Add appropriate input based on type
            if field_type == "text":
                card.add_item(TextInput(
                    id=field_id,
                    placeholder=placeholder,
                    is_required=is_required,
                    max_length=field.get("max_length")
                ))
            elif field_type == "date":
                card.add_item(DateInput(
                    id=field_id,
                    placeholder=placeholder,
                    is_required=is_required
                ))
            elif field_type == "choice":
                choices = []
                for choice in field.get("choices", []):
                    choices.append(Choice(
                        title=choice.get("title", ""),
                        value=choice.get("value", "")
                    ))
                    
                card.add_item(ChoiceSet(
                    id=field_id,
                    choices=choices,
                    is_multi_select=field.get("multi_select", False),
                    placeholder=placeholder,
                    is_required=is_required
                ))
                
        # Add submit button
        card.add_action(ActionSubmit(
            title=submit_label,
            data={"form_id": title.lower().replace(" ", "_")}
        ))
        
        return card.create()
    
    @staticmethod
    def create_article_card(
        title: str,
        content: str,
        image_url: Optional[str] = None,
        author: Optional[str] = None,
        date: Optional[str] = None,
        action_url: Optional[str] = None
    ) -> AdaptiveCard:
        """Create a card that displays an article or news item.
        
        Args:
            title: The article title.
            content: The article content.
            image_url: Optional URL for a header image.
            author: Optional author name.
            date: Optional date string.
            action_url: Optional URL for "Read more" action.
            
        Returns:
            An AdaptiveCard configured as an article.
        """
        card = AdaptiveCard.new().version("1.5")
        
        # Add image if provided
        if image_url:
            card.add_item(Image(
                url=image_url,
                alt_text=title,
                size=types.ImageSize.LARGE
            ))
            
        # Add title
        card.add_item(ElementFactory.create_heading(title))
        
        # Add metadata (author and date)
        if author or date:
            metadata = ""
            if author:
                metadata += f"By {author}"
            if date:
                metadata += f" | {date}" if author else date
                
            card.add_item(TextBlock(
                text=metadata,
                is_subtle=True,
                spacing=types.Spacing.SMALL
            ))
            
        # Add content
        card.add_item(TextBlock(
            text=content,
            wrap=True,
            spacing=types.Spacing.MEDIUM
        ))
        
        # Add action if URL provided
        if action_url:
            card.add_action(ActionOpenUrl(
                title="Read More",
                url=action_url
            ))
            
        return card.create()
    
    @staticmethod
    def create_dashboard_card(
        title: str,
        metrics: Dict[str, Any],
        description: Optional[str] = None,
        chart_image_url: Optional[str] = None
    ) -> AdaptiveCard:
        """Create a card that displays dashboard metrics.
        
        Args:
            title: The dashboard title.
            metrics: Dictionary of metric names and values.
            description: Optional description text.
            chart_image_url: Optional URL for a chart image.
            
        Returns:
            An AdaptiveCard configured as a dashboard.
        """
        card = AdaptiveCard.new().version("1.5")
        
        # Create header
        header_container = Container(
            items=[ElementFactory.create_heading(title)],
            style=types.ContainerStyle.EMPHASIS,
            bleed=True
        )
        card.add_item(header_container)
        
        # Add description if provided
        if description:
            card.add_item(TextBlock(
                text=description,
                wrap=True,
                spacing=types.Spacing.MEDIUM
            ))
            
        # Create metrics as facts
        facts = []
        for key, value in metrics.items():
            facts.append(Fact(title=key, value=str(value)))
            
        card.add_item(FactSet(facts=facts))
        
        # Add chart if provided
        if chart_image_url:
            card.add_item(Image(
                url=chart_image_url,
                alt_text="Chart",
                size=types.ImageSize.LARGE,
                separator=True
            ))
            
        return card.create()
    
    @staticmethod
    def create_confirmation_card(
        title: str,
        message: str,
        confirm_button_text: str = "Confirm",
        cancel_button_text: str = "Cancel",
        action_data: Optional[Dict[str, Any]] = None
    ) -> AdaptiveCard:
        """Create a card that requests confirmation for an action.
        
        Args:
            title: The confirmation title.
            message: The confirmation message.
            confirm_button_text: Text for the confirm button.
            cancel_button_text: Text for the cancel button.
            action_data: Optional data to include with the submit action.
            
        Returns:
            An AdaptiveCard configured as a confirmation dialog.
        """
        card = AdaptiveCard.new().version("1.5")
        
        # Add title
        card.add_item(ElementFactory.create_heading(title))
        
        # Add message
        card.add_item(TextBlock(
            text=message,
            wrap=True,
            spacing=types.Spacing.MEDIUM
        ))
        
        # Add confirm button
        confirm_data = {"action": "confirm"}
        if action_data:
            confirm_data.update(action_data)
            
        card.add_action(ActionSubmit(
            title=confirm_button_text,
            style=types.ActionStyle.POSITIVE,
            data=confirm_data
        ))
        
        # Add cancel button
        card.add_action(ActionSubmit(
            title=cancel_button_text,
            style=types.ActionStyle.DEFAULT,
            data={"action": "cancel"}
        ))
        
        return card.create()