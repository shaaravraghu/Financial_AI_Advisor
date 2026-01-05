import pandas as pd

class PlanningEngine:
    def __init__(self, transactions_path):
        self.df = pd.read_csv(transactions_path)

    def project_future(self, months=12):
        # Deterministic Math: Burn rate calculation
        avg_monthly_spend = self.df[self.df['Type'] == 'Expense']['Amount'].mean()
        
        # AI Logic: How will 2026 inflation affect this burn rate?
        # (This is injected into the final prompt in main.py)
        return f"Based on a monthly burn of ${avg_monthly_spend:.2f}, you have X months of runway."
    