from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

class InvoiceGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_invoice(self, invoice):
        """Generate a PDF invoice."""
        file_path = os.path.join(self.output_dir, f"{invoice.invoice_id}.pdf")
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.drawString(1 * inch, height - 1 * inch, f"Invoice ID: {invoice.invoice_id}")
        c.drawString(1 * inch, height - 1.5 * inch, f"Date: {invoice.transactions[0].date.strftime('%Y-%m-%d %H:%M:%S')}")

        y_position = height - 2.5 * inch
        for transaction in invoice.transactions:
            c.drawString(1 * inch, y_position, f"Product ID: {transaction.product_id}")
            c.drawString(4 * inch, y_position, f"Quantity: {transaction.quantity}")
            c.drawString(6 * inch, y_position, f"Price: ${transaction.price:.2f}")
            y_position -= 0.5 * inch

        c.drawString(1 * inch, y_position - 0.5 * inch, f"Total Amount: ${invoice.total_amount:.2f}")
        c.save()
        return file_path
