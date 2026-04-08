import os
from datetime import datetime
from dotenv import load_dotenv

from skills.airtable_tool import fetch_debtors, update_debtor_status
from skills.apify_tool import is_holiday_today
from skills.llm_tool import get_hermes_decision
from skills.voice_tool import trigger_elevenlabs_call 

load_dotenv()

def is_office_hours():
    # Operational hours: 09:00 to 23:00
    current_hour = datetime.now().hour
    return 9 <= current_hour <= 23

def run_manager():
    print("Starting Hermes Manager...")
    
    if not is_office_hours():
        print("Outside operational hours. Standby mode.")
        return

    holiday_status = is_holiday_today()
    print(f"Business Day: {not holiday_status}")

    debtors = fetch_debtors()
    
    for record in debtors:
        fields = record.get('fields', {})
        status = fields.get('Status', '').strip().lower()
        
        if status in ['pending', 'panding']:
            name = fields.get('Name')
            amount = fields.get('Amount')
            phone = fields.get('Phone')
            record_id = record.get('id')

            print(f"Processing: {name} | Amount: {amount}")
            
            decision = get_hermes_decision(name, amount, holiday_status)
            
            if decision == 'CALL':
                result = trigger_elevenlabs_call(name, amount, phone, "debt settlement")
                
                if result.get("status") == "success":
                    update_debtor_status(record_id, "Call Triggered")
                    print(f"Status updated for {name}")
            else:
                print(f"Decision: Skip {name}")

if __name__ == "__main__":
    run_manager()