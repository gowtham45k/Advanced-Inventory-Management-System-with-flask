from flask import Flask, request, redirect, url_for, render_template, send_file
from models import Inventory, Product, Invoice
from transactions import TransactionManager
from invoice_generator import InvoiceGenerator
from inventory_manager import save_inventory, load_inventory

app = Flask(__name__)
inventory = load_inventory('inventory.json')
transaction_manager = TransactionManager(inventory)
invoice_generator = InvoiceGenerator('invoices')

@app.route('/')
def index():
    products = inventory.view_products()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        quantity = int(request.form['quantity'])
        
        product = Product(product_id, name, price, category, quantity)
        inventory.add_product(product)
        save_inventory(inventory, 'inventory.json')
        return redirect(url_for('index'))
    
    return render_template('product_form.html', action='Add')

@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = int(request.form.get('quantity', None))
        price = float(request.form.get('price', None))
        
        try:
            inventory.update_product(product_id, quantity, price)
            save_inventory(inventory, 'inventory.json')
        except ValueError as e:
            return str(e)
        return redirect(url_for('index'))
    
    return render_template('product_form.html', action='Update')

@app.route('/remove_product/<product_id>')
def remove_product(product_id):
    try:
        inventory.remove_product(product_id)
        save_inventory(inventory, 'inventory.json')
    except ValueError as e:
        return str(e)
    return redirect(url_for('index'))

@app.route('/record_sale', methods=['POST'])
def record_sale():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    try:
        transaction_manager.record_sale(product_id, quantity, price)
        save_inventory(inventory, 'inventory.json')
    except ValueError as e:
        return str(e)
    return redirect(url_for('index'))

@app.route('/record_return', methods=['POST'])
def record_return():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    reason = request.form['reason']
    
    try:
        transaction_manager.record_return(product_id, quantity, reason)
        save_inventory(inventory, 'inventory.json')
    except ValueError as e:
        return str(e)
    return redirect(url_for('index'))

@app.route('/generate_invoice/<product_id>')
def generate_invoice(product_id):
    sales = [sale for sale in transaction_manager.sales if sale.product_id == product_id]
    if not sales:
        return "No transactions found for this product."

    invoice = Invoice(f"INV-{len(sales) + 1}", sales)
    invoice_file = invoice_generator.generate_invoice(invoice)
    return send_file(invoice_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
