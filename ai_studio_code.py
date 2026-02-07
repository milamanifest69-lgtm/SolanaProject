import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
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
        print(f"--- MILA CORE V2.1 (VISUAL EDITION) СТАРТИРАНА ---")

    def _rate_limit_check(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < 1.2:
            time.sleep(1.2 - elapsed)
        self.last_request_time = time.time()

    # --- МОДУЛ: ГЕНЕРИРАНЕ НА ГРАФИКА ---
    def generate_liquidity_chart(self, tokens):
        """Създава професионална графика за ликвидните потоци"""
        print("[Mila] Генерирам визуален анализ...")
        try:
            names = [t.get('symbol', 'Unknown') for t in tokens]
            liquidity = [t.get('v24hUSD', 0) for t in tokens] # Използваме 24ч обем като метрика

            plt.figure(figsize=(10, 6))
            plt.style.use('dark_background')
            colors = ['#14F195', '#9945FF', '#00C2FF', '#FF007A', '#F0E442'] # Solana Colors
            
            bars = plt.bar(names, liquidity, color=colors)
            plt.title('Top Trending Solana Tokens by 24h Volume', fontsize=16, color='white')
            plt.xlabel('Token Symbol', fontsize=12)
            plt.ylabel('Volume (USD)', fontsize=12)
            
            # Запазване на снимката
            chart_path = "mila_chart.png"
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        except Exception as e:
            print(f"Chart Error: {e}")
            return None

    def get_birdeye_trending(self):
        self._rate_limit_check()
        url = "https://public-api.birdeye.so/public/trending?list_iteration=10"
        headers = {"X-API-KEY": self.birdeye_key}
        try:
            response = requests.get(url, headers=headers).json()
            return response.get('data', {}).get('tokens', [])[:5]
        except: return []

    # --- МОДУЛ: ИЗПРАЩАНЕ НА СНИМКА В TELEGRAM ---
    def send_telegram_full_report(self, text, photo_path=None):
        # Първо пращаме текста
        url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"})
        
        # После пращаме снимката, ако има такава
        if photo_path and os.path.exists(photo_path):
            url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(photo_path, 'rb') as photo:
                requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": photo})
            print("[Mila] Графиката е изпратена!")

    def run_strategy(self):
        # 1. Данни
        liq_data = self.get_birdeye_trending()
        
        # 2. Генериране на графика
        chart_file = self.generate_liquidity_chart(liq_data)
        
        # 3. Генериране на текст
        prompt = f"Create a viral X post about these Solana tokens: {liq_data}. Mention @MagicEden. Professional and hype tone."
        report_text = model.generate_content(prompt).text

        # 4. Изпращане на всичко
        self.send_telegram_full_report(f"🚀 **НОВ ДОКЛАД С ГРАФИКА** 🚀\n\n{report_text}", chart_file)

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()