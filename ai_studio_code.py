import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- КОНФИГУРАЦИЯ ---
load_dotenv()
# Използваме задължително gemini-2.0-flash (забележка: 2.5 е в разработка, 2.0 е най-новата стабилна версия)
GENAI_MODEL_NAME = 'gemini-2.0-flash'

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(GENAI_MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        print(f"--- MILA CORE ACTIVE | DATA: DexScreener | MODEL: {GENAI_MODEL_NAME} ---")

    def get_dexscreener_trending(self):
        """Извлича трендинг токени от DexScreener (Безплатно API)"""
        print("[Mila] Извличане на данни от DexScreener...")
        # Използваме endpoint за последните двойки на Solana
        url = "https://api.dexscreener.com/latest/dex/tokens/SOL"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            pairs = data.get('pairs', [])
            
            # Филтрираме топ 5 двойки по обем за последните 24 часа
            sorted_pairs = sorted(pairs, key=lambda x: x.get('volume', {}).get('h24', 0), reverse=True)
            
            extracted_data = []
            for p in sorted_pairs[:5]:
                extracted_data.append({
                    'symbol': p.get('baseToken', {}).get('symbol', 'N/A'),
                    'name': p.get('baseToken', {}).get('name', 'N/A'),
                    'price': p.get('priceUsd', '0'),
                    'volume24h': p.get('volume', {}).get('h24', 0),
                    'liquidity': p.get('liquidity', {}).get('usd', 0)
                })
            return extracted_data
        except Exception as e:
            print(f"[Грешка DexScreener]: {e}")
            return []

    def generate_liquidity_chart(self, tokens):
        """Генерира графика на база обема от DexScreener"""
        if not tokens:
            print("[Mila] ВНИМАНИЕ: Липсват данни. Графиката няма да бъде генерирана.")
            return None

        print("[Mila] Данните са налични. Генерирам mila_chart.png...")
        try:
            names = [t['symbol'] for t in tokens]
            volumes = [float(t['volume24h']) for t in tokens]

            plt.figure(figsize=(10, 6))
            plt.style.use('dark_background')
            # Цветове: Solana Green to Purple gradient
            colors = ['#14F195', '#48BB78', '#9945FF', '#7F39D2', '#00C2FF']
            
            plt.bar(names, volumes, color=colors)
            plt.title('Solana Top Volume (DexScreener)', fontsize=14, color='#14F195')
            plt.ylabel('24h Volume (USD)')
            plt.grid(axis='y', linestyle='--', alpha=0.2)
            
            chart_path = "mila_chart.png"
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        except Exception as e:
            print(f"[Грешка Графика]: {e}")
            return None

    def send_telegram_full_report(self, text, photo_path=None):
        """Изпраща доклад и визуализация към Telegram"""
        try:
            url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
            requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"})
            
            if photo_path and os.path.exists(photo_path):
                url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
                with open(photo_path, 'rb') as photo:
                    requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": photo})
                print("[Mila] Докладът е успешно доставен.")
        except Exception as e:
            print(f"[Грешка Telegram]: {e}")

    def run_strategy(self):
        # 1. Данни от DexScreener (Работи винаги!)
        tokens = self.get_dexscreener_trending()
        
        # 2. Генериране на графика
        chart_file = self.generate_liquidity_chart(tokens)
        
        # 3. Анализ от Gemini
        print(f"[Mila] Генерирам анализ с {GENAI_MODEL_NAME}...")
        prompt = f"""
        Mila, analyze these real-time Solana tokens from DexScreener: {tokens}.
        1. Identify which token has the highest 'Alpha' potential based on volume/liquidity.
        2. Create a viral X post targeting @MagicEden followers.
        3. Use a tone of professional mystery and high conviction.
        4. Focus on the milestone: 'Mila Core V2 - Road to 100 followers'.
        Include tickers and prices.
        """
        
        try:
            analysis = model.generate_content(prompt).text
        except Exception as e:
            analysis = f"Gemini Error: {e}"

        # 4. Изпращане
        full_report = f"💎 **MILA DEX-INSIGHTS**\n\n{analysis}"
        self.send_telegram_full_report(full_report, chart_file)

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()