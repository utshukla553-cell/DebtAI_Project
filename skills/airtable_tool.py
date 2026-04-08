import os
from pyairtable import Table

# Configuration

table = Table(API_KEY, BASE_ID, TABLE_NAME)

def fetch_debtors():
    """Airtable se saare records lekar aata hai"""
    try:
        return table.all()
    except Exception as e:
        print(f"Error fetching debtors: {e}")
        return []

def update_debtor_status(record_id, status):
    """Airtable mein status update karta hai"""
    try:
        table.update(record_id, {"Status": status})
        print(f"Updated record {record_id} to {status}")
    except Exception as e:
        print(f"Error updating status: {e}")