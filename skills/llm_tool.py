import os
import requests
import json

def get_hermes_decision(name, amount, is_holiday):
    api_key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Simple logic: Agar holiday hai toh CALL mat karo
    if is_holiday:
        return "SKIP"

    prompt = f"User {name} owes {amount}. Today is a working day. Should we CALL or SKIP? Answer in one word only."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemini-2.0-flash-001", # Sabse stable model OpenRouter par
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        
        # Check agar response mein error hai
        if 'choices' in result:
            return result['choices'][0]['message']['content'].strip().upper()
        else:
            print(f"⚠️ OpenRouter Error: {result.get('error', 'Unknown Error')}")
            # Agar AI fail ho jaye, toh safety ke liye 'CALL' return kar do
            return "CALL" 
            
    except Exception as e:
        print(f"❌ LLM Skill Error: {e}")
        return "CALL"