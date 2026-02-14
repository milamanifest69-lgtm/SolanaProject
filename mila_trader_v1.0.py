import os
import pandas as pd
import time
import datetime
import requests
from dotenv import load_dotenv

# --- INITIALIZATION ---
load_dotenv()
# Пътят към лога, който генерира listener-ът
INTELLIGENCE_LOG = "/root/SolanaProject/ARCHIVE/intelligence_log.csv"
JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"

class MilaTraderV1:
    def __init__(self):
        self.min_confidence = 2 # Нужни са поне 2 сигнала за действие
        print(f"--- MILA TRADER v1.0 ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def analyze_signals(self):
        """Чете CSV лога и търси пазарни аномалии."""
        if not os.path.exists(INTELLIGENCE_LOG):
            print("[TRADER] No intelligence log found. Standing by.")
            return None

        try:
            df = pd.read_csv(INTELLIGENCE_LOG)
            if df.empty:
                return None

            # Филтрираме само събития от последните 10 минути
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            ten_mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
            recent_signals = df[df['timestamp'] > ten_mins_ago]

            if len(recent_signals) >= self.min_confidence:
                print(f"[TRADER] High-confidence signals detected: {len(recent_signals)}")
                return recent_signals
            
            return None
        except Exception as e:
            print(f"[TRADER ERROR] Signal analysis failed: {e}")
            return None

    def get_jupiter_quote(self, input_mint, output_mint, amount_sol):
        """Проверява цената в Jupiter преди изпълнение."""
        # Превръщаме SOL в Lamports (1 SOL = 10^9 Lamports)
        amount_lamports = int(amount_sol * 1_000_000_000)
        
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount_lamports,
            "slippageBps": 50 # 0.5% приплъзване
        }
        
        try:
            response = requests.get(JUPITER_QUOTE_API, params=params)
            return response.json()
        except Exception as e:
            print(f"[TRADER ERROR] Jupiter Quote failed: {e}")
            return None

    def run_trading_cycle(self):
        """Основен цикъл на агента."""
        while True:
            signals = self.analyze_signals()
            if signals is not None:
                # Тук ще добавим логиката за автоматично подписване на транзакции
                print("[TRADER] Evaluating execution for detected signals...")
                # Пример: Показваме намерените суапове
                for index, row in signals.iterrows():
                    print(f" > Signal: {row['label']} | Amount: {row['amount_sol']} SOL")
            
            # Изчакване 60 секунди преди следващия скан
            time.sleep(60)

if __name__ == "__main__":
    trader = MilaTraderV1()
    trader.run_trading_cycle()