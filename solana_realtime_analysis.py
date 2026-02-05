import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Настройка за студен, професионален стил
plt.style.use('dark_background')

def fetch_solana_data():
    # Извличане на данни за Solana (SOL) от CoinGecko API
    url = "https://api.coingecko.com/api/v3/coins/solana/market_chart"
    params = {'vs_currency': 'usd', 'days': '7', 'interval': 'daily'}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Обработка на цени и обеми
        prices = data['prices']
        volumes = data['total_volumes']
        
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['volume'] = [v[1] for v in volumes]
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
    except Exception as e:
        print(f"Data acquisition error: {e}")
        return None

def generate_analysis():
    df = fetch_solana_data()
    if df is None: return

    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Визуализация на Цена (Institutional Metric)
    color_price = '#9945FF' # Solana Purple
    ax1.set_xlabel('Timeline (UTC)')
    ax1.set_ylabel('SOL Price (USD)', color=color_price, fontsize=12)
    ax1.plot(df['timestamp'], df['price'], color=color_price, linewidth=3, label='Price Action')
    ax1.tick_params(axis='y', labelcolor=color_price)

    # Визуализация на Обем (Liquidity Metric)
    ax2 = ax1.twinx()
    color_vol = '#14F195' # Solana Green
    ax2.set_ylabel('24h Trading Volume (USD)', color=color_vol, fontsize=12)
    ax2.bar(df['timestamp'], df['volume'], color=color_vol, alpha=0.3, width=0.5, label='Network Liquidity')
    ax2.tick_params(axis='y', labelcolor=color_vol)

    plt.title('Solana Network: Quantitative Liquidity & Price Equilibrium', fontsize=16, pad=25)
    
    # Добавяне на клеймо за автентичност
    plt.figtext(0.15, 0.8, f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", color='white', fontsize=10)
    
    fig.tight_layout()
    filename = 'solana_realtime_metrics.png'
    plt.savefig(filename)
    print(f"Real-time analysis complete. File saved as: {filename}")

if __name__ == "__main__":
    generate_analysis()