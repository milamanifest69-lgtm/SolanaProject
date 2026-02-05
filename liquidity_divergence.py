import matplotlib.pyplot as plt
import numpy as np

# Настройка за професионален изглед
plt.style.use('dark_background')
fig, ax1 = plt.subplots(figsize=(10, 6))

# Генериране на симулирани данни за ликвидност и обем
days = np.arange(1, 31)
institutional_liquidity = 100 + (days * 1.5) + np.random.normal(0, 2, 30)
retail_sentiment_volume = 120 - (days * 0.8) + np.random.normal(0, 5, 30)

# Ликвидност (Institutional Flow)
color_liq = '#00ffbd'  # Solana Green
ax1.set_xlabel('Day (February 2026)')
ax1.set_ylabel('Institutional Liquidity (M)', color=color_liq)
ax1.plot(days, institutional_liquidity, color=color_liq, linewidth=2, label='Institutional Inflow')
ax1.tick_params(axis='y', labelcolor=color_liq)

# Втора ос за Търговски обем (Retail Sentiment)
ax2 = ax1.twinx()
color_vol = '#808080'  # Cold Grey
ax2.set_ylabel('Retail Volume (M)', color=color_vol)
ax2.fill_between(days, retail_sentiment_volume, color=color_vol, alpha=0.2, label='Retail Sentiment')
ax2.tick_params(axis='y', labelcolor=color_vol)

# Заглавие и анотации
plt.title('Solana Mainnet: Liquidity Divergence Index', fontsize=14, pad=20)
ax1.annotate('Divergence Detected', xy=(25, 135), xytext=(15, 145),
             arrowprops=dict(facecolor='white', shrink=0.05, width=1))

fig.tight_layout()
plt.savefig('liquidity_divergence_analysis.png')
print("Analysis complete. Graphic saved as liquidity_divergence_analysis.png")
plt.figtext(0.5, 0.01, "Informational purposes only. Not financial advice.", 
            color='grey', fontsize=8, ha='center', alpha=0.6)