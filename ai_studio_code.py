import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- КОНФИГУРАЦИЯ ---
load_dotenv()
GENAI_MODEL_NAME = 'gemini-2.5-flash'

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(GENAI_MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        print(f"--- MILA TERMINAL ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def get_dexscreener_trending(self):
        """Извлича токени със стабилна проверка и Fallback"""
        url = "https://api.dexscreener.com/latest/dex/tokens/SOL"
        fallback_data = [
            {'symbol': 'SOL', 'volume24h': 1500000000},
            {'symbol': 'JUP', 'volume24h': 450000000},
            {'symbol': 'PYTH', 'volume24h': 180000000},
            {'symbol': 'RAY', 'volume24h': 120000000},
            {'symbol': 'JTO', 'volume24h': 95000000}
        ]
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs')
                if isinstance(pairs, list) and len(pairs) > 0:
                    sorted_pairs = sorted(pairs, key=lambda x: x.get('volume', {}).get('h24', 0), reverse=True)
                    return [{'symbol': p.get('baseToken', {}).get('symbol', 'N/A'), 
                             'volume24h': p.get('volume', {}).get('h24', 0)} for p in sorted_pairs[:5]]
            return fallback_data
        except:
            return fallback_data

    def generate_terminal_chart(self, tokens):
        """Генерира графика в стил High-End Trading Terminal"""
        if not tokens: return None

        print("[Mila] Рендерирам терминална графика...")
        try:
            names = [t['symbol'] for t in tokens]
            volumes = [float(t['volume24h']) for t in tokens]

            # Настройки на фигурата
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0A0A0A')
            ax.set_facecolor('#0A0A0A')

            # Основна графика (Spring Green)
            bars = ax.bar(names, volumes, color='#00FFA3', width=0.6, edgecolor='#9945FF', linewidth=0.5)

            # Изчистване на рамките (Spines)
            for spine in ['top', 'right', 'left', 'bottom']:
                ax.spines[spine].set_visible(False)

            # Настройка на мрежата
            ax.yaxis.grid(True, color='#2D2D2D', linestyle='--', alpha=0.5)
            ax.set_axisbelow(True)

            # Шрифтове и етикети (Monospace)
            plt.xticks(family='monospace', color='#00FFA3', fontsize=10)
            plt.yticks(family='monospace', color='#9945FF', fontsize=8)
            
            # Заглавие в горния ляв ъгъл (Терминален стил)
            plt.title(' > MILA_CORE_SYSTEM: SOL_VOLUME_MONITOR_V2.1', 
                      loc='left', color='#00FFA3', family='monospace', fontsize=9, pad=20)

            # Добавяне на малък надпис за акцент
            ax.text(0.98, 0.02, 'SYSTEM_STATUS: OPERATIONAL', transform=ax.transAxes, 
                    color='#9945FF', family='monospace', fontsize=7, ha='right', alpha=0.7)

            chart_path = "mila_chart.png"
            plt.tight_layout()
            plt.savefig(chart_path, dpi=120, facecolor='#0A0A0A')
            plt.close()
            return chart_path
        except Exception as e:
            print(f"[Mila] Chart Error: {e}")
            return None

    def send_report(self, text, photo_path):
        try:
            url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
            requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"})
            
            if photo_path and os.path.exists(photo_path):
                url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
                with open(photo_path, 'rb') as photo:
                    requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": photo})
                print("[Mila] Terminal Report Dispatched.")
        except Exception as e:
            print(f"[Mila] Dispatch Error: {e}")

    def run_strategy(self):
        tokens = self.get_dexscreener_trending()
        chart_file = self.generate_terminal_chart(tokens)
        
        print(f"[Mila] Генерирам анализ с {GENAI_MODEL_NAME}...")
        prompt = f"""
        Mila Core Intelligence. Data: {tokens}.
        1. Professional Viral X Post (English).
        2. Tone: Quant Analyst / Trading Terminal.
        3. Mentions: @MagicEden milestone 100 followers.
        4. Focus on volume-weighted alpha.
        """
        
        try:
            analysis = model.generate_content(prompt).text
        except Exception as e:
            analysis = f"Terminal Error: {e}"

        header = f"⚡ **MILA TERMINAL: STRATEGIC_UPDATE**\n"
        self.send_report(f"{header}\n{analysis}", chart_file)

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()