import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def get_real_sol_price():
    """Извлича реалната цена на SOL от Binance"""
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDC"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data['price'])
    except Exception as e:
        print(f"Грешка при вземане на цена: {e}")
        return None

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": message}
        try:
            requests.get(url, params=params)
        except Exception as e:
            print(f"Грешка при Telegram: {e}")

# --- ГЛАВНО ИЗПЪЛНЕНИЕ ---

print("Solana Monitor Active с реални данни...")
send_telegram_msg("🚀 Mila е рестартирана и вече следи реалния пазар!")

while True:
    current_price = get_real_sol_price()
    
    if current_price:
        timestamp = time.strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] SOL: ${current_price}"
        print(log_msg)
        
        # Изпращаме РЕАЛНАТА цена в Telegram
        send_telegram_msg(f"📊 Актуална цена на SOL: ${current_price}")
    
    # Изчакваме 1 час (3600 секунди) за следващото обновяване
    time.sleep(3600)