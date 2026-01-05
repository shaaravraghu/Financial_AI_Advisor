import json
import requests
import numpy as np

class RiskEngine:
    def __init__(self, api_key, model="gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.market_file = 'data/market_context.txt'
        self.bio_file = 'data/user_bio.json'

    def calculate_risk_score(self, transactions):
        """
        Deterministic Risk Management: 
        Calculates volatility in user spending (Burn Rate Variance).
        """
        amounts = []
        for t in transactions:
             # robustly get amount
             val = t.get('Amount', t.get('amount'))
             if val:
                 amounts.append(float(val))
        
        if not amounts: return 0
        # Higher variance in spending = Higher behavioral risk
        return np.std(amounts) / np.mean(amounts)

    def probabilistic_reasoning(self, user_query, current_stats):
        """
        Uses Google Gemini to simulate future scenarios.
        """
        market_data = "No market data available"
        user_bio = "No bio available"

        try:
            with open(self.market_file, 'r') as f:
                market_data = f.read()
            with open(self.bio_file, 'r') as f:
                user_bio = f.read()
        except FileNotFoundError:
            pass

        # The 'Reasoning' Prompt
        prompt = f"""
        CONTEXT:
        User Bio: {user_bio}
        Market Trends: {market_data}
        Current Financial Stats: {current_stats}
        
        QUESTION: {user_query}
        
        TASK:
        1. Perform a Monte Carlo-style reasoning: What are the 3 most likely outcomes?
        2. Assign a probability (%) to each outcome.
        3. Risk Check: Does this query violate the user's Risk Profile?
        4. Strategy: If the user follows this, what is the 12-month future projection?
        
        Explain your reasoning clearly like a Senior Financier.
        """

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
            }
        }

        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            print(f"\n[RiskEngine] Making request to: {self.base_url}/{self.model}:generateContent")
            print(f"[RiskEngine] API Key status: {'Set (length: ' + str(len(self.api_key)) + ')' if self.api_key else 'NOT SET'}")
            
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"[RiskEngine] Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[RiskEngine] Error response body: {response.text}")
            
            response.raise_for_status()
            
            # Extract content from Gemini response
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            error_msg = f"Error computing risk logic: {e}"
            print(f"[RiskEngine] Full error details: {type(e).__name__}: {str(e)}")
            return error_msg