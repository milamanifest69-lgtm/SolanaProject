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

class AlphaScanner:
    """Търси необичайни скокове в обема и Smart Money движения."""
    def __init__(self):
        self.url = "https://api.dexscreener.com/latest/dex/tokens/SOL"

    def scan_for_alpha(self):
        print("[Mila] AlphaScanner: Анализирам Smart Money потоци...")
        try:
            response = requests.get(self.url, timeout=10)
            data = response.json()
            pairs = data.get('pairs', [])
            
            alpha_picks = []
            for p in pairs:
                vol_24h = float(p.get('volume', {}).get('h24', 0))
                liq = float(p.get('liquidity', {}).get('usd', 1)) # Избягваме деление на 0
                
                # Метрика: Обемът е над 5 пъти по-голям от ликвидността (Сигнал за натрупване)
                if vol_24h > liq * 5 and vol_24h > 50000:
                    alpha_picks.append({
                        'symbol': p.get('baseToken', {}).get('symbol'),
                        'ratio': round(vol_24h / liq, 2),
                        'volume': vol_24h,
                        'price': p.get('priceUsd')
                    })
            return sorted(alpha_picks, key=lambda x: x['ratio'], reverse=True)[:3]
        except Exception as e:
            print(f"AlphaScanner Error: {e}")
            return []

class MilaCore:
    def __init__(self):
        self.scanner = AlphaScanner()
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        print(f"--- MILA INTELLIGENCE CORE ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def format_breaking_news(self, raw_analysis):
        """Форматира анализа в агресивен Breaking News стил."""
        timestamp = datetime.datetime.now().strftime('%H:%M')
        header = f"🚨 **BREAKING: SOLANA ALPHA LEAK** [{timestamp}] 🚨\n"
        footer = "\n\n⚠️ *Actionable Insight: Monitor entry zones carefully. NFA.*"
        return f"{header}{raw_analysis}{footer}"

    def generate_terminal_chart(self, alpha_data):
        """Графика в стил High-End Terminal за Alpha токените."""
        if not alpha_data: return None
        try:
            names = [t['symbol'] for t in alpha_data]
            ratios = [t['ratio'] for t in alpha_data]

            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0A0A0A')
            ax.set_facecolor('#0A0A0A')

            ax.bar(names, ratios, color='#00FFA3', edgecolor='#9945FF', alpha=0.8)
            
            # Терминален минимализъм
            for s in ax.spines.values(): s.set_visible(False)
            ax.yaxis.grid(True, color='#2D2D2D', linestyle='--')
            plt.title(' > ALPHA_SCANNER: VOL_TO_LIQ_RATIO', loc='left', color='#00FFA3', family='monospace', fontsize=9)
            
            path = "mila_alpha_chart.png"
            plt.tight_layout()
            plt.savefig(path, facecolor='#0A0A0A')
            plt.close()
            return path
        except: return None

    def run_operational_cycle(self):
        # 1. Скениране за Alpha
        alpha_picks = self.scanner.scan_for_alpha()
        
        # 2. Визуализация
        chart = self.generate_terminal_chart(alpha_picks)
        
        # 3. Генериране на Actionable Insight
        prompt = f"""
        Mila, as a Strategic Alpha Analyst, interpret this data: {alpha_picks}.
        1. Give a 'Breaking News' style report for X.
        2. Provide 'Actionable Insight': What should our community do? (e.g. Watch for retest, Avoid high slippage, Look for Smart Money wallets).
        3. Tone: Aggressive, Elite, Quant.
        4. Target: Global Solana investors and @MagicEden.
        """
        
        try:
            raw_insight = model.generate_content(prompt).text
            final_report = self.format_breaking_news(raw_insight)
            
            # 4. Диспечиране
            self.send_to_telegram(final_report, chart)
        except Exception as e:
            print(f"Cycle Error: {e}")

    def send_to_telegram(self, text, photo):
        url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": text, "parse_mode": "Markdown"})
        if photo:
            url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(photo, 'rb') as p:
                requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": p})
        print("[Mila] Alpha Intelligence Dispatched.")

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_operational_cycle()