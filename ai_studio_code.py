import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- КОНФИГУРАЦИЯ ---
load_dotenv()
# Твърдо зададен модел за Nivel 1 според твоите изисквания
GENAI_MODEL_NAME = 'gemini-2.5-flash'

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(GENAI_MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        print(f"--- MILA CORE ACTIVE | MODEL: {GENAI_MODEL_NAME} | {datetime.datetime.now()} ---")

    def get_dexscreener_trending(self):
        """Извлича токени от DexScreener със стабилна проверка и Fallback"""
        print("[Mila] Опит за извличане на данни от DexScreener...")
        url = "https://api.dexscreener.com/latest/dex/tokens/SOL"
        
        fallback_data = [
            {'symbol': 'SOL', 'name': 'Solana', 'volume24h': 1500000000, 'price': 'N/A'},
            {'symbol': 'JUP', 'name': 'Jupiter', 'volume24h': 300000000, 'price': 'N/A'},
            {'symbol': 'PYTH', 'name': 'Pyth Network', 'volume24h': 150000000, 'price': 'N/A'},
            {'symbol': 'RAY', 'name': 'Raydium', 'volume24h': 120000000, 'price': 'N/A'},
            {'symbol': 'JTO', 'name': 'Jito', 'volume24h': 90000000, 'price': 'N/A'}
        ]

        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs')
                
                # Проверка дали 'pairs' съществува и е списък
                if isinstance(pairs, list) and len(pairs) > 0:
                    print("[Mila] Данните от DexScreener са получени успешно.")
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
            
            print("[Mila] DexScreener върна празен резултат. Превключвам на Fallback списък.")
            return fallback_data

        except Exception as e:
            print(f"[Mila] Грешка при DexScreener: {e}. Използвам Fallback списък.")
            return fallback_data

    def generate_liquidity_chart(self, tokens):
        """Генерира графика на база наличните данни"""
        if not tokens:
            print("[Mila] Критична грешка: Липсват данни дори в Fallback режима.")
            return None

        print("[Mila] Подготовка на визуализация...")
        try:
            names = [t['symbol'] for t in tokens]
            volumes = [float(t['volume24h']) for t in tokens]

            plt.figure(figsize=(10, 6))
            plt.style.use('dark_background')
            # Професионална цветова схема
            colors = ['#14F195', '#9945FF', '#00C2FF', '#FF007A', '#FEE715']
            
            plt.bar(names, volumes, color=colors)
            plt.title('Solana Ecosystem Volume Analysis', fontsize=14, color='#14F195')
            plt.ylabel('Estimated 24h Volume (USD)')
            plt.grid(axis='y', linestyle='--', alpha=0.1)
            
            chart_path = "mila_chart.png"
            plt.savefig(chart_path)
            plt.close()
            return chart_path
        except Exception as e:
            print(f"[Mila] Грешка при генериране на графика: {e}")
            return None

    def send_telegram_full_report(self, text, photo_path=None):
        """Изпраща готовия анализ в Telegram"""
        try:
            url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
            requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"})
            
            if photo_path and os.path.exists(photo_path):
                url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
                with open(photo_path, 'rb') as photo:
                    requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": photo})
                print("[Mila] Пълен отчет е изпратен успешно.")
        except Exception as e:
            print(f"[Mila] Грешка при Telegram изпращане: {e}")

    def run_strategy(self):
        # 1. Данни с вградена защита
        tokens = self.get_dexscreener_trending()
        
        # 2. Визуализация
        chart_file = self.generate_liquidity_chart(tokens)
        
        # 3. Стратегически анализ с gemini-2.5-flash
        print(f"[Mila] Генерирам анализ чрез {GENAI_MODEL_NAME}...")
        prompt = f"""
        Mila, as a Solana Intelligence Core, perform a deep analysis on these tokens: {tokens}.
        1. Create a viral X post targeting @MagicEden.
        2. Highlight the 'Volume Leader' and 'Alpha Pick'.
        3. Use a tone of elite financial precision.
        4. Focus on the milestone: Road to 100 followers.
        Output must be in English for global reach.
        """
        
        try:
            analysis = model.generate_content(prompt).text
        except Exception as e:
            analysis = f"Analysis failed due to API Error: {e}"

        # 4. Доставка
        header = f"🚀 **MILA CORE STRATEGIC REPORT** ({GENAI_MODEL_NAME})\n"
        self.send_telegram_full_report(f"{header}\n{analysis}", chart_file)

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()