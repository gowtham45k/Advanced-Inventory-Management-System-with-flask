from typing import List, Dict
from datetime import datetime

class Product:
    def __init__(self, product_id: str, name: str, price: float, category: str, quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity

    def __str__(self):
        return f"Product({self.product_id}, {self.name}, {self.price}, {self.category}, {self.quantity})"

class Inventory:
    def __init__(self):
        self.products: Dict[str, Product] = {}

    def add_product(self, product: Product):
        """Add a product to the inventory."""
        self.products[product.product_id] = product

    def update_product(self, product_id: str, quantity: int = None, price: float = None):
        """Update the product's quantity and/or price."""
        if product_id in self.products:
            if quantity is not None:
                self.products[product_id].quantity = quantity
            if price is not None:
                self.products[product_id].price = price
        else:
            raise ValueError("Product ID not found")

    def remove_product(self, product_id: str):
        """Remove a product from the inventory."""
        if product_id in self.products:
            del self.products[product_id]
        else:
            raise ValueError("Product ID not found")

    def view_products(self) -> List[Product]:
        """View all products in the inventory."""
        return list(self.products.values())

class Transaction:
    def __init__(self, transaction_id: str, product_id: str, quantity: int, price: float, date: datetime):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.date = date

    def __str__(self):
        return f"Transaction({self.transaction_id}, {self.product_id}, {self.quantity}, {self.price}, {self.date})"

class Sale(Transaction):
    def __init__(self, transaction_id: str, product_id: str, quantity: int, price: float, date: datetime):
        super().__init__(transaction_id, product_id, quantity, price, date)

class Returns(Transaction):
    def __init__(self, transaction_id: str, product_id: str, quantity: int, reason: str, date: datetime):
        super().__init__(transaction_id, product_id, quantity, 0.0, date)
        self.reason = reason

    def __str__(self):
        return f"Returns({self.transaction_id}, {self.product_id}, {self.quantity}, {self.reason}, {self.date})"

class Invoice:
    def __init__(self, invoice_id: str, transactions: List[Transaction]):
        self.invoice_id = invoice_id
        self.transactions = transactions
        self.total_amount = sum(t.price * t.quantity for t in transactions)

    def __str__(self):
        return f"Invoice({self.invoice_id}, {self.total_amount})"
