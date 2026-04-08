import os
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

# Environment Variables
API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

# Initialize Airtable client
table = Table(API_KEY, BASE_ID, TABLE_NAME)

def fetch_debtors():
    """
    Fetch all records from the configured Airtable table.
    """
    try:
        return table.all()
    except Exception as e:
        print(f"Airtable Fetch Error: {e}")
        return []

def update_debtor_status(record_id, status):
    """
    Update the 'Status' field for a specific record.
    Requirement: Implementation of closed-loop feedback.
    """
    try:
        table.update(record_id, {"Status": status})
        print(f"System: Record {record_id} status updated to '{status}'")
    except Exception as e:
        print(f"Airtable Update Error: {e}")