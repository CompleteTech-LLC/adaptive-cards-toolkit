"""Example usage of the agent toolkit for creating adaptive cards."""

import json
import adaptive_cards.card_types as types
from adaptive_cards.card import AdaptiveCard

from adaptive_cards_toolkit import (
    AgentCardBuilder,
    ElementFactory,
    LayoutHelper,
    DataConnector,
    ValidationUtility,
    TemplateFactory
)


def example_basic_card():
    """Create a basic card using the AgentCardBuilder."""
    builder = AgentCardBuilder()
    
    # Create a simple card
    card = builder.create_basic_card(
        title="Hello from Agent Toolkit",
        message="This is a simple card created using the Agent Toolkit.",
        image_url="https://adaptivecards.io/content/adaptive-card-50.png"
    )
    
    # Validate the card
    validation = builder.validate_card(card)
    print(f"Card validation: {validation['valid']}")
    print(f"Card size: {validation['size']:.2f}KB")
    
    # Get the JSON representation
    card_json = builder.get_json(card)
    print("\nBasic Card JSON:")
    print(card_json)
    
    return card


def example_action_card():
    """Create a card with actions using the AgentCardBuilder."""
    builder = AgentCardBuilder()
    
    # Create a card with actions
    card = builder.create_action_card(
        title="Action Card Example",
        message="This card has multiple action buttons.",
        actions=[
            {
                "type": "open_url",
                "title": "Learn More",
                "url": "https://adaptivecards.io/"
            },
            {
                "type": "submit",
                "title": "Submit Feedback",
                "data": {"action": "feedback"}
            }
        ],
        image_url="https://adaptivecards.io/content/adaptive-card-50.png"
    )
    
    return card


def example_element_factory():
    """Create elements using the ElementFactory."""
    # Create elements
    heading = ElementFactory.create_heading("Element Factory Example", level=1)
    text = ElementFactory.create_text("This demonstrates various elements created with ElementFactory.")
    important = ElementFactory.create_important_text("This is important information!")
    image = ElementFactory.create_image(
        url="https://adaptivecards.io/content/adaptive-card-50.png",
        alt_text="Adaptive Cards Logo"
    )
    
    # Create a card with these elements
    card = AdaptiveCard.new().version("1.5")
    card.add_items([heading, text, important, image])
    
    return card.create()


def example_layout_helper():
    """Create complex layouts using the LayoutHelper."""
    # Create some elements
    title = ElementFactory.create_heading("Layout Helper Example")
    description = ElementFactory.create_text("This card demonstrates various layouts.")
    
    # Create a two-column layout
    column_layout = LayoutHelper.create_two_column_layout(
        left_content=[
            ElementFactory.create_heading("Left Column", level=2),
            ElementFactory.create_text("Content in the left column.")
        ],
        right_content=[
            ElementFactory.create_heading("Right Column", level=2),
            ElementFactory.create_text("Content in the right column.")
        ]
    )
    
    # Create a header-body-footer layout
    header_footer_layout = LayoutHelper.create_header_body_footer_layout(
        header_items=[ElementFactory.create_heading("Section Header", level=2)],
        body_items=[ElementFactory.create_text("This is the main content of the section.")],
        footer_items=[ElementFactory.create_text("Footer information", is_subtle=True)]
    )
    
    # Create a card with these layouts
    card = AdaptiveCard.new().version("1.5")
    card.add_item(title)
    card.add_item(description)
    card.add_item(column_layout)
    card.add_items(header_footer_layout)
    
    return card.create()


