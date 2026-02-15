import os
import csv
import json
import datetime
import traceback
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# ПЪТ КЪМ ЛОГА
ARCHIVE_PATH = "/root/SolanaProject/ARCHIVE/intelligence_log.csv"
MIN_SOL_THRESHOLD = 1.0

# СТРАТЕГИЧЕСКИ АДРЕСИ
MONITORED_ADDRESSES = {
    "2S6mPGm8kHtbhiqa44e8yYAU5nYMLoqxUQa9T2w3UGrN": "Zerebro",
    "Dfhv69v86X874UicFayS9uPAGf9hXisP59N6pX9vpump": "Pippin",
    "HeLp6Nu644nNTV2STWvYJqasxMsvvR1KHpuv288Spump": "ai16z"
}

def init_csv():
    if not os.path.exists(ARCHIVE_PATH):
        with open(ARCHIVE_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'label', 'amount_sol', 'description', 'signature'])

def extract_sol_value(txn):
    total_lamports = 0
    native_transfers = txn.get('nativeTransfers', [])
    if native_transfers:
        for transfer in native_transfers:
            total_lamports += transfer.get('amount', 0)
    return total_lamports / 1_000_000_000

# СИГУРЕН ЕНДПОИНТ - Ботовете не го знаят
@app.route('/webhook_mila_secret_v1', methods=['POST'])
def webhook():
    data = request.json
    if not data or not isinstance(data, list):
        return jsonify({"status": "ignored"}), 200

    try:
        with open(ARCHIVE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for txn in data:
                amount = extract_sol_value(txn)
                signature = txn.get('signature', 'N/A')
                txn_str = json.dumps(txn)
                
                label = "GENERAL"
                is_monitored = False
                for address, name in MONITORED_ADDRESSES.items():
                    if address in txn_str:
                        is_monitored = True
                        label = f"AI_AGENT_{name}"
                        break

                if is_monitored or amount >= 100.0:
                    writer.writerow([datetime.datetime.now().isoformat(), label, f"{amount:.4f}", txn.get('description', '')[:200], signature])
                    print(f"!!! [MATCH] {label} | {amount:.2f} SOL !!!")
                    
    except Exception as e:
        print(f"[ERROR] {e}")

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    init_csv()
    app.run(host='0.0.0.0', port=5000)