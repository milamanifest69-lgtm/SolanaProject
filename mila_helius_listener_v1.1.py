import os
import json
import datetime
import re
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

class MilaHeliusListenerV1_1:
    def __init__(self):
        self.archive_dir = "ARCHIVE"
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)
        print(f"--- MILA HELLUS LISTENER v1.1 ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def _save_to_archive(self, data):
        """Записва транзакцията в JSON формат в папка ARCHIVE."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"txn_{timestamp}.json"
        filepath = os.path.join(self.archive_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def _check_whale_alert(self, description):
        """Идентифицира транзакции над 100 SOL в описанието."""
        try:
            # Търсене на цифри последвани от SOL
            match = re.search(r'(\d+(\.\d+)?)\s*SOL', description)
            if match:
                amount = float(match.group(1))
                if amount > 100:
                    print(f"\n[!!!] WHALE ALERT DETECTED: {amount} SOL [!!!]")
                    return True
        except Exception:
            pass
        return False

    def process_payload(self, payload):
        """Обработва входящия поток от Helius."""
        for txn in payload:
            description = txn.get('description', '')
            source = txn.get('source', 'Unknown')
            signature = txn.get('signature', 'N/A')
            
            # Проверка за участие на мониторираните адреси
            involved_accounts = [acc.get('account', '') for acc in txn.get('accountData', [])]
            
            label = "[GENERAL ACTIVITY]"
            is_monitored = False

            for address, name in MONITORED_ADDRESSES.items():
                if address in str(txn) or address in involved_accounts:
                    is_monitored = True
                    if name == "Jupiter Aggregator":
                        label = "[CAPITAL FLOW]"
                    else:
                        label = "[AI AGENT ACTIVITY]"
                    break

            # Извличане на метаданни
            extracted_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "label": label,
                "description": description,
                "source": source,
                "signature": signature,
                "raw_data": txn
            }

            # Принтиране в терминала
            print(f"{label} Source: {source} | Signature: {signature[:10]}...")
            print(f"Details: {description}")

            # Проверка за китове
            self._check_whale_alert(description)

            # Архивиране
            self._save_to_archive(extracted_data)

# Инициализация на ядрото
listener = MilaHeliusListenerV1_1()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error"}), 400
    
    listener.process_payload(data)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Стартиране на сървъра
    app.run(port=5000)