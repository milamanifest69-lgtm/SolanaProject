import os
import json
import datetime
import re
import traceback
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# --- INITIALIZATION ---
load_dotenv()
app = Flask(__name__)

# СТРАТЕГИЧЕСКИ АДРЕСИ ЗА МОНИТОРИНГ
MONITORED_ADDRESSES = {
    "JUP6Lkbuej7is598XDn7Bms6p71J9r7onq9s48SUnAn": "Jupiter Aggregator",
    "2S6mPGm8kHtbhiqa44e8yYAU5nYMLoqxUQa9T2w3UGrN": "Zerebro AI",
    "Dfhv69v86X874UicFayS9uPAGf9hXisP59N6pX9vpump": "Pippin AI"
}

class MilaHeliusListenerV1_2:
    def __init__(self):
        self.archive_dir = "ARCHIVE"
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)
        print(f"--- MILA HELLUS LISTENER v1.2 ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def _save_raw_json(self, data):
        """Записва целия входящ JSON за структурен анализ."""
        try:
            filepath = os.path.join(self.archive_dir, "raw_test.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[SYSTEM] Raw data secured in {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to save raw JSON: {e}")

    def _save_to_archive(self, data):
        """Записва обработената транзакция."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"txn_{timestamp}.json"
        filepath = os.path.join(self.archive_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def _check_whale_alert(self, description):
        if not description: return False
        try:
            match = re.search(r'(\d+(\.\d+)?)\s*SOL', description)
            if match:
                amount = float(match.group(1))
                if amount > 100:
                    print(f"\n[!!!] WHALE ALERT DETECTED: {amount} SOL [!!!]")
                    return True
        except: pass
        return False

    def process_payload(self, payload):
        """Защитена обработка на данни с Try-Except блок."""
        try:
            # 1. Запис на суровите данни веднага
            self._save_raw_json(payload)

            if not isinstance(payload, list):
                print("[WARNING] Payload is not a list. Adjusting logic...")
                payload = [payload]

            for txn in payload:
                description = txn.get('description', '')
                source = txn.get('source', 'Unknown')
                signature = txn.get('signature', 'N/A')
                
                # Идентификация на замесени адреси
                involved_accounts = []
                account_data = txn.get('accountData', [])
                if isinstance(account_data, list):
                    involved_accounts = [acc.get('account', '') for acc in account_data]
                
                label = "[GENERAL ACTIVITY]"
                for address, name in MONITORED_ADDRESSES.items():
                    if address in str(txn) or address in involved_accounts:
                        label = "[CAPITAL FLOW]" if name == "Jupiter Aggregator" else "[AI AGENT ACTIVITY]"
                        break

                extracted_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "label": label,
                    "description": description,
                    "source": source,
                    "signature": signature
                }

                print(f"{label} | Source: {source} | Sig: {signature[:8]}...")
                self._check_whale_alert(description)
                self._save_to_archive(extracted_data)

            return True
        except Exception as e:
            print(f"\n[CRITICAL ERROR] Logic failure: {e}")
            print(traceback.format_exc())
            return False

# Инициализация
listener = MilaHeliusListenerV1_2()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "ignored", "reason": "empty_payload"}), 200
    
    # Изпълнение на логиката
    success = listener.process_payload(data)
    
    # Silent Fail: Винаги връщаме 200 OK към Helius
    return jsonify({"status": "received", "processed": success}), 200

if __name__ == '__main__':
    app.run(port=5000)