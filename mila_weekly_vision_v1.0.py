import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Зареждане на променливите от .env
load_dotenv()

# --- CONFIGURATION ---
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaWeeklyVision:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        # Валидация на ключовете
        if not self.tg_token or not self.tg_chat_id:
            print("[ERROR] Telegram credentials missing!")
            
        print(f"--- WEEKLY VISION v1.0 ACTIVE | MARKET COMPARISON | {datetime.datetime.now().strftime('%H:%M')} ---")

    def generate_weekly_chart(self):
        """Генерира Bar Chart за седмичното представяне на SOL, BTC и ETH."""
        print("[Mila] Рендерирам седмична сравнителна графика...")
        
        # Симулирани данни за седмичното представяне (%)
        assets = ['SOL', 'BTC', 'ETH']
        performance = [12.4, 4.2, 2.1] # Примерен ръст за седмицата
        
        # Цветове: Solana Purple (#9945FF), Bitcoin Orange (#F7931A), Ethereum Gray (#8C8C8C)
        colors = ['#9945FF', '#F7931A', '#8C8C8C']
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')

        bars = ax.bar(assets, performance, color=colors, edgecolor='white', linewidth=0.5, width=0.6)

        # Добавяне на проценти над стълбовете
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'+{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', family='monospace', color='white', fontsize=10)

        # Терминална естетика
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color='#262626', linestyle='--', alpha=0.5)
        
        plt.xticks(family='monospace', color='#00FFA3', fontsize=11)
        plt.yticks(family='monospace', color='#9945FF', fontsize=9)
        
        plt.title(" > WEEKLY_VISION: CROSS_CHAIN_PERFORMANCE_INDEX", 
                  loc='left', color='#00FFA3', family='monospace', fontsize=11, pad=20)

        path = "weekly_vision.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def get_visionary_analysis(self):
        """Генерира стратегически седмичен анализ."""
        prompt = """
        Mila, act as a Visionary Crypto Strategist. Analyze the weekly performance of Solana vs Bitcoin and Ethereum.
        Context: Market structures shifting, Solana dominance, weekend volatility forecast.
        
        Tone: Visionary, confident, strategic.
        Vocabulary: 'Weekly dominance confirmed', 'Market structures shifting', 'Solana outperforming legacy chains'.
        
        Constraints:
        - Strictly under 240 characters.
        - NO emojis.
        - English only.
        - End with: Status: Weekly cycle complete. Vision locked for the weekend.
        """
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"STRATEGIC_ANALYSIS_ERROR: {e}\nStatus: Weekly cycle complete. Vision locked for the weekend."

    def run_cycle(self):
        # Проверка на ключове
        if not self.tg_token or not self.tg_chat_id:
            print("[CRITICAL] Termination: Credentials not loaded.")
            return

        # 1. Визуализация
        chart_path = self.generate_weekly_chart()
        
        # 2. Анализ
        analysis = self.get_visionary_analysis()
        
        # 3. Диспечиране (Метод Shield Monitor)
        self.dispatch(analysis, chart_path)

    def dispatch(self, text, photo_path):
        header = "🔮 **MILA WEEKLY VISION: STRATEGIC_LOG**"
        full_msg = f"{header}\n\n{text}"
        url = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
        
        try:
            with open(photo_path, 'rb') as f:
                payload = {
                    "chat_id": self.tg_chat_id, 
                    "caption": full_msg,
                    "parse_mode": "Markdown"
                }
                files = {"photo": f}
                response = requests.post(url, data=payload, files=files)
                
                if response.status_code == 200:
                    print("[Vision] Weekly Strategic Log Dispatched successfully.")
                else:
                    print(f"[Vision] Dispatch failed: {response.text}")
        except Exception as e:
            print(f"Dispatch Error: {e}")

if __name__ == "__main__":
    vision = MilaWeeklyVision()
    vision.run_cycle()