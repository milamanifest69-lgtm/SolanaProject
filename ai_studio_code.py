import os
import time
import datetime
import requests
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- КОНФИГУРАЦИЯ ЗА GITHUB ACTIONS / VS CODE ---
load_dotenv()
GENAI_MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(GENAI_MODEL_NAME)

class MilaIntelligence:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.timestamp = datetime.datetime.now()
        print(f"--- MILA CORE v3.0 | MODE: AUTONOMOUS | {self.timestamp.strftime('%H:%M:%S')} ---")

    def get_market_data(self):
        """Извлича данни от DexScreener със защита срещу NoneType."""
        print("[Mila] Скенирам пазарни данни...")
        url = "https://api.dexscreener.com/latest/dex/tokens/SOL"
        fallback = [{'symbol': 'SOL', 'price': 'N/A', 'volume': 0, 'makers': 0, 'liquidity': 1}]
        
        try:
            response = requests.get(url, timeout=15)
            if response.status_code != 200: return fallback
            
            data = response.json()
            pairs = data.get('pairs')
            if not isinstance(pairs, list): return fallback
            
            extracted = []
            for p in pairs[:10]:
                extracted.append({
                    'symbol': p.get('baseToken', {}).get('symbol', 'N/A'),
                    'price': p.get('priceUsd', '0'),
                    'volume': p.get('volume', {}).get('h24', 0),
                    'makers': p.get('makers', {}).get('h24', 0),
                    'liquidity': p.get('liquidity', {}).get('usd', 1),
                    'change': p.get('priceChange', {}).get('h24', 0)
                })
            return extracted
        except Exception as e:
            print(f"Error fetching data: {e}")
            return fallback

    def analyze_sentiment(self, tokens):
        """Определя настроението на пазара на база волатилност и обем."""
        avg_change = sum(float(t['change']) for t in tokens if t['change']) / len(tokens)
        if avg_change > 10: return "🚀 EUPHORIC"
        if avg_change < -10: return "😨 PANIC/FEAR"
        return "📊 NEUTRAL/ACCUMULATION"

    def run_strategy(self):
        # 1. Извличане на данни
        tokens = self.get_market_data()
        sentiment = self.analyze_sentiment(tokens)
        
        # 2. Ротация на темата (Rotation Logic)
        # 0 = Tech/Price, 1 = AI Agents, 2 = Magic Eden/NFTs
        topic_mode = self.timestamp.hour % 3
        themes = ["TECHNICAL_ALPHA", "AI_AGENT_META", "MAGIC_EDEN_TRENDS"]
        current_theme = themes[topic_mode]

        # 3. Проверка за ULTRA ALPHA
        ultra_alpha = []
        for t in tokens:
            # Сигнал: Много малко ликвидност, но огромен брой уникални трейдъри (makers)
            if t['makers'] > 1000 and t['liquidity'] < 50000:
                ultra_alpha.append(t['symbol'])

        # 4. Прогноза за 12 часа (SOL & JTO Focus)
        sol_data = next((t for t in tokens if t['symbol'] == 'SOL'), None)
        jto_data = next((t for t in tokens if t['symbol'] == 'JTO'), None)

        # 5. Генериране на Интелигентен Репорт
        prompt = f"""
        Mila Core V3 Strategy. 
        Theme: {current_theme}
        Market Sentiment: {sentiment}
        Data: {tokens[:5]}
        Ultra Alpha Detected: {ultra_alpha}
        SOL/JTO Status: SOL at {sol_data['price'] if sol_data else 'N/A'}, JTO Vol: {jto_data['volume'] if jto_data else 'N/A'}

        Instructions:
        1. If theme is TECHNICAL_ALPHA: Forecast SOL & JTO for next 12h.
        2. If theme is AI_AGENT_META: Discuss latest AI agent wallet movements ($GOAT, $ZEREBRO).
        3. If theme is MAGIC_EDEN_TRENDS: Focus on NFT volume and Magic Eden 100-follower goal.
        4. Always provide an 'Actionable Move'.
        5. Tone: Elite Intelligence Analyst.
        6. Style: Breaking News (English).
        """

        try:
            analysis = model.generate_content(prompt).text
            
            # Добавяне на таг ако е Ultra Alpha
            if ultra_alpha:
                analysis = f"🚨 **ULTRA ALPHA ALERT: {ultra_alpha}** 🚨\n\n" + analysis
            
            self.dispatch(analysis, current_theme)
        except Exception as e:
            print(f"GenAI Error: {e}")

    def dispatch(self, text, theme):
        """Изпращане към Telegram."""
        header = f"⚡ **MILA CORE: {theme}**\n"
        full_text = f"{header}\n{text}"
        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        requests.post(url, json={"chat_id": self.tg_chat_id, "text": full_text, "parse_mode": "Markdown"})
        print(f"[Mila] Report {theme} dispatched.")

if __name__ == "__main__":
    mila = MilaIntelligence()
    mila.run_strategy()