import json
from models import Inventory, Product

def save_inventory(inventory: Inventory, filename: str):
    """Save the current state of the inventory to a JSON file."""
    with open(filename, 'w') as f:
        data = {
            'products': [
                {
                    'product_id': p.product_id,
                    'name': p.name,
                    'price': p.price,
                    'category': p.category,
                    'quantity': p.quantity
                } for p in inventory.products.values()
            ]
        }
        json.dump(data, f, indent=4)

def load_inventory(filename: str) -> Inventory:
    """Load the inventory state from a JSON file."""
    inventory = Inventory()
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data['products']:
                product = Product(
                    item['product_id'],
                    item['name'],
                    item['price'],
                    item['category'],
                    item['quantity']
                )
                inventory.add_product(product)
    except FileNotFoundError:
        pass
    return inventory
