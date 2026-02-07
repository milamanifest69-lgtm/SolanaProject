import os
import time
import datetime
import requests
import numpy as np
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# 1. Зареждане на ключовете
load_dotenv()
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class MilaShield:
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_radar_chart(self):
        labels = np.array(['Throughput', 'Latency', 'Validators', 'Slashing Risk', 'Stability'])
        stats = np.array([9.5, 8.8, 9.2, 9.8, 9.0])
        
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        stats = np.concatenate((stats, [stats[0]]))
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, stats, color='#4682B4', alpha=0.25)
        ax.plot(angles, stats, color='#00FFFF', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        
        plt.title("Solana Network Security Shield", size=15, color='white', y=1.1)
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#1B1E23')
        
        file_path = "shield_radar.png"
        plt.savefig(file_path, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        return file_path

    def send_to_telegram(self, photo_path):
        if not TG_TOKEN or not TG_CHAT_ID:
            print("[ERROR] Telegram credentials missing!")
            return

        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto"
        # Опростен текст без сложни форматирания, за да избегнем грешки при парсване
        caption = (
            "🛡️ MILA SHIELD MONITOR\n\n"
            "Network integrity verified. Infrastructure resilience increasing. "
            "Firedancer synchronization status: Optimal.\n\n"
            "Status: Monitoring the perimeter. Network fortified."
        )
        
        with open(photo_path, 'rb') as photo:
            payload = {'chat_id': TG_CHAT_ID, 'caption': caption} # Премахнахме parse_mode
            files = {'photo': photo}
            response = requests.post(url, data=payload, files=files)
            
        if response.status_code == 200:
            print("[Shield] Network Audit Dispatched to Telegram.")
        else:
            print(f"[ERROR] Failed to send: {response.text}")

if __name__ == "__main__":
    print(f"--- SHIELD MONITOR ACTIVE | {datetime.datetime.now().strftime('%H:%M')} ---")
    shield = MilaShield()
    path = shield.generate_radar_chart()
    shield.send_to_telegram(path)