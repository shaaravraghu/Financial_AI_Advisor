import os
import sys

# Add the current directory to sys.path so we can import from local modules reliably
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. .env keys will be ignored.")

from memory_manager import MemoryManager
from engines.filter_agent import FilterAgent
from engines.risk_engine import RiskEngine
from utils import APIBridge

# --- CONFIGURATION ---
# Read sensitive configuration from environment variables when available
ELEVEN_API_KEY = os.environ.get('ELEVENLABS_API_KEY', "your_elevenlabs_key")
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', "your_google_api_key")
GOOGLE_MODEL = os.environ.get('GOOGLE_MODEL', "gemini-1.5-flash")

# Debug prints to verify configuration
print(f"\n{'='*60}")
print("CONFIGURATION LOADED:")
print(f"{'='*60}")
print(f"ElevenLabs API Key: {'✓ Set' if ELEVEN_API_KEY != 'your_elevenlabs_key' else '✗ NOT SET (using placeholder)'}")
print(f"Google API Key: {'✓ Set' if GOOGLE_API_KEY != 'your_google_api_key' else '✗ NOT SET (using placeholder)'}")
print(f"Google Model: {GOOGLE_MODEL}")
print(f"{'='*60}\n")

if GOOGLE_API_KEY == "your_google_api_key":
    print("⚠️  WARNING: Google API key is still a placeholder!")
    print("   Please update GOOGLE_API_KEY in your .env file with your actual key from Google AI Studio")
    print("   Get it here: https://aistudio.google.com/app/apikey\n")

class FinancierApp:
    def __init__(self):
        # Initialize all modules
        self.memory = MemoryManager()
        self.bridge = APIBridge(ELEVEN_API_KEY)
        self.filter_agent = FilterAgent(GOOGLE_API_KEY, GOOGLE_MODEL)
        self.risk_engine = RiskEngine(GOOGLE_API_KEY, GOOGLE_MODEL)

    def run_cycle(self, user_input, is_voice=False):
        """A single loop of listening, thinking, and advising."""
        
        # 1. CAPTURE & FILTER
        if is_voice:
            print(f"Processing voice file: {user_input}")
            raw_text = self.bridge.capture_voice(user_input)
        else:
            raw_text = user_input
            
        print(f"User Input: {raw_text}")
        
        # Filter data using the agent
        filtered_data = self.filter_agent.sift_input(raw_text)
        
        # Log interaction
        self.memory.log_interaction("USER", raw_text)
        
        # 2. UPDATE RECORDS
        # Check if 'structured_data' is in the filtered data
        sd = filtered_data.get('structured_data')
        if sd:
            self.memory.add_transaction(
                t_type=sd.get('Type', sd.get('type')),
                category=sd.get('Category', sd.get('category')),
                amount=sd.get('Amount', sd.get('amount')),
                description=f"Extracted from: {raw_text}", # Or use logic if available
                necessary=not filtered_data.get('fluff', False)
            )
            print("Transaction recorded.")

        # Handle Bio Updates
        bio_updates = filtered_data.get('updates_to_bio')
        if bio_updates:
            print(f"Updating Bio: {bio_updates}")
            # Load current bio
            current_bio = self.memory.load_json(self.memory.bio_file)
            
            # Update fields - assuming bio_updates is a dict or string we can append
            if isinstance(bio_updates, dict):
                current_bio.update(bio_updates)
            elif isinstance(bio_updates, str):
                 current_bio.setdefault('notes', []).append(bio_updates)
            
            # Save properly
            self.memory.save_json(self.memory.bio_file, current_bio)

        # 3. ANALYZE & PLAN (Probabilistic Reasoning)
        transactions = self.memory.load_json(self.memory.trans_file) if self.memory.trans_file.endswith('.json') else [] 
        # Note: memory_manager uses CSV for transactions, load_json might fail if not careful.
        # But load_json was used in old main.py. Let's check memory_manager again.
        # It has `add_transaction` which writes CSV.
        # It has `load_json`.
        # Old main.py: `transactions = self.memory.load_json(self.memory.trans_file)`
        # This seems like a bug in the old code if trans_file is CSV.
        # Let's check `memory_manager.py` content again.
        # Step 28: `self.trans_file = 'data/transactions.csv'`
        # Step 28: `load_json` uses `json.load`.
        # So the OLD code was broken! `transactions = self.memory.load_json(self.memory.trans_file)` would fail on CSV.
        # I should fix this in this refactor.
        # `RiskEngine.calculate_risk_score` expects a list of dicts.
        # I should read the CSV properly.
        # Since I am refactoring, I will add a method to read CSV in main or fix memory manager?
        # I'll just read CSV here using generic python or if `memory_manager` has a reader?
        # `memory_manager` does NOT have a CSV reader method shown in Step 28.
        # I will implement a quick CSV reader here or assume empty for now to avoid scope creep, 
        # BUT `RiskEngine` needs it.
        # I'll add a helper here.
        import csv
        transactions = []
        if os.path.exists(self.memory.trans_file):
            try:
                with open(self.memory.trans_file, 'r') as f:
                    reader = csv.DictReader(f)
                    transactions = list(reader)
            except Exception:
                transactions = []

        advice_text = self.risk_engine.probabilistic_reasoning(raw_text, str(transactions[-5:])) # Pass last 5 for context

        # 4. EXECUTE & LOG (Decision Log & Voice)
        decision_packet = {
            "trigger": raw_text,
            "advice": advice_text,
            "rationale": "Analyzed via MiMo-V2 Hybrid-Thinking Mode",
            "impact": "Projected 12-month wealth adjustment"
        }
        self.bridge.log_decision_to_file(decision_packet)
        self.bridge.speak_advice(advice_text)

        print(f"\nFINANCIER ADVICE: {advice_text}\n")

if __name__ == "__main__":
    app = FinancierApp()
    print("AI Financier Active. Enter text or path to audio file.")
    while True:
        try:
            cmd = input("You: ")
            if cmd.lower() in ['exit', 'quit']: break
            app.run_cycle(cmd)
        except KeyboardInterrupt:
            break
