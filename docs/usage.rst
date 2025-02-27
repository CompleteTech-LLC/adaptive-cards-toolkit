Usage
=====

Basic Usage
----------

Here's a simple example of creating a notification card:

.. code-block:: python

    from adaptive_cards_toolkit.templates import TemplateFactory
    from adaptive_cards_toolkit.validation_utility import ValidationUtility
    from adaptive_cards_toolkit.delivery_manager import DeliveryManager

    # Create a notification card
    card = TemplateFactory.create_notification_card(
        title="System Maintenance",
        message="The system will be down for maintenance on Saturday from 2-4 PM EST.",
        level="warning"
    )

    # Validate the card
    validator = ValidationUtility()
    result = validator.validate(card)

    if result["valid"]:
        # Send the card (if you have a webhook URL)
        delivery = DeliveryManager(webhook_url="https://your-webhook-url.com")
        delivery.send(card)

Components Overview
------------------

The toolkit consists of several major components:

1. **AgentCardBuilder**: Simplified interface for creating adaptive cards
2. **ElementFactory**: Create card elements with sensible defaults
3. **LayoutHelper**: Build responsive layouts easily
4. **DataConnector**: Convert structured data to card elements
5. **TemplateFactory**: Pre-built templates for common card scenarios
6. **ValidationUtility**: Validate cards before delivery
7. **DeliveryManager**: Send cards to platforms like MS Teams
8. **OpenAI Assistant**: Generate cards using natural language

Examples
--------

Creating a Basic Card
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from adaptive_cards_toolkit.card_builder import AgentCardBuilder

    builder = AgentCardBuilder()
    
    # Create a simple card
    card = builder.create_basic_card(
        title="Hello from Adaptive Cards Toolkit",
        message="This is a simple card created using the Toolkit.",
        image_url="https://adaptivecards.io/content/adaptive-card-50.png"
    )

Working with Elements
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from adaptive_cards.card import AdaptiveCard
    from adaptive_cards_toolkit.element_factory import ElementFactory

    # Create a new card
    card = AdaptiveCard.new().version("1.5")

    # Add heading elements with different levels
    card.add_item(ElementFactory.create_heading("Main Heading", level=1))
    card.add_item(ElementFactory.create_heading("Subheading", level=2))

    # Add regular text
    card.add_item(ElementFactory.create_text("This is regular text content."))

    # Add important text with different colors
    card.add_item(ElementFactory.create_important_text("Warning message", color="warning"))

Creating Complex Layouts
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from adaptive_cards.card import AdaptiveCard
    from adaptive_cards_toolkit.element_factory import ElementFactory
    from adaptive_cards_toolkit.layout_helper import LayoutHelper

    # Create a new card
    card = AdaptiveCard.new().version("1.5")
    
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
    
    card.add_item(column_layout)

Working with Data
~~~~~~~~~~~~~~~~

.. code-block:: python

    from adaptive_cards.card import AdaptiveCard
    from adaptive_cards_toolkit.element_factory import ElementFactory
    from adaptive_cards_toolkit.data_connector import DataConnector

    # Sample data
    json_data = {
        "product": "Adaptive Cards Toolkit",
        "version": "1.0.0",
        "features": ["Easy card creation", "Complex layouts", "Data visualization"]
    }
    
    # Create a card with data visualization
    card = AdaptiveCard.new().version("1.5")
    
    # Add fact set from data
    card.add_item(DataConnector.create_fact_set({
        "Product": json_data["product"],
        "Version": json_data["version"]
    }))
    
    # Add list from data
    card.add_items(DataConnector.create_list(json_data["features"]))

Using Templates
~~~~~~~~~~~~~~

.. code-block:: python

    from adaptive_cards_toolkit.templates import TemplateFactory

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

OpenAI Integration
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from adaptive_cards_toolkit.openai_agent import AdaptiveCardGenerator

    # Initialize with OpenAI API key
    generator = AdaptiveCardGenerator(api_key="your-openai-api-key")

    # Generate card from natural language
    result = generator.generate_card(
        "Create a notification about system maintenance on Saturday from 2-4 PM"
    )

    if result["success"]:
        card = result["card"]
        print(f"Generated card: {result['explanation']}")
        
        # Send to webhook (optional)
        generator.send_card(card, "https://your-webhook-url.com")