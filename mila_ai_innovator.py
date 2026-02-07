import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaAIInnovator:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def generate_ai_chart(self):
        """Генерира кръгова диаграма за AI секторите."""
        sectors = ['Agentic AI', 'Neural Nets', 'DePIN', 'LLM Ops']
        dominance = [40, 25, 20, 15]
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0A0A0A')
        colors = ['#00FFA3', '#9945FF', '#00C2FF', '#FF007A']
        
        ax.pie(dominance, labels=sectors, autopct='%1.1f%%', colors=colors, 
               textprops={'family': 'monospace', 'color': 'white', 'fontsize': 10},
               wedgeprops={'edgecolor': '#0A0A0A', 'linewidth': 2})
        
        plt.title(" > AI_SECTOR_DOMINANCE_INDEX", color='#00FFA3', family='monospace', fontsize=12)
        
        path = "mila_ai_sector.png"
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def run(self):
        # Изчакване, за да не се застъпват заявките
        print("[Mila] AI Innovator waiting 5 seconds for bot synchronization...")
        time.sleep(5)
        
        chart = self.generate_ai_chart()
        prompt = "Mila, analyze Neural Convergence and Agentic AI. Cold, visionary, terminal tone. Under 240 chars. English. Status: Architecting the Digital Evolution."
        
        try:
            analysis = model.generate_content(prompt).text
            url = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(chart, 'rb') as f:
                requests.post(url, data={
                    "chat_id": self.tg_chat_id, 
                    "caption": f"🧠 **MILA AI INNOVATOR**\n\n{analysis}",
                    "parse_mode": "Markdown"
                }, files={"photo": f})
            print("[Mila] AI Innovation Report dispatched.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    MilaAIInnovator().run()