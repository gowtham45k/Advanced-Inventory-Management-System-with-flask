from models import Sale, Returns
from datetime import datetime
import uuid
import csv

class TransactionManager:
    def __init__(self, inventory):
        self.inventory = inventory
        self.sales = self.load_sales()
        self.returns = self.load_returns()

    def load_sales(self):
        """Load sales transactions from CSV file."""
        sales = []
        try:
            with open('sales.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sales.append(Sale(
                        row['transaction_id'],
                        row['product_id'],
                        int(row['quantity']),
                        float(row['price']),
                        datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    ))
        except FileNotFoundError:
            pass
        return sales

    def load_returns(self):
        """Load return transactions from CSV file."""
        returns = []
        try:
            with open('returns.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    returns.append(Returns(
                        row['transaction_id'],
                        row['product_id'],
                        int(row['quantity']),
                        row['reason'],
                        datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    ))
        except FileNotFoundError:
            pass
        return returns

    def record_sale(self, product_id: str, quantity: int, price: float):
        """Record a sale transaction and update the inventory."""
        if product_id not in self.inventory.products:
            raise ValueError("Product ID not found")
        
        product = self.inventory.products[product_id]
        if product.quantity < quantity:
            raise ValueError("Not enough inventory")

        transaction_id = str(uuid.uuid4())
        sale = Sale(transaction_id, product_id, quantity, price, datetime.now())
        self.sales.append(sale)
        product.quantity -= quantity
        self.save_sales()

    def record_return(self, product_id: str, quantity: int, reason: str):
        """Record a return transaction and update the inventory."""
        if product_id not in self.inventory.products:
            raise ValueError("Product ID not found")

        product = self.inventory.products[product_id]
        transaction_id = str(uuid.uuid4())
        return_transaction = Returns(transaction_id, product_id, quantity, reason, datetime.now())
        self.returns.append(return_transaction)
        product.quantity += quantity
        self.save_returns()

    def save_sales(self):
        """Save sales transactions to CSV file."""
        with open('sales.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['transaction_id', 'product_id', 'quantity', 'price', 'date'])
            writer.writeheader()
            for sale in self.sales:
                writer.writerow({
                    'transaction_id': sale.transaction_id,
                    'product_id': sale.product_id,
                    'quantity': sale.quantity,
                    'price': sale.price,
                    'date': sale.date.strftime('%Y-%m-%d %H:%M:%S')
                })

    def save_returns(self):
        """Save return transactions to CSV file."""
        with open('returns.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['transaction_id', 'product_id', 'quantity', 'reason', 'date'])
            writer.writeheader()
            for return_transaction in self.returns:
                writer.writerow({
                    'transaction_id': return_transaction.transaction_id,
                    'product_id': return_transaction.product_id,
                    'quantity': return_transaction.quantity,
                    'reason': return_transaction.reason,
                    'date': return_transaction.date.strftime('%Y-%m-%d %H:%M:%S')
                })
