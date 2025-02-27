"""Example of creating a notification card with the Adaptive Cards Toolkit."""

from adaptive_cards_toolkit import TemplateFactory, ValidationUtility

def main():
    """Create and display a notification card."""
    # Create a notification card
    card = TemplateFactory.create_notification_card(
        title="System Maintenance",
        message="The system will be down for maintenance on Saturday from 2-4 PM EST.",
        level="warning",
        action_url="https://example.com/system-status"
    )
    
    # Validate the card
    validator = ValidationUtility()
    result = validator.validate(card)
    
    print(f"Card is valid: {result['valid']}")
    print(f"Card size: {result['size']:.2f}KB")
    
    # Display card JSON
    print("\nCard JSON:")
    print(card.to_json())
    
    return card

if __name__ == "__main__":
    main()
