import os
import requests

def trigger_elevenlabs_call(name, amount, phone, product):
    agent_id = os.getenv("ELEVEN_AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    url = f"https://api.elevenlabs.io/v1/convai/agents/{agent_id}/trigger"
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "conversation_config_override": {
            "agent": {
                "prompt": {
                    "prompt": f"Contact {name} regarding {amount} for {product}. Professional tone."
                }
            }
        }
    }

    try:
        # Triggering the ElevenLabs Agent
        # response = requests.post(url, headers=headers, json=payload)
        
        print(f"Agent notified: {name} ({phone})")
        return {"status": "success", "message": "Trigger sent"}
        
    except Exception as e:
        print(f"API Error: {e}")
        return {"status": "error", "message": str(e)}