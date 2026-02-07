import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.hour = datetime.datetime.now().hour
        self.internal_alpha = {'SOL': 1.85e9, 'JTO': 1.25e8, 'PYTH': 8.5e7, 'JUP': 3.1e8}

    def human_format(self, num, pos=None):
        if num is None or num == 0: return "0"
        if abs(num) >= 1e9: return f'{num / 1e9:.1f}B'
        if abs(num) >= 1e6: return f'{num / 1e6:.1f}M'
        return str(int(num))

    def generate_terminal_chart(self, labels, values, title):
        if not labels:
            labels, values = list(self.internal_alpha.keys()), list(self.internal_alpha.values())
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')
        ax.bar(labels, values, color='#00FFA3', edgecolor='#9945FF', width=0.5)
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color='#262626', linestyle='--')
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.human_format))
        plt.title(f" > MILA_TERMINAL: {title}", loc='left', color='#00FFA3', family='monospace', fontsize=9)
        
        path = "mila_solana.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def run(self):
        # Fetching data logic (simplified for brevity)
        labels, values = ['SOL', 'JTO', 'PYTH'], [1.9e9, 1.3e8, 9e7]
        chart = self.generate_terminal_chart(labels, values, "NETWORK_INTENSITY")
        
        prompt = "Mila, create a cold, strategic X update for Solana. Alpha Format. Under 250 chars. English."
        try:
            analysis = model.generate_content(prompt).text
            # ВАЖНО: Пращаме всичко в един пакет
            url = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(chart, 'rb') as f:
                requests.post(url, data={
                    "chat_id": self.tg_chat_id, 
                    "caption": f"⚡ **MILA SYSTEM LOG**\n\n{analysis}",
                    "parse_mode": "Markdown"
                }, files={"photo": f})
            print("[Mila] Solana Report dispatched as a single unit.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    MilaCore().run()