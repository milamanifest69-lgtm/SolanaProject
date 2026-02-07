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
# Използваме gemini-2.0-flash като основен стабилен модел
MODEL_NAME = 'gemini-2.0-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaCore:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.hour = datetime.datetime.now().hour
        # Вътрешни исторически данни (Fallback) - Използваме стандартни цели числа
        self.internal_alpha = {
            'SOL': 1850000000, 
            'JTO': 125000000,  
            'PYTH': 85000000,  
            'JUP': 310000000   
        }
        print(f"--- MILA TERMINAL v4.2 | SYNTAX_FIXED | {datetime.datetime.now().strftime('%H:%M')} ---")

    def human_format(self, num, pos=None):
        """Превръща числата в професионален M/B формат за етикетите на осите"""
        if num is None or num == 0: return "0"
        if abs(num) >= 1_000_000_000:
            return f'{num / 1_000_000_000:.1f}B'
        if abs(num) >= 1_000_000:
            return f'{num / 1_000_000:.1f}M'
        if abs(num) >= 1_000:
            return f'{num / 1_000:.1f}K'
        return str(int(num))

    def fetch_dex_data(self):
        """Стабилно извличане с проверка за наличност"""
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
        """Генерира графика. Ако няма данни, чертае STANDBY екран."""
        if not labels or not values:
            print("[Mila] No real-time data detected. Activating INTERNAL_FALLBACK.")
            labels = list(self.internal_alpha.keys())
            values = list(self.internal_alpha.values())
            title = f"INTERNAL_ESTIMATE: {title}"

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')
        
        c_green = '#00FFA3' # Spring Green
        c_purple = '#9945FF' # Solana Purple

        if chart_type == 'bar':
            ax.bar(labels, values, color=c_green, edgecolor=c_purple, width=0.5, linewidth=0.8)
        else:
            ax.plot(labels, values, color=c_green, marker='s', linewidth=2, markersize=6, mfc=c_purple)

        # UI Детайли
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color='#262626', linestyle='--', alpha=0.6)
        
        # Настройка на шрифтове (Monospace)
        plt.xticks(family='monospace', color=c_green, fontsize=9)
        plt.yticks(family='monospace', color=c_purple, fontsize=8)
        
        # Форматиране на осите в M/B чрез human_format функцията
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(self.human_format))
        
        # Заглавие тип Терминал
        plt.title(f" > MILA_SYSTEM_WINDOW: {title}", loc='left', color=c_green, family='monospace', fontsize=9, pad=15)
        
        # Малък статус маркер
        ax.text(0.99, 0.02, 'CORE_V4.2_STABLE', transform=ax.transAxes, color=c_purple, family='monospace', fontsize=7, ha='right')

        path = "mila_output.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def run_strategy(self):
        pairs = self.fetch_dex_data()
        mode = self.hour % 3
        
        labels, values, chart_path = [], [], None

        if mode == 0: # Fundamental (SOL/JTO)
            title = "STAKING_&_MEV_DYNAMICS"
            if pairs:
                targets = [p for p in pairs if p.get('baseToken', {}).get('symbol') in ['SOL', 'JTO']]
                labels = [t.get('baseToken', {}).get('symbol') for t in targets]
                values = [float(t.get('volume', {}).get('h24', 0)) for t in targets]
            chart_path = self.generate_terminal_chart(labels, values, title, 'bar')

        elif mode == 1: # Alpha Scanner
            title = "LIQUIDITY_VELOCITY_ALERTS"
            if pairs:
                top_5 = sorted(pairs, key=lambda x: float(x.get('volume', {}).get('h24', 0)), reverse=True)[:5]
                labels = [t.get('baseToken', {}).get('symbol') for t in top_5]
                values = [float(t.get('volume', {}).get('h24', 0)) for t in top_5]
            chart_path = self.generate_terminal_chart(labels, values, title, 'bar')

        else: # Ecosystem Dynamics (Ред 124 - Поправен)
            title = "NETWORK_SENTIMENT_SCAN"
            # Използваме научно представяне (e9 за милиарди, e6 за милиони)
            labels = ['SOL', 'JUP', 'PYTH', 'RAY']
            values = [1.9e9, 450e6, 180e6, 110e6] 
            chart_path = self.generate_terminal_chart(labels, values, title, 'line')

        # AI Анализ
        prompt = f"""
        Mila, create a terminal-style update for X.
        Current Topic: {title}. 
        Data Context: {labels} | {values}.
        Target: @MagicEden road to 100 followers. 
        Focus: Actionable Insight + JTO MEV context if applicable.
        Length: < 260 chars.
        """

        try:
            analysis = model.generate_content(prompt).text
            self.dispatch(analysis, title, chart_path)
        except Exception as e:
            print(f"GenAI Error: {e}")

    def dispatch(self, text, theme, photo_path):
        header = f"⚡ **MILA_SYSTEM_LOG: {theme}**"
        full_msg = f"{header}\n\n{text}"
        
        # Telegram Text
        url_text = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        requests.post(url_text, json={"chat_id": self.tg_chat_id, "text": full_msg, "parse_mode": "Markdown"})
        
        # Telegram Photo
        if photo_path and os.path.exists(photo_path):
            url_photo = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
            with open(photo_path, 'rb') as f:
                requests.post(url_photo, data={"chat_id": self.tg_chat_id}, files={"photo": f})
        print(f"[Mila] Operational Cycle Complete: {theme}")

if __name__ == "__main__":
    mila = MilaCore()
    mila.run_strategy()