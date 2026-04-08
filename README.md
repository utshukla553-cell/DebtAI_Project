# Hermes Debt Manager (My Assignment)

I have built this system to automate debt collection using AI. It checks our database, decides who to call using an LLM, and then triggers a voice call.

# How I built this

* **Database (Airtable):** I'm using Airtable to store customer names, phone numbers, and debt amounts.
* **Holiday Check (Apify):** Before making any call, the script checks if today is a working day. It won't call on weekends or holidays.
* **Decision Making (OpenRouter):** I sent the debtor's data to Gemini 2.0. The AI looks at the amount and status to decide if we should 'CALL' or 'SKIP'.
* **Voice Call (ElevenLabs):** If the AI says 'CALL', the system triggers an ElevenLabs Conversational Agent.
* **Syncing back:** After the call trigger is successful, the script updates the status in Airtable to "Call Triggered" so we don't repeat the same record.

# My Files
* `main.py`: This is the main script that runs the whole process.
* `skills/`: This folder has all my tool scripts for Airtable, Apify, and Voice.
* `requirements.txt`: Libraries I used (requests, pyairtable, etc.)

# How to run it
1. Clone the repo to your laptop.
2. Run `pip install -r requirements.txt` to install everything.
3. Make sure to add your API keys in the `.env` file.
4. Just run `python main.py`.

# Important Note
I have added a prompt to the ElevenLabs agent so it only talks about the debt. If the customer tries to change the topic, the agent will politely bring them back to the payment discussion.

