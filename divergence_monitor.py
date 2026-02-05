import os
import time
import requests
from datetime import datetime

def check_divergence():
    url = "https://api.coingecko.com/api/v3/coins/solana/market_chart"
    params = {'vs_currency': 'usd', 'days': '1'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Вземаме последната цена и последния обем
        current_price = data['prices'][-1][1]
        current_volume = data['total_volumes'][-1][1]
        
        # Логика за засичане на аномалия (примерна)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] SOL: ${current_price:.2f} | Vol: {current_volume/1e6:.1f}M")
        
        # Тук можем да добавим автоматично генериране на графика при аномалия
        return True
    except Exception as e:
        print(f"Monitoring Error: {e}")
        return False

print("Solana Divergence Monitor Active. Scanning every 60 minutes...")
while True:
    check_divergence()
    # Изчакване от 1 час (3600 секунди)
    time.sleep(3600)
    import requests
import os

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)
    send_telegram_msg("🚀 Система Mila: Връзката е установена. Мониторингът на Solana започва!")