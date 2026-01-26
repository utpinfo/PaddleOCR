from app.entities.invoice_type import INVOICE_TYPE
from app.services.invoice_classifier import normalize_text, classify_invoice

invoice_type = INVOICE_TYPE

invoice_info = classify_invoice("通行费", threshold=50)
subtype = invoice_info["SubType"]

print(invoice_info)