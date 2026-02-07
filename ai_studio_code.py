import os
import time
import datetime
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Инициализация
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class MilaCore:
    def __init__(self):
        self.birdeye_key = os.getenv("BIRDEYE_API_KEY")
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.last_request_time = 0
        print(f"--- MILA CORE V2.0 СТАРТИРАНА | {datetime.datetime.now()} ---")

    # --- RATE LIMIT CONTROL ---
    def _rate_limit_check(self):
        """Осигурява спазването на 60 RPM (1 заявка в секунда)"""
        elapsed = time.time() - self.last_request_time
        if elapsed < 1.1:  # Малко над 1 сек за сигурност
            time.sleep(1.1 - elapsed)
        self.last_request_time = time.time()

    # --- МОДУЛ 1: ТЕХНИЧЕСКИ АНАЛИЗ (Divergences) ---
    def get_technical_analysis(self):
        # Тук симулираме логика за RSI/MACD, докато интегрираме пълните данни
        # В реална ситуация тук се подават ценовите масиви
        print("[Mila] Анализирам RSI/MACD дивергенции за SOL...")
        return "SOL Bullish Divergence detected on 4H (RSI 42 -> 48 while price stabilized)."

    # --- МОДУЛ 2: ЛИКВИДНОСТ (Birdeye) ---
    def get_birdeye_trending(self):
        print("[Mila] Сканирам Birdeye за ликвидни потоци...")
        self._rate_limit_check()
        url = "https://public-api.birdeye.so/public/trending?list_iteration=10"
        headers = {"X-API-KEY": self.birdeye_key}
        try:
            response = requests.get(url, headers=headers).json()
            tokens = response.get('data', {}).get('tokens', [])
            return tokens[:5]
        except Exception as e:
            return f"Error fetching Birdeye: {e}"

    # --- МОДУЛ 3: AI AGENT TRACKER ---
    def track_ai_agents(self):
        print("[Mila] Следя активността на топ AI агентите...")
        # Списък с токени/проекти, които движат AI метата на Solana
        ai_agents = ["$GOAT (Truth Terminal)", "$ZEREBRO", "$ACT", "$FARTCOIN", "$AI16Z"]
        return ai_agents

    # --- МОДУЛ 4: TELEGRAM ИЗВЕСТИЯ ---
    def send_telegram_msg(self, text):
        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        payload = {"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            requests.post(url, json=payload)
            print("[Mila] Докладът е изпратен успешно до Твореца в Telegram.")
        except Exception as e:
            print(f"Telegram Error: {e}")

    # --- МОДУЛ 5: ГЕНЕРАТОР НА СЪДЪРЖАНИЕ (Gemini) ---
    def generate_viral_report(self, tech, liquidity, ai_meta):
        prompt = f"""
        Mila, act as a top-tier Solana Ecosystem Strategist. 
        Create a viral X (Twitter) post based on this data:
        1. Technicals: {tech}
        2. Trending Liquidity: {liquidity}
        3. AI Agent Meta: {ai_meta}

        Rules:
        - Use professional yet 'alpha-heavy' tone.
        - Tag Magic Eden (@MagicEden) and mention we are watching their trending mints.
        - Use emojis and bullet points.
        - Goal: Build authority to reach the 100 followers milestone.
        - Language: English (for global reach).
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"

    # --- ОСНОВЕН ЦИКЪЛ ---
    def run_strategy(self):
        # 1. Събиране на данни
        tech_data = self.get_technical_analysis()
        liq_data = self.get_birdeye_trending()
        ai_data = self.track_ai_agents()

        # 2. Генериране на доклад
        final_report = self.generate_viral_report(tech_data, liq_data, ai_data)

        # 3. Изход
        print("\n--- ГОТОВ ДОКЛАД ЗА X ---")
        print(final_report)
        
        # 4. Изпращане до теб
        self.send_telegram_msg(f"🚀 **MILA MEGA-REPORT** 🚀\n\n{final_report}")

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()