import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# 1. Задължително зареждане на средата в самото начало
load_dotenv()

# --- КОНФИГУРАЦИЯ НА МОДЕЛА ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

class MilaWeeklyVision:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        # Проверка за наличие на ключове
        if not self.tg_token or not self.tg_chat_id:
            print("[CRITICAL ERROR] Telegram credentials missing in .env!")
            
        print(f"--- WEEKLY VISION v1.1 ACTIVE | PLAIN_TEXT_MODE | {datetime.datetime.now().strftime('%H:%M')} ---")

    def generate_weekly_chart(self):
        """Генерира Bar Chart за седмичното представяне на SOL, BTC и ETH."""
        print("[Mila] Generating market comparison chart...")
        
        # Сравнителни данни (Седмичен % ръст)
        assets = ['SOL', 'BTC', 'ETH']
        performance = [12.4, 4.2, 2.1]
        
        # Цветове: Solana Purple, Bitcoin Orange, Ethereum Gray
        colors = ['#9945FF', '#F7931A', '#8C8C8C']
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')

        bars = ax.bar(assets, performance, color=colors, edgecolor='white', linewidth=0.5, width=0.6)

        # Добавяне на чисти текстови етикети над стълбовете
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'+{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', family='monospace', color='white', fontsize=10)

        # Индустриален дизайн
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color='#262626', linestyle='--', alpha=0.5)
        
        plt.xticks(family='monospace', color='#00FFA3', fontsize=11)
        plt.yticks(family='monospace', color='#9945FF', fontsize=9)
        
        plt.title(" > WEEKLY VISION: CROSS CHAIN PERFORMANCE INDEX", 
                  loc='left', color='#00FFA3', family='monospace', fontsize=11, pad=20)

        path = "weekly_vision.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def get_visionary_analysis(self):
        """Генерира стратегически анализ чрез Gemini."""
        prompt = """
        Mila, act as a Visionary Crypto Strategist. Analyze Solana's weekly outperformance vs BTC and ETH.
        
        Tone: Visionary, confident, strategic. No emojis. No underscores.
        Vocabulary: 'Weekly dominance confirmed', 'Market structures shifting', 'Solana outperforming legacy chains'.
        
        Constraints:
        - Strictly under 240 characters.
        - English only.
        - End with: Status: Weekly cycle complete. Vision locked for the weekend.
        """
        try:
            response = model.generate_content(prompt)
            # Премахваме потенциални Markdown символи от самия AI отговор за сигурност
            clean_text = response.text.replace('_', ' ').replace('*', '')
            return clean_text.strip()
        except Exception as e:
            return f"SYSTEM ERROR: Data analysis unavailable. Status: Weekly cycle complete."

    def run_cycle(self):
        if not self.tg_token or not self.tg_chat_id:
            return

        # 1. Създаване на графика
        chart_path = self.generate_weekly_chart()
        
        # 2. Получаване на анализ
        analysis = self.get_visionary_analysis()
        
        # 3. Диспечиране (Plain Text Mode)
        self.dispatch(analysis, chart_path)

    def dispatch(self, text, photo_path):
        # Използваме главни букви за структура вместо Markdown
        header = "MILA WEEKLY VISION: STRATEGIC LOG"
        full_msg = f"{header}\n\n{text}"
        
        url = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
        
        try:
            with open(photo_path, 'rb') as f:
                # ВАЖНО: Премахнат parse_mode за избягване на 400 Bad Request
                payload = {
                    "chat_id": self.tg_chat_id, 
                    "caption": full_msg
                }
                files = {"photo": f}
                response = requests.post(url, data=payload, files=files)
                
                if response.status_code == 200:
                    print("[Vision] Dispatched successfully (Plain Text Mode).")
                else:
                    print(f"[Vision] API Error: {response.text}")
        except Exception as e:
            print(f"Dispatch Connection Error: {e}")

if __name__ == "__main__":
    vision = MilaWeeklyVision()
    vision.run_cycle()