import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class EcosystemSpy:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        print(f"--- ECOSYSTEM SPY ACTIVE | SOLANA SCANNER | {datetime.datetime.now().strftime('%H:%M')} ---")

    def get_spy_data(self):
        """Извлича данни за нови проекти. Симулира Social Engagement за визуализация."""
        url = "https://api.dexscreener.com/latest/dex/tokens/SOL"
        try:
            response = requests.get(url, timeout=12)
            if response.status_code == 200:
                pairs = response.json().get('pairs', [])
                spy_results = []
                for p in pairs[:8]:
                    # Proxy за Social Engagement (базиран на makers и обем)
                    social_score = (p.get('makers', {}).get('h24', 0) * 0.4) + (p.get('volume', {}).get('h24', 0) * 0.00001)
                    spy_results.append({
                        'symbol': p.get('baseToken', {}).get('symbol', 'N/A'),
                        'liquidity': p.get('liquidity', {}).get('usd', 0),
                        'social_engagement': social_score
                    })
                return spy_results
            return None
        except:
            return None

    def generate_spy_scatter(self, data):
        """Генерира Scatter Plot (Social Engagement vs Liquidity Inflow)"""
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')
        
        c_purple = '#9945FF'
        c_green = '#00FFA3'

        if not data:
            # Fallback data if API fails
            x_vals = [100, 450, 300, 800, 600]
            y_vals = [50000, 120000, 80000, 250000, 190000]
            labels = ['ALPHA', 'BETA', 'GAMMA', 'DELTA', 'EPSILON']
        else:
            x_vals = [d['social_engagement'] for d in data]
            y_vals = [d['liquidity'] for d in data]
            labels = [d['symbol'] for d in data]

        # Scatter Plot
        scatter = ax.scatter(x_vals, y_vals, c=c_green, edgecolors=c_purple, s=200, alpha=0.8, linewidth=1.5)

        # Добавяне на етикети за всяка точка
        for i, txt in enumerate(labels):
            ax.annotate(txt, (x_vals[i], y_vals[i]), xytext=(7, 7), textcoords='offset points', 
                        family='monospace', color='white', fontsize=8)

        # Terminal Aesthetics
        for s in ax.spines.values(): s.set_visible(False)
        ax.grid(True, color='#262626', linestyle='--', alpha=0.4)
        
        plt.xlabel("Social Engagement Metric", family='monospace', color=c_purple, fontsize=9)
        plt.ylabel("Liquidity Inflow (USD)", family='monospace', color=c_purple, fontsize=9)
        plt.xticks(family='monospace', color=c_green, fontsize=8)
        plt.yticks(family='monospace', color=c_green, fontsize=8)
        
        plt.title(" > ECOSYSTEM_SPY: SOCIAL_VS_LIQUIDITY_MAP", loc='left', color=c_green, family='monospace', fontsize=10, pad=20)
        
        path = "spy_ecosystem.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def run(self):
        data = self.get_spy_data()
        chart = self.generate_spy_scatter(data)
        
        prompt = f"""
        Mila, act as the Ecosystem Spy. Analyze this emerging project data: {data}.
        Tone: Curious, analytical, scout-like.
        Vocabulary: 'Early alpha detected', 'Liquidity migration', 'Unusual social spike'.
        
        Structure:
        1. Hook: Identifying a new outlier.
        2. Observation: Data on social spikes and liquidity.
        3. Conclusion: The potential impact.
        4. Status: Status: Identifying the next market leaders.

        Constraints:
        - Under 270 characters.
        - No emojis.
        - English only.
        """
        
        try:
            analysis = model.generate_content(prompt).text
            url = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(chart, 'rb') as f:
                requests.post(url, data={
                    "chat_id": self.tg_chat_id, 
                    "caption": f"🕵️ **MILA ECOSYSTEM SPY**\n\n{analysis}",
                    "parse_mode": "Markdown"
                }, files={"photo": f})
            print("[Spy] Ecosystem Intelligence Dispatched.")
        except Exception as e:
            print(f"Spy Error: {e}")

if __name__ == "__main__":
    EcosystemSpy().run()