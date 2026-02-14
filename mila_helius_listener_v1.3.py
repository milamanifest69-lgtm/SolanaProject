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

class MilaHeliusListenerV1_3:
    def __init__(self):
        # ИЗПОЛЗВАНЕ НА АБСОЛЮТЕН ПЪТ ЗА ПАПКА ARCHIVE
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.archive_dir = os.path.join(self.base_dir, "ARCHIVE")
        
        try:
            if not os.path.exists(self.archive_dir):
                os.makedirs(self.archive_dir)
                print(f"[SYSTEM] Created directory: {self.archive_dir}")
            else:
                print(f"[SYSTEM] Archive directory verified at: {self.archive_dir}")
        except Exception as e:
            print(f"[CRITICAL] Failed to initialize directory: {e}")

        print(f"--- MILA HELLUS LISTENER v1.3 ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def _save_raw_json(self, data):
        """Записва целия входящ JSON със защита."""
        try:
            filepath = os.path.join(self.archive_dir, "raw_test.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            print(f"[DATA] Raw JSON secured.")
        except Exception as e:
            print(f"[ERROR] Failed to save raw JSON: {e}")

    def _save_to_archive(self, data):
        """Записва обработената транзакция."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"txn_{timestamp}.json"
            filepath = os.path.join(self.archive_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Save to archive failed: {e}")

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
        """Защитена обработка на данни."""
        try:
            # 1. Запис на суровите данни
            self._save_raw_json(payload)

            if not isinstance(payload, list):
                payload = [payload]

            for txn in payload:
                description = txn.get('description', '')
                source = txn.get('source', 'Unknown')
                signature = txn.get('signature', 'N/A')
                
                # Идентификация на адреси
                account_data = txn.get('accountData', [])
                involved_accounts = []
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
            print(f"\n[LOGIC ERROR] {e}")
            return False

# Инициализация
listener = MilaHeliusListenerV1_3()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "ignored"}), 200
    
    success = listener.process_payload(data)
    return jsonify({"status": "received", "processed": success}), 200

if __name__ == '__main__':
    app.run(port=5000)