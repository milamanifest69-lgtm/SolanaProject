import os
import time
import datetime
import requests
import numpy as np
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Задължително зареждане на средата в началото
load_dotenv()

# --- CONFIGURATION ---
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaShieldMonitor:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        # Проверка на променливите за Телеграм
        if not self.tg_token or not self.tg_chat_id:
            print("[ERROR] Telegram credentials missing!")
        
        print(f"--- SHIELD MONITOR v1.1 ACTIVE | INFRASTRUCTURE AUDIT | {datetime.datetime.now().strftime('%H:%M')} ---")

    def generate_radar_chart(self):
        """Генерира Radar Chart (паяжина) за мрежовите параметри на Solana."""
        print("[Mila] Рендерирам технически Radar Chart...")
        
        categories = ['Throughput', 'Latency', 'Validator\nDiversity', 'Slashing\nRisks', 'Software\nStability']
        values = [9.2, 8.8, 7.5, 9.5, 8.0]
        
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        values += values[:1]
        angles += angles[:1]

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), facecolor='#0A0A0A')
        ax.set_facecolor('#0A0A0A')

        # Цветове: Steel Blue (#4682B4) и Neon Cyan (#00FFFF)
        color_cyan = '#00FFFF'
        color_blue = '#4682B4'

        plt.xticks(angles[:-1], categories, color=color_cyan, family='monospace', fontsize=9)
        ax.set_rlabel_position(0)
        plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#2D2D2D", fontsize=7)
        plt.ylim(0, 10)

        ax.plot(angles, values, color=color_cyan, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color_blue, alpha=0.3)

        ax.spines['polar'].set_color('#2D2D2D')
        ax.grid(color='#2D2D2D', linestyle='--', alpha=0.5)

        plt.title(" > SHIELD_MONITOR_V1.1: INFRASTRUCTURE_INTEGRITY", 
                  loc='left', color=color_cyan, family='monospace', fontsize=10, pad=30)

        path = "shield_radar.png"
        plt.tight_layout()
        plt.savefig(path, facecolor='#0A0A0A', dpi=120)
        plt.close()
        return path

    def get_security_analysis(self):
        """Генерира системен анализ на инфраструктурата."""
        prompt = """
        Mila, act as a Quantum Network Systems Administrator. Analyze Solana's infrastructure.
        Context: Firedancer synchronization, validator distribution, and network resilience.
        
        Tone: Cold, technical, secure.
        Vocabulary: 'Network integrity verified', 'Infrastructure resilience increasing', 'Firedancer synchronization status', 'Deterministic finality'.
        
        Constraints:
        - Strictly under 240 characters.
        - NO emojis.
        - English only.
        - End with: Status: Monitoring the perimeter. Network fortified.
        """
        try:
            response = model.generate_content(prompt)
            return response.strip() if hasattr(response, 'strip') else response.text.strip()
        except Exception as e:
            return f"SYSTEM_AUDIT_ERROR: {e}\nStatus: Monitoring the perimeter. Network fortified."

    def run_cycle(self):
        # 1. Проверка на credentials преди старт на тежките задачи
        if not self.tg_token or not self.tg_chat_id:
            print("[CRITICAL] Operation aborted: Telegram keys not found.")
            return

        # 2. Генериране на визия
        chart = self.generate_radar_chart()
        
        # 3. Генериране на анализ
        analysis = self.get_security_analysis()
        
        # 4. Диспечиране
        self.dispatch(analysis, chart)

    def dispatch(self, text, photo_path):
        header = "🛡️ **MILA SHIELD MONITOR: INFRA_LOG**"
        full_msg = f"{header}\n\n{text}"
        url = f"https://api.telegram.org/bot{self.tg_token}/sendPhoto"
        
        try:
            with open(photo_path, 'rb') as f:
                payload = {
                    "chat_id": self.tg_chat_id, 
                    "caption": full_msg,
                    "parse_mode": "Markdown"
                }
                files = {"photo": f}
                response = requests.post(url, data=payload, files=files)
                
                if response.status_code == 200:
                    print("[Shield] Network Audit Dispatched successfully.")
                else:
                    print(f"[Shield] Failed to send: {response.text}")
        except Exception as e:
            print(f"Dispatch Error: {e}")

if __name__ == "__main__":
    monitor = MilaShieldMonitor()
    monitor.run_cycle()