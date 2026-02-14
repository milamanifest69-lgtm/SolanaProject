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
MIN_SOL_THRESHOLD = 1.0  # Праг за засичане

MONITORED_ADDRESSES = {
    "JUP6Lkbuej7is598XDn7Bms6p71J9r7onq9s48SUnAn": "Jupiter",
    "675kPX9MHTjS2zt1q61utZskL8HPY944S5utE7NmoZ3e": "Raydium Authority",
    "2S6mPGm8kHtbhiqa44e8yYAU5nYMLoqxUQa9T2w3UGrN": "Zerebro",
    "Dfhv69v86X874UicFayS9uPAGf9hXisP59N6pX9vpump": "Pippin"
}

def init_csv():
    if not os.path.exists(ARCHIVE_PATH):
        with open(ARCHIVE_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'label', 'amount_sol', 'description', 'signature'])

def extract_sol_value(txn):
    """Извлича реалната стойност на SOL от nativeTransfers (lamports to SOL)."""
    total_lamports = 0
    native_transfers = txn.get('nativeTransfers', [])
    if native_transfers:
        for transfer in native_transfers:
            total_lamports += transfer.get('amount', 0)
    return total_lamports / 1_000_000_000

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data or not isinstance(data, list):
        return jsonify({"status": "ignored"}), 200

    try:
        with open(ARCHIVE_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for txn in data:
                # 1. Точно извличане на сумата
                amount = extract_sol_value(txn)
                description = txn.get('description', 'No description')
                signature = txn.get('signature', 'N/A')
                
                # 2. Дълбоко търсене на адреси в цялата транзакция
                txn_str = json.dumps(txn)
                label = "GENERAL"
                is_monitored = False

                for address, name in MONITORED_ADDRESSES.items():
                    if address in txn_str:
                        is_monitored = True
                        label = "CAPITAL_FLOW" if name in ["Jupiter", "Raydium Authority"] else "AI_AGENT"
                        break

                # 3. Филтриране по логика
                if is_monitored and (amount >= MIN_SOL_THRESHOLD or label == "AI_AGENT"):
                    writer.writerow([
                        datetime.datetime.now().isoformat(),
                        label,
                        f"{amount:.4f}",
                        description[:200],
                        signature
                    ])
                    print(f"!!! [MATCH] {label} | {amount:.2f} SOL | Sig: {signature[:8]} !!!")
                else:
                    # Лог за диагностика
                    print(f"[SCAN] Ignored: {amount:.4f} SOL | Target Found: {is_monitored}")

    except Exception as e:
        print(f"[ERROR] Logic failure: {e}")
        traceback.print_exc()

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    init_csv()
    app.run(host='0.0.0.0', port=5000)