import os
import csv
import json
import datetime
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# --- INITIALIZATION ---
load_dotenv()
app = Flask(__name__)

# КОНФИГУРАЦИЯ
# Променяме прага на 100 SOL за чиста Whale Alpha
ARCHIVE_PATH = "/root/SolanaProject/ARCHIVE/intelligence_log.csv"
MIN_SOL_THRESHOLD = 100.0 

MONITORED_ADDRESSES = {
    "JUP6Lkbuej7is598XDn7Bms6p71J9r7onq9s48SUnAn": "Jupiter",
    "2S6mPGm8kHtbhiqa44e8yYAU5nYMLoqxUQa9T2w3UGrN": "Zerebro",
    "Dfhv69v86X874UicFayS9uPAGf9hXisP59N6pX9vpump": "Pippin"
}

def init_csv():
    """Инициализира CSV файла със заглавен ред, ако не съществува."""
    if not os.path.exists(ARCHIVE_PATH):
        try:
            with open(ARCHIVE_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'label', 'amount_sol', 'description', 'signature'])
            print(f"[SYSTEM] CSV Log initialized at {ARCHIVE_PATH}")
        except Exception as e:
            print(f"[CRITICAL] CSV Initialization failed: {e}")

def extract_sol_amount(description):
    """Извлича количеството SOL от текстовото описание на Helius."""
    if not description: return 0.0
    try:
        match = re.search(r'(\d+(\.\d+)?)\s*SOL', description)
        return float(match.group(1)) if match else 0.0
    except: return 0.0

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data: return jsonify({"status": "ignored"}), 200

    if not isinstance(data, list): data = [data]

    try:
        with open(ARCHIVE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            for txn in data:
                description = txn.get('description', '')
                amount = extract_sol_amount(description)
                
                # ЛОГИКА ЗА ФИЛТРИРАНЕ: AI Агенти или големи китове (100+ SOL)
                is_ai_agent = any(addr in str(txn) for addr in ["2S6mPGm8", "Dfhv69v8"])
                is_whale = amount >= MIN_SOL_THRESHOLD
                
                if is_ai_agent or is_whale:
                    label = "AI_AGENT" if is_ai_agent else "WHALE_SWAP"
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        label,
                        amount,
                        description[:200], # Ограничаваме дължината
                        txn.get('signature', 'N/A')
                    ])
                    # Принтираме само важните събития в терминала
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {label}: {amount} SOL")
    except Exception as e:
        print(f"[ERROR] Logging failed: {e}")

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    init_csv()
    # Публичен хост за приемане на данни от Helius
    app.run(host='0.0.0.0', port=5000)