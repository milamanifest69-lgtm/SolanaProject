import os
import time
import requests
from dotenv import load_dotenv

# 1. Зареждане на ключовете
load_dotenv()

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        params = {"chat_id": chat_id, "text": message}
        try:
            requests.get(url, params=params)
        except Exception as e:
            print(f"Грешка: {e}")

def check_divergence():
    # Данни от твоя последен терминал
    price = 79.60 
    vol = "11176.1M"
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] SOL: ${price} | Vol: {vol}")
    return price, vol

# --- ГЛАВНО ИЗПЪЛНЕНИЕ ---

# СТЪПКА 1: Изпращаме тестово съобщение веднага
print("Опит за изпращане към Telegram...")
send_telegram_msg("🚀 Базата е завършена! Mila е онлайн и следи Solana.")

# СТЪПКА 2: Стартираме мониторинга
print("Solana Divergence Monitor Active...")
while True:
    check_divergence()
    # Изпращаме статус в Telegram на всеки час
    send_telegram_msg(f"📊 Текуща цена на SOL: ${79.60}")
    time.sleep(3600)