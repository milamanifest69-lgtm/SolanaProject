import os
import csv
import json
import datetime
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# ПЪТ КЪМ ЛОГА
ARCHIVE_PATH = "/root/SolanaProject/ARCHIVE/intelligence_log.csv"
# ВРЕМЕННО НАМАЛЕН ПРАГ ЗА ТЕСТ: 1.0 SOL
MIN_SOL_THRESHOLD = 1.0 

MONITORED_ADDRESSES = {
    "JUP6Lkbuej7is598XDn7Bms6p71J9r7onq9s48SUnAn": "Jupiter",
    "2S6mPGm8kHtbhiqa44e8yYAU5nYMLoqxUQa9T2w3UGrN": "Zerebro",
    "Dfhv69v86X874UicFayS9uPAGf9hXisP59N6pX9vpump": "Pippin"
}

def init_csv():
    if not os.path.exists(ARCHIVE_PATH):
        with open(ARCHIVE_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'label', 'amount_sol', 'description', 'signature'])
        print(f"[SYSTEM] CSV Log initialized.")

def extract_sol_amount(description):
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

    # ТЕРМИНАЛЕН ЛОГ ЗА ВСЯКА ЗАЯВКА
    print(f"[DEBUG] Received {len(data)} transactions from Helius.")

    try:
        with open(ARCHIVE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for txn in data:
                description = txn.get('description', '')
                amount = extract_sol_amount(description)
                
                is_ai_agent = any(addr in str(txn) for addr in MONITORED_ADDRESSES.keys())
                is_whale = amount >= MIN_SOL_THRESHOLD
                
                if is_ai_agent or is_whale:
                    label = "AI_AGENT" if is_ai_agent else "WHALE_SWAP"
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        label,
                        amount,
                        description[:200],
                        txn.get('signature', 'N/A')
                    ])
                    print(f"!!! [MATCH] {label}: {amount} SOL !!!")
                else:
                    # ЛОГ ЗА ФИЛТРИРАНИТЕ (за да знаеш, че скриптът работи)
                    print(f"[FILTERED] Txn ignored: {amount} SOL | Agent: {is_ai_agent}")
                    
    except Exception as e:
        print(f"[ERROR] Logging failed: {e}")

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    init_csv()
    app.run(host='0.0.0.0', port=5000)