import os
import datetime
from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
app = Flask(__name__)

# Глобален контейнер за данни (In-memory buffer)
data_buffer = []

class MilaHeliusProcessor:
    def __init__(self):
        print(f"--- MILA HELIUS LISTENER ACTIVE | PORT: 5000 | {datetime.datetime.now().strftime('%H:%M')} ---")

    def process_incoming_data(self, json_data):
        """Превръща суровия JSON в Pandas DataFrame и го добавя към буфера."""
        try:
            # Helius праща списък от транзакции
            df = pd.json_normalize(json_data)
            
            # Извличане на ключови метрики: Тип транзакция, Слот, Подпис
            essential_info = df[['type', 'slot', 'signature', 'timestamp']]
            data_buffer.append(essential_info)
            
            print(f"[MILA] Ingested {len(essential_info)} transactions. Buffer size: {len(data_buffer)}")
            
            # Визуализация при натрупване на критична маса (напр. 5 пакета данни)
            if len(data_buffer) >= 5:
                self.visualize_activity()
                
        except Exception as e:
            print(f"[ERROR] Data processing failed: {e}")

    def visualize_activity(self):
        """Генерира графика на активността в реално време."""
        if not data_buffer:
            return

        print("[Mila] Generating real-time activity chart...")
        full_df = pd.concat(data_buffer, ignore_index=True)
        
        # Броене на типовете транзакции (Swap, Transfer, NFT_Mint и т.н.)
        activity_counts = full_df['type'].value_counts()

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')

        activity_counts.plot(kind='bar', color='#00FFA3', edgecolor='#9945FF', ax=ax)

        # Terminal Aesthetics
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color='#2D2D2D', linestyle='--', alpha=0.5)
        
        plt.title(" > MILA_HELIUS_MONITOR: TRANSACTION_TYPES_FLOW", 
                  loc='left', color='#00FFA3', family='monospace', fontsize=10, pad=20)
        plt.xticks(rotation=45, family='monospace', color='#00FFA3')
        plt.yticks(family='monospace', color='#9945FF')

        path = "helius_realtime_activity.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        print(f"[VISUALIZER] Activity map secured: {path}")
        
        # Изчистване на буфера след визуализация
        data_buffer.clear()

# Инициализация на процесора
processor = MilaHeliusProcessor()

@app.route('/webhook', methods=['POST'])
def helius_webhook():
    """Endpoint за приемане на данни от Helius."""
    raw_data = request.json
    if not raw_data:
        return jsonify({"status": "error", "message": "Empty payload"}), 400

    processor.process_incoming_data(raw_data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Стартиране на локалния сървър
    app.run(port=5000)