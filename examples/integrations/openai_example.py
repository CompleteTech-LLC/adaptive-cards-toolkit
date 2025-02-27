"""Example usage of the OpenAI Assistant agent for creating adaptive cards."""

import json
import os
import argparse
from typing import Dict, Any, Optional

from adaptive_cards_toolkit.openai_agent import AdaptiveCardGenerator


def save_card_to_file(card_json: Dict[str, Any], output_file: str) -> None:
    """Save a card JSON to a file.
    
    Args:
        card_json: The card JSON data.
        output_file: The output file path.
    """
    with open(output_file, "w") as f:
        json.dump(card_json, f, indent=2)
    print(f"Card saved to {output_file}")


def main():
    """Run the example."""
    parser = argparse.ArgumentParser(description="Generate adaptive cards using OpenAI Assistant")
    parser.add_argument("--prompt", type=str, help="Prompt describing the card to generate")
    parser.add_argument("--output", type=str, default="generated_card.json", 
                        help="Output file for the generated card (default: generated_card.json)")
    parser.add_argument("--api-key", type=str, help="OpenAI API key (optional, will use OPENAI_API_KEY env var if not provided)")
    parser.add_argument("--webhook", type=str, help="Optional webhook URL to send the card to")
    
    args = parser.parse_args()
    
    # Get the prompt from command line or interactively
    prompt = args.prompt
    if not prompt:
        print("Describe the adaptive card you want to generate:")
        prompt = input("> ")
    
    # Initialize the card generator
    try:
        # For testing, let's create a simplified version that doesn't require OpenAI API
        if os.environ.get("TEST_MODE") == "true":
            print("Running in test mode - generating a mock card")
            from tools.agent_toolkit.templates import TemplateFactory
            
            # Create a mock result with a sample notification card
            mock_card = TemplateFactory.create_notification_card(
                title="System Maintenance",
                message="The system will be down for maintenance on Saturday from 2-4 PM EST.",
                level="warning",
                icon_url="https://adaptivecards.io/content/notification-default.png"
            )
            
            result = {
                "success": True,
                "card": mock_card,
                "card_json": json.loads(mock_card.to_json()),
                "explanation": "I've created a notification card with a warning style to alert users about the upcoming maintenance."
            }
        else:
            generator = AdaptiveCardGenerator(api_key=args.api_key)
            
            print(f"Generating adaptive card based on prompt: '{prompt}'")
            result = generator.generate_card(prompt)
        
        if result["success"]:
            print("\n✅ Card generated successfully!")
            print("\nDesign explanation:")
            print(result["explanation"])
            
            # Save to file
            save_card_to_file(result["card_json"], args.output)
            
            # Send to webhook if provided
            if args.webhook:
                print(f"\nSending card to webhook URL: {args.webhook}")
                delivery_result = generator.send_card(result["card"], args.webhook)
                
                if delivery_result["success"]:
                    print("✅ Card sent successfully!")
                else:
                    print(f"❌ Failed to send card: {delivery_result['message']}")
        else:
            print(f"\n❌ Failed to generate card: {result['error']}")
            
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()