def example_data_connector():
    """Convert structured data to card elements using DataConnector."""
    # Sample data
    json_data = {
        "product": "Adaptive Cards",
        "version": "1.5",
        "features": ["Dynamic content", "Rich visuals", "User input"],
        "release_date": "2023-01-15"
    }
    
    # Create a card with data visualization
    card = AdaptiveCard.new().version("1.5")
    card.add_item(ElementFactory.create_heading("Data Connector Example"))
    
    # Add fact set from data
    card.add_item(DataConnector.create_fact_set({
        "Product": json_data["product"],
        "Version": json_data["version"],
        "Release Date": json_data["release_date"]
    }))
    
    # Add list from data
    card.add_item(ElementFactory.create_heading("Features", level=2))
    card.add_items(DataConnector.create_list(json_data["features"]))
    
    # Add two-column layout
    card.add_item(DataConnector.key_value_pairs_to_columns(json_data))
    
    return card.create()


def example_template_factory():
    """Create pre-built card templates using TemplateFactory."""
    # Create a notification card
    notification_card = TemplateFactory.create_notification_card(
        title="New Feature Available",
        message="Adaptive Cards now support advanced layouts!",
        level="info",
        icon_url="https://adaptivecards.io/content/notification-default.png",
        action_url="https://adaptivecards.io/"
    )
    
    # Create a form card
    form_card = TemplateFactory.create_form_card(
        title="Feedback Form",
        subtitle="Please provide your feedback on our service",
        fields=[
            {
                "type": "text",
                "id": "name",
                "label": "Your Name",
                "placeholder": "Enter your name",
                "required": True
            },
            {
                "type": "text",
                "id": "feedback",
                "label": "Your Feedback",
                "placeholder": "Tell us what you think..."
            },
            {
                "type": "choice",
                "id": "rating",
                "label": "Rating",
                "choices": [
                    {"title": "Excellent", "value": "5"},
                    {"title": "Good", "value": "4"},
                    {"title": "Average", "value": "3"},
                    {"title": "Poor", "value": "2"},
                    {"title": "Very Poor", "value": "1"}
                ]
            }
        ],
        submit_label="Submit Feedback"
    )
    
    # Create a dashboard card
    dashboard_card = TemplateFactory.create_dashboard_card(
        title="Monthly Performance",
        metrics={
            "Total Users": "1,234",
            "New Users": "+56",
            "Engagement": "78%",
            "Revenue": "$12,345"
        },
        description="Performance metrics for the current month",
        chart_image_url="https://adaptivecards.io/content/chart.png"
    )
    
    return {
        "notification": notification_card,
        "form": form_card,
        "dashboard": dashboard_card
    }


if __name__ == "__main__":
    # Run the examples
    print("=== Agent Toolkit Examples ===\n")
    
    # Basic card example
    basic_card = example_basic_card()
    
    # Action card example
    action_card = example_action_card()
    print("\nAction Card created successfully.")
    
    # Element factory example
    element_card = example_element_factory()
    print("\nElement Factory Card created successfully.")
    
    # Layout helper example
    layout_card = example_layout_helper()
    print("\nLayout Helper Card created successfully.")
    
    # Data connector example
    data_card = example_data_connector()
    print("\nData Connector Card created successfully.")
    
    # Template factory example
    template_cards = example_template_factory()
    print("\nTemplate Factory Cards created successfully:")
    for template_name in template_cards:
        print(f"- {template_name}")
    
    # Validate all cards
    validator = ValidationUtility()
    print("\n=== Card Validation Results ===")
    
    cards = {
        "Basic Card": basic_card,
        "Action Card": action_card,
        "Element Factory Card": element_card,
        "Layout Helper Card": layout_card,
        "Data Connector Card": data_card,
        "Notification Template": template_cards["notification"],
        "Form Template": template_cards["form"],
        "Dashboard Template": template_cards["dashboard"]
    }
    
    for name, card in cards.items():
        result = validator.validate(card)
        print(f"\n{name}:")
        print(f"  Valid: {result['valid']}")
        print(f"  Size: {result['size']:.2f}KB")
        
        if result['warnings']:
            print("  Warnings:")
            for warning in result['warnings']:
                print(f"    - {warning}")
                
        if not result['valid']:
            print("  Details:")
            for detail in result['details']:
                print(f"    - {detail}")
    
    print("\nAll examples completed successfully.")