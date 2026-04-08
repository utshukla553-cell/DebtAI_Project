import os
import requests
import json

def get_hermes_decision(name, amount, is_holiday):
    """
    Hermes Decision Engine: Determines whether to CALL or SKIP a debtor.
    Integrates with OpenRouter API for LLM-based reasoning.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Business Logic: Skip calls on holidays/weekends
    if is_holiday:
        return "SKIP"

    prompt = f"Debtor: {name}, Amount: {amount}. Today is a business day. Action: CALL or SKIP? Output one word only."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.0-flash-001",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        
        if 'choices' in result:
            decision = result['choices'][0]['message']['content'].strip().upper()
            return decision if decision in ['CALL', 'SKIP'] else 'CALL'
        
        print(f"LLM Provider Error: {result.get('error', 'Unknown')}")
        return "CALL"
            
    except Exception as e:
        print(f"Decision Engine Error: {e}")
        return "CALL"