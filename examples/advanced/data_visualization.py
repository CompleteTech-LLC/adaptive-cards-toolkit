"""Example of creating data visualization cards with the Adaptive Cards Toolkit."""

import json
from adaptive_cards.card import AdaptiveCard
from adaptive_cards_toolkit import ElementFactory, DataConnector, ValidationUtility

def main():
    """Create and display a data visualization card."""
    # Sample data
    data = {
        "monthly_stats": {
            "users": 1234,
            "revenue": 56789,
            "growth": 12.5,
            "churn": 2.3
        },
        "top_products": [
            {"name": "Product A", "sales": 432, "rating": 4.8},
            {"name": "Product B", "sales": 367, "rating": 4.7},
            {"name": "Product C", "sales": 289, "rating": 4.5}
        ]
    }
    
    # Create a new card
    card = AdaptiveCard.new().version("1.5")
    
    # Add a title
    card.add_item(ElementFactory.create_heading("Monthly Performance Dashboard"))
    
    # Add monthly stats as a fact set
    monthly_stats = {
        "Users": f"{data['monthly_stats']['users']:,}",
        "Revenue": f"${data['monthly_stats']['revenue']:,}",
        "Growth": f"{data['monthly_stats']['growth']}%",
        "Churn": f"{data['monthly_stats']['churn']}%"
    }
    card.add_item(DataConnector.create_fact_set(monthly_stats))
    
    # Add top products section
    card.add_item(ElementFactory.create_heading("Top Products", level=2))
    
    # Convert product data to a table
    headers = ["Product", "Sales", "Rating"]
    rows = []
    for product in data["top_products"]:
        rows.append([
            product["name"],
            str(product["sales"]),
            str(product["rating"])
        ])
    
    table_elements = DataConnector.create_table(headers, rows)
    card.add_items(table_elements)
    
    # Validate the card
    validator = ValidationUtility()
    result = validator.validate(card.create())
    
    print(f"Card is valid: {result['valid']}")
    print(f"Card size: {result['size']:.2f}KB")
    
    # Display card JSON
    print("\nCard JSON:")
    print(json.dumps(json.loads(card.to_json()), indent=2))
    
    return card.create()

if __name__ == "__main__":
    main()
