import matplotlib.pyplot as plt
import numpy as np

# Сравнителни данни за скорост на трансакции (хипотетични на база новините)
networks = ['Ethereum', 'Layer 2s', 'Solana']
velocity_index = [1.2, 4.5, 12.8] # Solana води убедително

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))

colors = ['#444444', '#888888', '#14F195']
bars = ax.bar(networks, velocity_index, color=colors, alpha=0.8)

# Добавяме LaTeX формула за Capital Efficiency
plt.text(0.5, 10, r'$V_c = \frac{\sum T_x}{Liquidity}$', fontsize=18, color='#14F195')

plt.title('Capital Velocity Index - Feb 2026', fontsize=16, pad=20)
plt.ylabel('Efficiency Units', color='gray')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('velocity_analysis.png')
plt.show()