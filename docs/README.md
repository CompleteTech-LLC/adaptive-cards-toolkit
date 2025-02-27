# Agent Toolkit for Adaptive Cards

A high-level toolkit designed for AI agents to create, validate, and deliver adaptive cards.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Components](#components)
  - [AgentCardBuilder](#1-agentcardbuilder)
  - [ElementFactory](#2-elementfactory)
  - [LayoutHelper](#3-layouthelper)
  - [DataConnector](#4-dataconnector)
  - [TemplateFactory](#5-templatefactory)
  - [ValidationUtility](#6-validationutility)
  - [DeliveryManager](#7-deliverymanager)
  - [OpenAI Integration](#8-openai-assistant-integration)
- [Example Usage](#example-usage)
- [Advanced Topics](#advanced-topics)
  - [Combining Components](#combining-components)
  - [Performance Optimization](#performance-optimization)
  - [Error Handling](#error-handling)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Best Practices](#best-practices)

## Overview

The Agent Toolkit provides a simplified interface on top of the `adaptive-cards-py` library, making it easier for AI agents and developers to create, validate, and deliver adaptive cards. Whether you need to programmatically create cards or want to generate them using natural language, this toolkit offers a comprehensive solution.

Key features include:

- **High-level abstractions**: Create complex cards with minimal code
- **Pre-built templates**: Common patterns for notifications, forms, dashboards, etc.
- **Component factories**: Create elements with sensible defaults
- **Layout helpers**: Build responsive designs easily
- **Data visualization**: Convert structured data (JSON, CSV) to cards
- **Validation**: Check cards before delivery to prevent errors
- **Delivery management**: Send cards to platforms like MS Teams
- **OpenAI integration**: Generate cards using natural language

### When to use this toolkit

- **For AI agents**: When you need a high-level API to create cards programmatically
- **For developers**: When you want to simplify adaptive card creation and focus on content
- **For applications**: When you need to generate cards from user input or data sources
- **For prototype development**: When you want to quickly experiment with different card designs

## Prerequisites

- Python 3.10 or higher
- `adaptive-cards-py` package
- `requests` for delivery management
- `openai` package (optional, for AI-generated cards)

## Installation

```bash
# First, install the adaptive-cards-py base library
pip install adaptive-cards-py

# For OpenAI integration (optional)
pip install openai
```

## Components

### 1. AgentCardBuilder

The `AgentCardBuilder` class provides a simplified interface for creating adaptive cards with minimal code. It handles the complexities of card initialization, element addition, and validation.

#### Key Features:
- Create basic cards with title, message, and optional image
- Add action buttons (submit or URL opening)
- Validate cards before delivery
- Export cards to JSON

#### Usage:

```python
from tools.agent_toolkit.card_builder import AgentCardBuilder

# Initialize with default card version
builder = AgentCardBuilder(version="1.5")

# Create a basic card
card = builder.create_basic_card(
    title="Hello World",
    message="This is a simple card created with AgentCardBuilder.",
    image_url="https://example.com/image.png"
)

# Create a card with actions
card_with_actions = builder.create_action_card(
    title="Action Card",
    message="This card has interactive buttons",
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
    ]
)

# Validate the card
validation_result = builder.validate_card(card)
if validation_result["valid"]:
    # Get JSON representation
    card_json = builder.get_json(card)
else:
    print(f"Validation failed: {validation_result['details']}")
```

### 2. ElementFactory

The `ElementFactory` class simplifies the creation of common card elements with appropriate defaults, making it easier to create readable, accessible, and visually appealing cards.

#### Key Features:
- Create headings with appropriate styling based on level
- Create text blocks with various formatting options
- Create input elements for forms with proper configuration
- Create images with appropriate sizing and accessibility attributes

#### Usage:

```python
from tools.agent_toolkit.element_factory import ElementFactory
import adaptive_cards.card_types as types

# Create headings of different levels
heading1 = ElementFactory.create_heading("Primary Heading", level=1)
heading2 = ElementFactory.create_heading("Secondary Heading", level=2)
heading3 = ElementFactory.create_heading("Tertiary Heading", level=3)

# Create different text styles
normal_text = ElementFactory.create_text("Standard text content.")
subtle_text = ElementFactory.create_text("Less prominent text.", is_subtle=True)
bold_text = ElementFactory.create_text("Bold text", weight=types.FontWeight.BOLDER)
colored_text = ElementFactory.create_text("Colored text", color=types.Colors.ACCENT)

# Create important text
warning_text = ElementFactory.create_important_text("Warning message!", color=types.Colors.WARNING)

# Create an image
image = ElementFactory.create_image(
    url="https://example.com/image.png",
    alt_text="Descriptive text for accessibility",
    size=types.ImageSize.MEDIUM,
    style=types.ImageStyle.DEFAULT
)

# Create form inputs
text_input = ElementFactory.create_text_input(
    id="name",
    placeholder="Enter your name",
    is_required=True,
    max_length=100
)

date_input = ElementFactory.create_date_input(
    id="birthdate",
    placeholder="Select your birth date",
    is_required=False
)

choice_set = ElementFactory.create_choice_set(
    id="rating",
    choices=[
        {"title": "Excellent", "value": "5"},
        {"title": "Good", "value": "4"},
        {"title": "Average", "value": "3"},
        {"title": "Poor", "value": "2"},
        {"title": "Very Poor", "value": "1"}
    ],
    placeholder="Select a rating",
    is_multi_select=False
)
```

### 3. LayoutHelper

The `LayoutHelper` class provides methods for creating responsive layouts and structured arrangements of elements, making it easier to build visually appealing cards.

#### Key Features:
- Create containers with proper styling and spacing
- Create column-based layouts for responsive design
- Create standard layout patterns like header-body-footer

#### Usage:

```python
from tools.agent_toolkit.layout_helper import LayoutHelper
from tools.agent_toolkit.element_factory import ElementFactory
import adaptive_cards.card_types as types

# Create container with styling
container = LayoutHelper.create_container(
    items=[
        ElementFactory.create_heading("Container Title"),
        ElementFactory.create_text("Container content")
    ],
    style=types.ContainerStyle.EMPHASIS,
    spacing=types.Spacing.MEDIUM,
    separator=True
)

# Create a two-column layout
column_layout = LayoutHelper.create_two_column_layout(
    left_content=[
        ElementFactory.create_heading("Left Column"),
        ElementFactory.create_text("Content on the left")
    ],
    right_content=[
        ElementFactory.create_image("https://example.com/image.png")
    ],
    left_width="stretch",
    right_width="auto"
)

# Create a layout with multiple equal columns
multi_column = LayoutHelper.create_equal_columns([
    [ElementFactory.create_heading("Column 1")],
    [ElementFactory.create_heading("Column 2")],
    [ElementFactory.create_heading("Column 3")]
])

# Create a complete page layout with header, body, and footer
page_layout = LayoutHelper.create_header_body_footer_layout(
    header_items=[
        ElementFactory.create_heading("Page Title")
    ],
    body_items=[
        ElementFactory.create_text("Main content goes here"),
        column_layout  # Nested layouts are supported
    ],
    footer_items=[
        ElementFactory.create_text("© 2025 Example Corp", is_subtle=True)
    ],
    header_style=types.ContainerStyle.EMPHASIS,
    footer_style=types.ContainerStyle.ACCENT
)
```

### 4. DataConnector

The `DataConnector` class provides utilities for converting structured data formats into adaptive card elements, making it easy to create data-driven cards.

#### Key Features:
- Convert dictionaries to fact sets
- Create lists from array data
- Create tables from tabular data
- Parse and visualize JSON and CSV data

#### Usage:

```python
from tools.agent_toolkit.data_connector import DataConnector
from adaptive_cards.card import AdaptiveCard
from tools.agent_toolkit.element_factory import ElementFactory

# Create a fact set from a dictionary
employee_data = {
    "Name": "John Smith",
    "Department": "Engineering",
    "Title": "Senior Developer",
    "Email": "john.smith@example.com"
}
fact_set = DataConnector.create_fact_set(employee_data)

# Create a list from array data
todo_items = ["Complete project", "Schedule meeting", "Send report"]
todo_list = DataConnector.create_list(todo_items, is_numbered=True)

# Create a table from tabular data
headers = ["Name", "Department", "Role"]
rows = [
    ["John", "Engineering", "Developer"],
    ["Jane", "Marketing", "Manager"],
    ["Bob", "Sales", "Director"]
]
table = DataConnector.create_table(
    headers=headers,
    rows=rows,
    column_widths=["stretch", 1, 1],
    alternate_row_style=True
)

# Convert complex JSON data to card elements
json_data = {
    "project": "Adaptive Cards Integration",
    "tasks": [
        {"name": "Research", "status": "Completed", "assignee": "John"},
        {"name": "Implementation", "status": "In Progress", "assignee": "Jane"},
        {"name": "Testing", "status": "Not Started", "assignee": "Bob"}
    ],
    "deadline": "2023-12-31"
}
json_elements = DataConnector.from_json(json_data)

# Convert CSV data to card elements
csv_data = """Name,Department,Role
John,Engineering,Developer
Jane,Marketing,Manager
Bob,Sales,Director"""
csv_elements = DataConnector.from_csv(csv_data)

# Create a two-column key-value layout
key_value_layout = DataConnector.key_value_pairs_to_columns(
    employee_data,
    key_width=1,
    value_width=2
)

# Create a card with data visualization
card = AdaptiveCard.new().version("1.5")
card.add_item(ElementFactory.create_heading("Employee Information"))
card.add_item(fact_set)
card.add_item(ElementFactory.create_heading("Tasks", level=2))
card.add_items(todo_list)
card.add_item(ElementFactory.create_heading("Team Members", level=2))
card.add_items(table)
card.create()
```

### 5. TemplateFactory

The `TemplateFactory` class provides pre-built templates for common card scenarios, allowing quick creation of well-designed cards for specific purposes.

#### Available Templates:
- **Notification Card**: For alerts, announcements, and notices
- **Form Card**: For collecting user input with various field types
- **Article Card**: For displaying content with title, body, and optional image
- **Dashboard Card**: For displaying metrics and KPIs
- **Confirmation Card**: For confirming user actions with approve/deny buttons

#### Usage:

```python
from tools.agent_toolkit.templates import TemplateFactory

# Create a notification card
notification = TemplateFactory.create_notification_card(
    title="System Update",
    message="The system will be down for maintenance on Saturday from 2-4 PM EST.",
    level="warning",  # "info", "warning", "success", or "danger"
    icon_url="https://example.com/warning-icon.png",
    action_url="https://example.com/details"
)

# Create a form card
form = TemplateFactory.create_form_card(
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
            "id": "email",
            "label": "Email Address",
            "placeholder": "Enter your email"
        },
        {
            "type": "choice",
            "id": "rating",
            "label": "Rate our service",
            "choices": [
                {"title": "Excellent", "value": "5"},
                {"title": "Good", "value": "4"},
                {"title": "Average", "value": "3"},
                {"title": "Poor", "value": "2"},
                {"title": "Very Poor", "value": "1"}
            ]
        },
        {
            "type": "date",
            "id": "visit_date",
            "label": "Date of Visit"
        }
    ],
    submit_label="Submit Feedback"
)

# Create an article card
article = TemplateFactory.create_article_card(
    title="Introducing Adaptive Cards",
    content="Adaptive Cards are a open card exchange format enabling developers to exchange UI content in a common and consistent way.",
    image_url="https://example.com/adaptive-cards.png",
    author="Adaptive Cards Team",
    date="January 15, 2023",
    action_url="https://adaptivecards.io/"
)

# Create a dashboard card
dashboard = TemplateFactory.create_dashboard_card(
    title="Monthly Performance",
    metrics={
        "Total Users": "1,234",
        "New Users": "+56",
        "Active Users": "789",
        "Retention Rate": "92%",
        "Revenue": "$12,345"
    },
    description="Key metrics for January 2023",
    chart_image_url="https://example.com/chart.png"
)

# Create a confirmation card
confirmation = TemplateFactory.create_confirmation_card(
    title="Confirm Deletion",
    message="Are you sure you want to delete this item? This action cannot be undone.",
    confirm_button_text="Yes, Delete It",
    cancel_button_text="Cancel"
)
```

### 6. ValidationUtility

The `ValidationUtility` class provides tools for validating and optimizing adaptive cards before delivery, ensuring compatibility with target platforms.

#### Key Features:
- Validate cards against target platform requirements
- Get card size and check against platform limits
- Get warnings and suggestions for optimization
- Identify and report schema validation issues

#### Usage:

```python
from tools.agent_toolkit.validation_utility import ValidationUtility

# Initialize for specific target platform
validator = ValidationUtility(target="teams")  # Default is "teams"

# Validate a card
validation_result = validator.validate(card)

# Check validation status
if validation_result["valid"]:
    print(f"Card is valid for {validator.target}")
    print(f"Card size: {validation_result['size']:.2f}KB")
else:
    print(f"Card validation failed:")
    for detail in validation_result["details"]:
        print(f"- {detail}")

# Check for warnings (issues that don't invalidate the card)
if validation_result["warnings"]:
    print("\nWarnings:")
    for warning in validation_result["warnings"]:
        print(f"- {warning}")

# Get optimization suggestions
if validation_result["suggestions"]:
    print("\nOptimization suggestions:")
    for suggestion in validation_result["suggestions"]:
        print(f"- {suggestion}")

# Get just the size of a card
size = validator.get_size(card)
print(f"Card size: {size:.2f}KB")

# Get optimization suggestions for a large card
suggestions = validator.suggest_optimizations(card)
for suggestion in suggestions:
    print(f"- {suggestion}")
```

### 7. DeliveryManager

The `DeliveryManager` class manages the delivery of adaptive cards to various platforms, with built-in validation and error handling.

#### Key Features:
- Send cards to Microsoft Teams
- Validate cards before sending
- Handle delivery errors gracefully
- Configure and update webhook endpoints

#### Usage:

```python
from tools.agent_toolkit.delivery_manager import DeliveryManager

# Initialize with webhook URL
manager = DeliveryManager(webhook_url="https://your-teams-webhook.com")

# Validate before sending
validation_result = manager.validate_before_send(card)
if validation_result["valid"]:
    # Send the card
    delivery_result = manager.send(card)
    
    if delivery_result["success"]:
        print(f"Card delivered successfully!")
        print(f"Status code: {delivery_result['status_code']}")
    else:
        print(f"Delivery failed: {delivery_result['message']}")
else:
    print("Card validation failed. Fix the following issues:")
    for detail in validation_result["details"]:
        print(f"- {detail}")

# Initialize without URL and set it later
manager = DeliveryManager()
# ... later in the code
manager.set_webhook_url("https://new-webhook-url.com")

# Send with automatic validation
result = manager.send(card, validate=True)

# Send without validation (faster)
result = manager.send(card, validate=False)
```

### 8. OpenAI Assistant Integration

The `AdaptiveCardGenerator` class leverages the OpenAI Assistant API to generate adaptive cards from natural language descriptions, making card creation accessible to non-technical users.

#### Key Features:
- Generate cards using natural language descriptions
- AI-powered selection of appropriate card templates
- Explanation of design choices
- Validation before delivery
- Command-line interface for quick generation

#### Usage:

```python
from tools.agent_toolkit.openai_agent import AdaptiveCardGenerator

# Initialize with your OpenAI API key
generator = AdaptiveCardGenerator(api_key="your-openai-api-key")
# Or use environment variable: export OPENAI_API_KEY="your-key"

# Generate a card based on a natural language prompt
result = generator.generate_card(
    "Create a dashboard card showing sales metrics with total revenue of $10,245, 
     156 new customers, and 89% customer satisfaction"
)

if result["success"]:
    # Access the generated card
    card = result["card"]
    card_json = result["card_json"]
    explanation = result["explanation"]
    
    print("Card generated successfully!")
    print(f"Design explanation: {explanation}")
    
    # Optionally send the card to a webhook
    delivery_result = generator.send_card(card, "https://your-webhook-url.com")
    print(f"Delivery success: {delivery_result['success']}")
else:
    print(f"Generation failed: {result['error']}")
```

#### Command-line Interface:

```bash
# Basic usage
python -m tools.agent_toolkit.openai_example --prompt "Create a notification card for system maintenance"

# Specify output file
python -m tools.agent_toolkit.openai_example --prompt "Create a form for user feedback" --output feedback_form.json

# Send to webhook
python -m tools.agent_toolkit.openai_example --prompt "Create an alert about server issues" --webhook "https://your-webhook-url.com"
```

## Example Usage

For complete examples of each component, refer to:

- `example.py`: Demonstrates usage of core toolkit components
- `openai_example.py`: Shows how to generate cards with OpenAI

## Advanced Topics

### Combining Components

The toolkit components are designed to work together seamlessly:

```python
from tools.agent_toolkit.card_builder import AgentCardBuilder
from tools.agent_toolkit.element_factory import ElementFactory
from tools.agent_toolkit.layout_helper import LayoutHelper
from tools.agent_toolkit.data_connector import DataConnector
from tools.agent_toolkit.validation_utility import ValidationUtility
from tools.agent_toolkit.delivery_manager import DeliveryManager

# Create elements
title = ElementFactory.create_heading("Project Status")
description = ElementFactory.create_text("Current status of all projects")

# Create data visualization
project_data = [
    {"name": "Alpha", "status": "Complete", "progress": "100%"},
    {"name": "Beta", "status": "In Progress", "progress": "65%"},
    {"name": "Gamma", "status": "Not Started", "progress": "0%"}
]
data_elements = DataConnector.from_json(project_data)

# Create layout
content = LayoutHelper.create_container(
    items=[title, description] + data_elements,
    style="emphasis"
)

# Initialize card builder
builder = AgentCardBuilder()
card = builder.create_basic_card(
    title="Project Dashboard", 
    message=""
)
card.body.append(content)

# Validate before sending
validator = ValidationUtility()
result = validator.validate(card)

if result["valid"]:
    # Send to Teams
    delivery = DeliveryManager(webhook_url="https://your-webhook.com")
    delivery.send(card)
```

### Performance Optimization

To improve performance when generating multiple cards:

1. **Reuse component instances**:
   - Create a single instance of each factory/helper
   - Reuse these instances across multiple card creations

2. **Minimize validation**:
   - Only validate final cards before delivery
   - Use `validate=False` for DeliveryManager when templates are known to be valid

3. **Batch data processing**:
   - When converting large datasets, process in batches
   - Consider pagination for very large data sets

### Error Handling

The toolkit provides robust error handling:

```python
try:
    # Create and send card
    card = builder.create_basic_card(title="Test", message="Testing error handling")
    result = delivery.send(card)
    
    if not result["success"]:
        # Handle delivery failure
        if "validation" in result:
            # Handle validation failure
            print(f"Validation failed: {result['validation']['details']}")
        else:
            # Handle delivery error
            print(f"Delivery error: {result['message']}")
            
except Exception as e:
    # Handle unexpected errors
    print(f"Error: {str(e)}")
```

## Testing

The toolkit includes a comprehensive test suite:

```bash
# Run all tests
python -m tools.agent_toolkit.tests.run_tests

# Run specific test module
python -m unittest tools.agent_toolkit.tests.test_card_builder

# Run tests with higher verbosity
python -m tools.agent_toolkit.tests.run_tests --verbosity 2
```

## Contributing

Contributions are welcome! When contributing:

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation
4. Run the test suite before submitting changes

## License

This toolkit is licensed under the same license as the adaptive-cards-py package.

## Best Practices

1. **Start with templates** for common scenarios
2. **Validate cards** before sending to ensure compatibility 
3. **Use layout helpers** for responsive designs
4. **Structure data** with DataConnector for clean visualization
5. **Keep cards concise** to avoid size limitations
6. **Add IDs to elements** that need to be referenced or manipulated
7. **Handle delivery errors** gracefully
8. **Optimize image sizes** to reduce card size
9. **Test cards across platforms** to ensure compatibility
10. **Consider using AI generation** for rapid prototyping