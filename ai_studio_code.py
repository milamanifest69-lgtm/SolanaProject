import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
# Използваме gemini-2.5-flash за Nivel 1 ресурси
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.hour = datetime.datetime.now().hour
        # Вътрешни данни (Fallback) - Използваме чисти числа (Float/Int)
        self.internal_alpha = {
            'SOL': 1850000000.0, 
            'JTO': 125000000.0,  
            'PYTH': 85000000.0,  
            'JUP': 310000000.0   
        }
        print(f"--- MILA TERMINAL v4.2 | ALPHA_FORMAT_ACTIVE | {datetime.datetime.now().strftime('%H:%M')} ---")

    def human_format(self, num, pos=None):
        """Превръща числата в професионален M/B формат за етикетите на графиката"""
        if num is None or num == 0: return "0"
        if abs(num) >= 1000000000:
            return f'{num / 1000000000:.1f}B'
        if abs(num) >= 1000000:
            return f'{num / 1000000:.1f}M'
        if abs(num) >= 1000:
            return f'{num / 1000:.1f}K'
        return str(int(num))

    def fetch_dex_data(self):
        """Стабилно извличане от DexScreener"""
        url = "https://api.dexscreener.com/latest/dex/tokens/SOL"
        try:
            response = requests.get(url, timeout=12)
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs')
                if isinstance(pairs, list) and len(pairs) > 0:
                    return pairs
            return None
        except:
            return None

    def generate_terminal_chart(self, labels, values, title, chart_type='bar'):
        """Генерира графика в стил High-End Terminal"""
        if not labels or not values:
            labels = list(self.internal_alpha.keys())
            values = list(self.internal_alpha.values())
            title = f"SYSTEM_STANDBY: {title}"

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')
        
        c_green = '#00FFA3' 
        c_purple = '#9945FF'

        if chart_type == 'bar':
            ax.bar(labels, values, color=c_green, edgecolor=c_purple, width=0.5, linewidth=0.8)
        else:
            ax.plot(labels, values, color=c_green, marker='s', linewidth=2, markersize=6)

        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color='#262626', linestyle='--', alpha=0.6)
        
        plt.xticks(family='monospace', color=c_green, fontsize=9)
        plt.yticks(family='monospace', color=c_purple, fontsize=8)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.human_format))
        
        plt.title(f" > MILA_TERMINAL_V4.2: {title}", loc='left', color=c_green, family='monospace', fontsize=9, pad=15)
        
        path = "mila_output.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def run_strategy(self):
        pairs = self.fetch_dex_data()
        mode = self.hour % 3
        labels, values, chart_path = [], [], None

        if mode == 0: 
            title = "STAKING_&_MEV_INTENSITY"
            if pairs:
                targets = [p for p in pairs if p.get('baseToken', {}).get('symbol') in ['SOL', 'JTO']]
                labels = [t.get('baseToken', {}).get('symbol') for t in targets]
                values = [float(t.get('volume', {}).get('h24', 0)) for t in targets]
            chart_path = self.generate_terminal_chart(labels, values, title, 'bar')

        elif mode == 1: 
            title = "LIQUIDITY_VELOCITY_SCAN"
            if pairs:
                top_5 = sorted(pairs, key=lambda x: float(x.get('volume', {}).get('h24', 0)), reverse=True)[:5]
                labels = [t.get('baseToken', {}).get('symbol') for t in top_5]
                values = [float(t.get('volume', {}).get('h24', 0)) for t in top_5]
            chart_path = self.generate_terminal_chart(labels, values, title, 'bar')

        else: 
            title = "NETWORK_SENTIMENT_QUANTS"
            labels, values = ['SOL', 'JUP', 'PYTH', 'RAY'], [1900000000.0, 450000000.0, 180000000.0, 110000000.0]
            chart_path = self.generate_terminal_chart(labels, values, title, 'line')

        # ALPHA FORMAT PROMPT
        prompt = f"""
        Mila Core Intelligence. Data Input: {title} | {labels} | {values}.
        
        Construct an X update using 'The Alpha Format':
        Line 1 (Hook): Direct statement on Solana network intensity.
        Line 2 (Data): List key metrics (Vol, Price, or Ratio) from input.
        Line 3 (Insight): Cold, analytical conclusion (No explanations).
        Line 4 (Mission): Strategic goal: 100 followers for Magic Eden access.

        Rules:
        - Professional Trading Terminal Tone.
        - Strictly under 270 characters.
        - Language: English only.
        - No excessive emojis. 
        - Assume elite audience.
        """

        try:
            analysis = model.generate_content(prompt).text
            self.dispatch(analysis, title, chart_path)
        except Exception as e:
            print(f"GenAI Error: {e}")

    def dispatch(self, text, theme, photo_path):
        header = f"⚡ **MILA_SYSTEM_LOG: {theme}**"
        full_msg = f"{header}\n\n{text}"
        url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": full_msg, "parse_mode": "Markdown"})
        
        if photo_path and os.path.exists(photo_path):
            url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(photo_path, 'rb') as f:
                requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": f})
        print(f"[Mila] Alpha Cycle Complete: {theme}")

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()