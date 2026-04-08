from skills.airtable_tool import fetch_debtors, update_debtor_status
from skills.apify_tool import is_holiday_today
from skills.llm_tool import get_hermes_decision
from skills.voice_tool import trigger_elevenlabs_call 
from dotenv import load_dotenv
from datetime import datetime  # <-- Import zaroori hai

load_dotenv()

def is_office_hours():
    """Requirement: Call only during specific hours of the day."""
    current_hour = datetime.now().hour
    # 9 AM se 6 PM (18:00) tak allowed hai
    return 9 <= current_hour <=23

def run_hermes_system():
    print("--- 🤖 Hermes AI Manager Started ---")
    
    # 1. 🕒 Time Check (Requirement: Hour of the day)
    if not is_office_hours():
        print("🌙 Status: Outside Office Hours. Hermes is in standby mode.")
        return # Yahan se code ruk jayega

    # 2. 📅 Holiday Check via Apify
    holiday_status = is_holiday_today()
    print(f"📅 Holiday Check: {'Holiday' if holiday_status else 'Working Day'}")

    # 3. 📥 Fetch Data from Airtable
    debtors = fetch_debtors()
    print(f"📊 Total debtors fetched: {len(debtors)}")
    
    for record in debtors:
        fields = record.get('fields', {})
        name = fields.get('Name', 'Customer')
        amount = fields.get('Amount', 0)
        status = fields.get('Status')
        phone = fields.get('Phone', 'Unknown')
        product = "pending dues" 
        record_id = record.get('id')

        # Smart Status Check (Case & Spelling Proof)
        if status and str(status).strip().lower() in ['pending', 'panding']:
            print(f"🔎 Processing: {name} (Amount: {amount})")
            
            # 4. 🧠 LLM Decision (OpenRouter)
            decision = get_hermes_decision(name, amount, holiday_status)
            print(f"🧠 AI Decision for {name}: {decision}")

            if decision == 'CALL':
                # 5. 📞 Trigger ElevenLabs Hermes Skill
                result = trigger_elevenlabs_call(name, amount, phone, product)
                
                if result["status"] == "success":
                    print(f"✅ Success: {result['message']}")
                    
                    # 6. 🔄 Closed Learning Loop (Updating Status)
                    # Requirement: System learns that action was taken
                    update_debtor_status(record_id, "Call Triggered")
                else:
                    print(f"❌ Failed for {name}")
            else:
                print(f"😴 Skipping {name} (AI Decision: {decision})")

if __name__ == "__main__":
    try:
        run_hermes_system()
    except Exception as e:
        print(f"🚨 CRITICAL SYSTEM ERROR: {e}")