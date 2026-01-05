import json
import requests
import os

class FilterAgent:
    def __init__(self, api_key, model="gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def sift_input(self, raw_text):
        """
        Agentic Filtration: Separates Necessary vs Unnecessary data.
        Uses Google Gemini API to categorize info.
        """
        prompt = f"""
        Act as a professional financial clerk. Analyze the following user input:
        "{raw_text}"
        
        1. Extract structured financial data (Amount, Type, Category).
        2. Identify 'Unnecessary' fluff (emotions, weather, social context).
        3. Determine if this affects the 'Risk Profile' or 'Interests'.
        
        Return ONLY a JSON object with keys: 
        'structured_data', 'fluff', 'updates_to_bio', 'is_important_decision'.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            print(f"\n[FilterAgent] Making request to: {self.base_url}/{self.model}:generateContent")
            print(f"[FilterAgent] API Key status: {'Set (length: ' + str(len(self.api_key)) + ')' if self.api_key else 'NOT SET'}")
            
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"[FilterAgent] Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"[FilterAgent] Error response body: {response.text}")
            
            response.raise_for_status()
            
            # Extract content from Gemini response
            content = response.json()['candidates'][0]['content']['parts'][0]['text']
            
            # Attempt to parse JSON if the model returns it as a string
            if isinstance(content, str):
                # Simple cleanup if the model wraps in code blocks
                clean_content = content.replace('```json', '').replace('```', '').strip()
                return json.loads(clean_content)
            return content 
        except Exception as e:
            # Fallback for offline/error
            print(f"Filter Agent Error: {e}")
            print(f"[FilterAgent] Full error details: {type(e).__name__}: {str(e)}")
            return {
                "structured_data": None,
                "fluff": True,
                "updates_to_bio": None,
                "is_important_decision": False
            }