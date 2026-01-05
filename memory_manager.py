import csv
import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.bio_file = 'data/user_bio.json'
        self.trans_file = 'data/transactions.csv'
        self.history_file = 'data/interaction_history.txt'
        self.decision_file = 'data/decision_log.txt'
        self.market_file = 'data/market_context.txt'
        
        # Ensure the data directory exists
        os.makedirs('data', exist_ok=True)
        self._initialize_files()

    def _initialize_files(self):
        """Creates files with headers if they don't exist."""
        # Initialize Transactions CSV
        if not os.path.exists(self.trans_file):
            with open(self.trans_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Type', 'Category', 'Amount', 'Description', 'Is_Necessary'])

        # Initialize Bio JSON
        if not os.path.exists(self.bio_file):
            default_bio = {
                "name": "User",
                "risk_profile": {"score": 5, "label": "Moderate"},
                "interests": [],
                "financial_goals": []
            }
            self.save_json(self.bio_file, default_bio)

    def log_interaction(self, speaker, text):
        """Records everything said (Historical Data)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.history_file, 'a') as f:
            f.write(f"[{timestamp}] {speaker}: {text}\n")

    def add_transaction(self, t_type, category, amount, description, necessary=True):
        """Maintains transactions and planning details in CSV."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.trans_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, t_type, category, amount, description, necessary])

    def save_decision(self, trigger, decision, reasoning):
        """Notes down all important decisions taken."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"--- {timestamp} ---\nTRIGGER: {trigger}\nDECISION: {decision}\nREASONING: {reasoning}\n\n"
        with open(self.decision_file, 'a') as f:
            f.write(entry)

    def get_market_trends(self):
        """Reads macro-economic data."""
        if os.path.exists(self.market_file):
            with open(self.market_file, 'r') as f:
                return f.read()
        return "No market data available."

    def save_json(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def load_json(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)