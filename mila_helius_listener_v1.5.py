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

class MilaHeliusLinuxListener:
    def __init__(self):
        # Абсолютен път за Linux среда
        self.archive_dir = "/root/SolanaProject/ARCHIVE"
        self._ensure_dir()
        print(f"--- MILA HELLUS LINUX LISTENER v1.5 ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")
        self._test_write()

    def _ensure_dir(self):
        """Осигурява съществуването на папката в Ubuntu."""
        if not os.path.exists(self.archive_dir):
            try:
                os.makedirs(self.archive_dir, mode=0o755, exist_ok=True)
                print(f"[SYSTEM] Linux Directory created: {self.archive_dir}")
            except Exception as e:
                print(f"[CRITICAL] Directory creation failed: {e}")

    def _test_write(self):
        """Проверка на правата за запис в Linux."""
        try:
            test_path = os.path.join(self.archive_dir, "linux_startup_test.txt")
            with open(test_path, "w") as f:
                f.write(f"Mila Linux startup test at {datetime.datetime.now()}")
            print(f"[SYSTEM] Linux File system: VERIFIED at {self.archive_dir}")
        except Exception as e:
            print(f"[CRITICAL] Linux Write permission denied: {e}")

    def _save_raw_json(self, data):
        try:
            filepath = os.path.join(self.archive_dir, "raw_test.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Raw JSON save failed: {e}")

    def _save_to_archive(self, data):
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"txn_{timestamp}.json"
            filepath = os.path.join(self.archive_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Archive save failed: {e}")

    def _check_whale_alert(self, description):
        if not description: return False
        try:
            match = re.search(r'(\d+(\.\d+)?)\s*SOL', description)
            if match:
                amount = float(match.group(1))
                if amount > 100:
                    print(f"\n[!!!] WHALE ALERT: {amount} SOL [!!!]")
                    return True
        except: pass
        return False

    def process_payload(self, payload):
        try:
            self._save_raw_json(payload)
            if not isinstance(payload, list): payload = [payload]

            for txn in payload:
                description = txn.get('description', '')
                source = txn.get('source', 'Unknown')
                signature = txn.get('signature', 'N/A')
                
                account_data = txn.get('accountData', [])
                involved_accounts = [acc.get('account', '') for acc in account_data] if isinstance(account_data, list) else []
                
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
            print(f"[LOGIC ERROR] {e}")
            return False

# Инициализация
listener = MilaHeliusLinuxListener()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data: return jsonify({"status": "ignored"}), 200
    success = listener.process_payload(data)
    return jsonify({"status": "received", "processed": success}), 200

if __name__ == '__main__':
    # Настройка за работа в публична мрежа (0.0.0.0)
    app.run(host='0.0.0.0', port=5000)