import matplotlib.pyplot as plt
import numpy as np

# Дефинираме данни за нашата "Еволюция"
# x = време (дни), y = скалируемост на мрежата (хипотетичен модел)
x = np.linspace(0, 10, 100)
y = x**2  # Квадратичен растеж

plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Project Evolution Path', color='#14F195', linewidth=2) # Solana Green

# Добавяме научен елемент - формулата
plt.text(1, 80, r'$E = mc^2 \rightarrow Growth = f(x^2)$', fontsize=14, color='white', 
         bbox=dict(facecolor='black', alpha=0.5))

plt.title('Solana Project Scalability Model', color='white', fontsize=16)
plt.xlabel('Days of Development', color='gray')
plt.ylabel('Network Integration Complexity', color='gray')
plt.grid(True, linestyle='--', alpha=0.3)
plt.style.use('dark_background')

# Запазваме резултата
plt.savefig('first_scientific_update.png')
print("Графиката е генерирана успешно като 'first_scientific_update.png'!")
plt.show()