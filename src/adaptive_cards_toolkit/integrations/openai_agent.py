"""OpenAI Assistant agent for creating adaptive cards."""

import json
import os
import time
from typing import Any, Dict, List, Optional, Union

from openai import OpenAI

from adaptive_cards_toolkit.core.card_builder import AgentCardBuilder
from adaptive_cards_toolkit.core.element_factory import ElementFactory
from adaptive_cards_toolkit.core.layout_helper import LayoutHelper
from adaptive_cards_toolkit.core.data_connector import DataConnector
from adaptive_cards_toolkit.core.validation_utility import ValidationUtility
from adaptive_cards_toolkit.templates.templates import TemplateFactory
from adaptive_cards_toolkit.delivery.delivery_manager import DeliveryManager


class AdaptiveCardGenerator:
    """Agent that uses OpenAI Assistant API to generate adaptive cards."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """Initialize the adaptive card generator.
        
        Args:
            api_key: Optional OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
            model: The OpenAI model to use.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Provide as parameter or set OPENAI_API_KEY env var.")
            
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        
        # Initialize tools
        self.card_builder = AgentCardBuilder()
        self.validator = ValidationUtility()
        
        # Create or retrieve the assistant
        self.assistant = self._create_or_get_assistant()
        
    def _create_or_get_assistant(self):
        """Create a new assistant or retrieve existing one."""
        # Define the assistant's instructions
        instructions = """
        You are an adaptive card design expert. Your job is to create visually appealing, 
        informative and effective adaptive cards based on user requirements.
        
        You have access to a toolkit that helps you create adaptive cards. You can:
        1. Create cards from templates (notification, form, article, dashboard, confirmation)
        2. Build custom cards with specific elements and layouts
        3. Validate cards before delivery
        4. Convert structured data into card visualizations
        
        When designing cards:
        - Keep them concise and focused
        - Use appropriate colors, spacing, and typography
        - Ensure they are accessible and responsive
        - Follow best practices for the target platform
        
        Always provide a brief explanation of your design choices.
        """
        
        # Define the function schemas for the assistant
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_notification_card",
                    "description": "Create a simple notification card",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The notification title"
                            },
                            "message": {
                                "type": "string",
                                "description": "The notification message"
                            },
                            "level": {
                                "type": "string",
                                "enum": ["info", "warning", "success", "danger"],
                                "description": "Optional notification level"
                            },
                            "icon_url": {
                                "type": "string",
                                "description": "Optional URL for an icon"
                            },
                            "action_url": {
                                "type": "string",
                                "description": "Optional URL for the card's action"
                            }
                        },
                        "required": ["title", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_form_card",
                    "description": "Create a form card with input fields",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The form title"
                            },
                            "fields": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["text", "date", "choice"],
                                            "description": "Field type"
                                        },
                                        "id": {
                                            "type": "string",
                                            "description": "Field ID"
                                        },
                                        "label": {
                                            "type": "string",
                                            "description": "Field label"
                                        },
                                        "placeholder": {
                                            "type": "string",
                                            "description": "Optional placeholder text"
                                        },
                                        "required": {
                                            "type": "boolean",
                                            "description": "Whether the field is required"
                                        },
                                        "choices": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "title": {"type": "string"},
                                                    "value": {"type": "string"}
                                                }
                                            },
                                            "description": "List of choices for choice fields"
                                        },
                                        "multi_select": {
                                            "type": "boolean",
                                            "description": "Whether multiple choices can be selected"
                                        }
                                    },
                                    "required": ["type", "id", "label"]
                                },
                                "description": "List of field configurations"
                            },
                            "submit_label": {
                                "type": "string",
                                "description": "Label for the submit button"
                            },
                            "subtitle": {
                                "type": "string",
                                "description": "Optional subtitle for the form"
                            }
                        },
                        "required": ["title", "fields"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_article_card",
                    "description": "Create a card that displays an article or news item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The article title"
                            },
                            "content": {
                                "type": "string",
                                "description": "The article content"
                            },
                            "image_url": {
                                "type": "string",
                                "description": "Optional URL for a header image"
                            },
                            "author": {
                                "type": "string",
                                "description": "Optional author name"
                            },
                            "date": {
                                "type": "string",
                                "description": "Optional date string"
                            },
                            "action_url": {
                                "type": "string",
                                "description": "Optional URL for 'Read more' action"
                            }
                        },
                        "required": ["title", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_dashboard_card",
                    "description": "Create a card that displays dashboard metrics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string", 
                                "description": "The dashboard title"
                            },
                            "metrics": {
                                "type": "object",
                                "description": "Dictionary of metric names and values"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description text"
                            },
                            "chart_image_url": {
                                "type": "string",
                                "description": "Optional URL for a chart image"
                            }
                        },
                        "required": ["title", "metrics"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_confirmation_card",
                    "description": "Create a card that requests confirmation for an action",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The confirmation title"
                            },
                            "message": {
                                "type": "string",
                                "description": "The confirmation message"
                            },
                            "confirm_button_text": {
                                "type": "string",
                                "description": "Text for the confirm button"
                            },
                            "cancel_button_text": {
                                "type": "string",
                                "description": "Text for the cancel button"
                            }
                        },
                        "required": ["title", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_custom_card",
                    "description": "Create a custom card with specified elements and layout",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "elements": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["heading", "text", "image", "container", "column_set", "fact_set"],
                                            "description": "Element type"
                                        },
                                        "content": {
                                            "type": "object",
                                            "description": "Element-specific configuration"
                                        }
                                    },
                                    "required": ["type", "content"]
                                },
                                "description": "List of elements to include in the card"
                            },
                            "actions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "type": {
                                            "type": "string",
                                            "enum": ["open_url", "submit"],
                                            "description": "Action type"
                                        },
                                        "title": {
                                            "type": "string",
                                            "description": "Action button text"
                                        },
                                        "url": {
                                            "type": "string",
                                            "description": "URL for open_url actions"
                                        },
                                        "data": {
                                            "type": "object",
                                            "description": "Data payload for submit actions"
                                        }
                                    },
                                    "required": ["type", "title"]
                                },
                                "description": "List of actions to include in the card"
                            }
                        },
                        "required": ["elements"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "visualize_data",
                    "description": "Convert structured data into card elements",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "data_format": {
                                "type": "string",
                                "enum": ["json", "csv", "key_value", "list", "table"],
                                "description": "Format of the data to visualize"
                            },
                            "data": {
                                "type": "string",
                                "description": "The data to visualize (as a string)"
                            },
                            "title": {
                                "type": "string",
                                "description": "Optional title for the visualization"
                            }
                        },
                        "required": ["data_format", "data"]
                    }
                }
            }
        ]
        
        # Check if we already have created this assistant
        assistants = self.client.beta.assistants.list(limit=100)
        for assistant in assistants.data:
            if assistant.name == "Adaptive Card Designer":
                return assistant
                
        # Create a new assistant if not found
        return self.client.beta.assistants.create(
            name="Adaptive Card Designer",
            instructions=instructions,
            tools=tools,
            model=self.model
        )
        
    def _execute_function(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the requested function and return the result.
        
        Args:
            name: The function name.
            arguments: The function arguments.
            
        Returns:
            Dictionary with function result.
        """
        result = {"success": False, "error": None, "card": None, "card_json": None}
        
        try:
            if name == "create_notification_card":
                card = TemplateFactory.create_notification_card(**arguments)
                
            elif name == "create_form_card":
                card = TemplateFactory.create_form_card(**arguments)
                
            elif name == "create_article_card":
                card = TemplateFactory.create_article_card(**arguments)
                
            elif name == "create_dashboard_card":
                card = TemplateFactory.create_dashboard_card(**arguments)
                
            elif name == "create_confirmation_card":
                card = TemplateFactory.create_confirmation_card(**arguments)
                
            elif name == "create_custom_card":
                # This requires more complex handling of the custom elements
                card = self._create_custom_card(arguments)
                
            elif name == "visualize_data":
                # Convert and visualize the data
                card = self._visualize_data(arguments)
                
            else:
                raise ValueError(f"Unknown function: {name}")
                
            # Validate the card
            validation = self.validator.validate(card)
            
            # Build the result
            result["success"] = True
            result["card"] = card
            result["card_json"] = json.loads(card.to_json()) 
            result["validation"] = validation
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            
        return result
    
    def _create_custom_card(self, arguments: Dict[str, Any]) -> Any:
        """Create a custom card with specified elements.
        
        Args:
            arguments: The function arguments.
            
        Returns:
            An AdaptiveCard instance.
        """
        card = self.card_builder.card_builder.new().version(self.card_builder.version)
        
        # Add each element
        for element_config in arguments.get("elements", []):
            element_type = element_config.get("type")
            content = element_config.get("content", {})
            
            if element_type == "heading":
                element = ElementFactory.create_heading(
                    text=content.get("text", ""),
                    level=content.get("level", 1)
                )
                card.add_item(element)
                
            elif element_type == "text":
                element = ElementFactory.create_text(
                    text=content.get("text", ""),
                    is_subtle=content.get("is_subtle", False)
                )
                card.add_item(element)
                
            elif element_type == "image":
                element = ElementFactory.create_image(
                    url=content.get("url", ""),
                    alt_text=content.get("alt_text")
                )
                card.add_item(element)
                
            # Add more element types as needed
        
        # Add actions if specified
        for action_config in arguments.get("actions", []):
            action_type = action_config.get("type")
            
            if action_type == "open_url":
                action = {
                    "type": "open_url",
                    "title": action_config.get("title", ""),
                    "url": action_config.get("url", "")
                }
                card.add_action(action)
                
            elif action_type == "submit":
                action = {
                    "type": "submit",
                    "title": action_config.get("title", ""),
                    "data": action_config.get("data", {})
                }
                card.add_action(action)
        
        return card.create()
    
    def _visualize_data(self, arguments: Dict[str, Any]) -> Any:
        """Visualize data as a card.
        
        Args:
            arguments: The function arguments.
            
        Returns:
            An AdaptiveCard instance.
        """
        data_format = arguments.get("data_format")
        data_str = arguments.get("data")
        title = arguments.get("title", "Data Visualization")
        
        card = self.card_builder.card_builder.new().version(self.card_builder.version)
        
        # Add title
        card.add_item(ElementFactory.create_heading(title))
        
        # Process data based on format
        if data_format == "json":
            try:
                json_data = json.loads(data_str)
                elements = DataConnector.from_json(json_data)
                card.add_items(elements)
            except json.JSONDecodeError:
                card.add_item(ElementFactory.create_text("Invalid JSON data"))
                
        elif data_format == "csv":
            elements = DataConnector.from_csv(data_str)
            card.add_items(elements)
            
        elif data_format == "key_value":
            try:
                data_dict = json.loads(data_str)
                if isinstance(data_dict, dict):
                    column_set = DataConnector.key_value_pairs_to_columns(data_dict)
                    card.add_item(column_set)
                else:
                    card.add_item(ElementFactory.create_text("Invalid key-value data"))
            except json.JSONDecodeError:
                card.add_item(ElementFactory.create_text("Invalid key-value data"))
                
        elif data_format == "list":
            try:
                items = json.loads(data_str)
                if isinstance(items, list):
                    is_numbered = arguments.get("numbered", False)
                    elements = DataConnector.create_list([str(item) for item in items], is_numbered)
                    card.add_items(elements)
                else:
                    card.add_item(ElementFactory.create_text("Invalid list data"))
            except json.JSONDecodeError:
                card.add_item(ElementFactory.create_text("Invalid list data"))
                
        elif data_format == "table":
            try:
                table_data = json.loads(data_str)
                if isinstance(table_data, dict) and "headers" in table_data and "rows" in table_data:
                    elements = DataConnector.create_table(
                        headers=table_data["headers"],
                        rows=table_data["rows"]
                    )
                    card.add_items(elements)
                else:
                    card.add_item(ElementFactory.create_text("Invalid table data"))
            except json.JSONDecodeError:
                card.add_item(ElementFactory.create_text("Invalid table data"))
        
        return card.create()
    
    def generate_card(self, user_prompt: str, max_tries: int = 3) -> Dict[str, Any]:
        """Generate an adaptive card based on the user prompt.
        
        Args:
            user_prompt: The user's request for a card.
            max_tries: Maximum number of attempts to generate a valid card.
            
        Returns:
            Dictionary with the generation result:
                "success": Boolean indicating if generation was successful
                "card": The generated card object (if successful)
                "card_json": The card as JSON (if successful)
                "explanation": The agent's explanation of design choices
                "error": Error message (if unsuccessful)
        """
        result = {
            "success": False,
            "card": None,
            "card_json": None,
            "explanation": "",
            "error": None
        }
        
        # Create a thread
        thread = self.client.beta.threads.create()
        
        # Add the user message to the thread
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_prompt
        )
        
        # Track number of tries
        tries = 0
        
        while tries < max_tries:
            tries += 1
            
            # Run the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=self.assistant.id
            )
            
            # Poll for completion
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                
                if run_status.status == "completed":
                    break
                elif run_status.status == "requires_action":
                    # Handle function calls
                    tool_outputs = []
                    for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)
                        
                        # Execute the function
                        function_result = self._execute_function(function_name, arguments)
                        
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(function_result)
                        })
                    
                    # Submit tool outputs back to the assistant
                    self.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    
                elif run_status.status == "failed":
                    result["error"] = f"Run failed: {run_status.last_error}"
                    return result
                    
                # Wait before polling again
                time.sleep(0.5)
            
            # Retrieve messages
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.id
            )
            
            # Extract the latest assistant message
            for message in messages.data:
                if message.role == "assistant":
                    # Look for the card in the message annotations or attachments
                    card_data = None
                    explanation = ""
                    
                    # Extract the message content
                    for content in message.content:
                        if content.type == "text":
                            explanation += content.text.value
                    
                    # Check if there's function call data in the message
                    annotations = []
                    for content in message.content:
                        if content.type == "text":
                            annotations.extend(content.text.annotations)
                    
                    # Extract file citation
                    for annotation in annotations:
                        if annotation.type == "file_citation":
                            file_id = annotation.file_citation.file_id
                            # Retrieve file content if needed
                    
                    # If we have a card in the tool results
                    for run_step in self.client.beta.threads.runs.steps.list(
                        thread_id=thread.id,
                        run_id=run.id
                    ).data:
                        if hasattr(run_step, "step_details") and hasattr(run_step.step_details, "tool_calls"):
                            for tool_call in run_step.step_details.tool_calls:
                                if hasattr(tool_call, "function") and tool_call.function.output:
                                    try:
                                        output = json.loads(tool_call.function.output)
                                        if output.get("success") and output.get("card_json"):
                                            card_data = output
                                            break
                                    except:
                                        pass
                    
                    if card_data:
                        result["success"] = True
                        result["card"] = card_data.get("card")
                        result["card_json"] = card_data.get("card_json")
                        result["explanation"] = explanation
                        return result
                    
                    break
            
            # If we reach here, we need to ask for clarification and try again
            if tries < max_tries:
                self.client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content="I need a valid adaptive card. Please try again with one of the card templates or a custom card."
                )
        
        result["error"] = "Maximum number of tries reached without generating a valid card."
        return result
    
    def send_card(self, card, webhook_url: str) -> Dict[str, Any]:
        """Send a card to a webhook URL.
        
        Args:
            card: The card to send.
            webhook_url: The webhook URL to send the card to.
            
        Returns:
            Dictionary with delivery results.
        """
        delivery = DeliveryManager(webhook_url=webhook_url)
        return delivery.send(card)