import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- КОНФИГУРАЦИЯ ---
load_dotenv()
# Използваме задължително gemini-2.5-flash според твоята директива
GENAI_MODEL_NAME = 'gemini-2.5-flash'

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(GENAI_MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.birdeye_key = os.getenv("BIRDEYE_API_KEY")
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.last_request_time = 0
        print(f"--- MILA CORE ACTIVE | MODEL: {GENAI_MODEL_NAME} | {datetime.datetime.now()} ---")

    def _rate_limit_check(self):
        """Гарантира 60 RPM (1 заявка на 1.2 секунди за сигурност)"""
        elapsed = time.time() - self.last_request_time
        if elapsed < 1.2:
            time.sleep(1.2 - elapsed)
        self.last_request_time = time.time()

    def get_birdeye_trending(self):
        """Извлича трендинг токени от Birdeye"""
        print("[Mila] Извличане на данни от Birdeye...")
        self._rate_limit_check()
        url = "https://public-api.birdeye.so/public/trending?list_iteration=10"
        headers = {"X-API-KEY": self.birdeye_key}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            tokens = data.get('data', {}).get('tokens', [])
            return tokens[:5] if tokens else []
        except Exception as e:
            print(f"[Грешка Birdeye]: {e}")
            return []

    def generate_liquidity_chart(self, tokens):
        """Генерира графика само при наличие на данни"""
        if not tokens:
            print("[Mila] ВНИМАНИЕ: Няма данни за токени. Прескачам генерирането на графика.")
            return None

        print("[Mila] Данните са налични. Генерирам mila_chart.png...")
        try:
            names = [t.get('symbol', 'N/A') for t in tokens]
            # Използваме 24h обем за визуализация
            volumes = [t.get('v24hUSD', 0) for t in tokens]

            plt.figure(figsize=(10, 6))
            plt.style.use('dark_background')
            colors = ['#14F195', '#9945FF', '#00C2FF', '#FF007A', '#F0E442']
            
            plt.bar(names, volumes, color=colors)
            plt.title('Solana Liquidity Inflow (Top 5 Trending)', fontsize=14, color='#14F195')
            plt.ylabel('24h Volume (USD)')
            plt.grid(axis='y', linestyle='--', alpha=0.3)
            
            chart_path = "mila_chart.png"
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        except Exception as e:
            print(f"[Грешка Графика]: {e}")
            return None

    def send_telegram_full_report(self, text, photo_path=None):
        """Изпраща текст и графика до Telegram"""
        try:
            # Текст
            url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
            requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"})
            
            # Снимка (само ако съществува)
            if photo_path and os.path.exists(photo_path):
                url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
                with open(photo_path, 'rb') as photo:
                    requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": photo})
                print("[Mila] Докладът и графиката са изпратени в Telegram.")
            else:
                print("[Mila] Изпратен е само текстов доклад.")
        except Exception as e:
            print(f"[Грешка Telegram]: {e}")

    def run_strategy(self):
        # 1. Данни от Birdeye
        tokens = self.get_birdeye_trending()
        
        # 2. Генериране на графика (със защита)
        chart_file = self.generate_liquidity_chart(tokens)
        
        # 3. Анализ от Gemini 2.5 Flash
        print(f"[Mila] Генерирам стратегически анализ с {GENAI_MODEL_NAME}...")
        prompt = f"""
        Analyze these Solana trending tokens: {tokens}. 
        Create a high-impact X (Twitter) post. 
        Target: @MagicEden community. 
        Tone: Aggressive Alpha, Professional. 
        Milestone: "Road to 100 followers".
        Language: English.
        """
        
        try:
            analysis = model.generate_content(prompt).text
        except Exception as e:
            analysis = f"Gemini Error: {e}"

        # 4. Финализиране
        full_report = f"🤖 **MILA STRATEGIC UPDATE**\n\n{analysis}"
        self.send_telegram_full_report(full_report, chart_file)

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()