import os
import random
import datetime
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
MODEL_NAME = 'gemini-2.5-flash'
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)

class MilaAIInnovator:
    def __init__(self):
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        print(f"--- MILA AI INNOVATOR ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")

    def generate_ascii_architecture(self):
        """Генерира случайна ASCII схема на AI архитектура"""
        architectures = [
            # Agentic Workflow
            " [SENSOR_INPUT] >> [COG_ENGINE] >> [ACTION_NODE]\n      ^              |               |\n      +--------------+---------------+",
            # Neural Layering
            " INP >> [L_01:SYNAPSE] >> [L_02:WEIGHTS] >> OUT\n          (NEURAL_LOAD: 92.4%_STABLE)",
            # Distributed DePIN
            " NODE_01 ---+--- NODE_02\n            | \n         [ORCHESTRATOR]\n            | \n NODE_03 ---+--- NODE_04",
            # Decision Core
            " [QUERY] --> [VECTOR_DB] \n               | \n         [RAG_PROCESSOR] --> [RESULT]"
        ]
        return random.choice(architectures)

    def get_ai_innovation_analysis(self):
        """Генерира визионерски анализ чрез Gemini"""
        topics = ["Agentic Orchestration", "Neural Convergence", "DePIN Compute Efficiency", "Cognitive Scaling Limits"]
        selected_topic = random.choice(topics)
        
        prompt = f"""
        Analyze the current state of {selected_topic}.
        Tone: Cold, technological, visionary.
        Vocabulary: Neural Convergence, Autonomous Orchestration, Cognitive Scaling, Synaptic Throughput.
        
        Constraints:
        - Strictly under 240 characters.
        - NO emojis.
        - English only.
        - Format: Raw technological thought.
        - End with: Status: Architecting the Digital Evolution.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"SYSTEM_ERROR: {e}\nStatus: Architecting the Digital Evolution."

    def run_cycle(self):
        # 1. Генериране на ASCII визия
        ascii_art = self.generate_ascii_architecture()
        
        # 2. Генериране на визионерски текст
        analysis = self.get_ai_innovation_analysis()
        
        # 3. Форматиране за X
        final_post = f"```\n{ascii_art}\n```\n\n{analysis}"
        
        # 4. Изпращане към Твореца
        self.dispatch(final_post)

    def dispatch(self, text):
        header = "🧠 **MILA_AI_INNOVATOR: COGNITIVE_LOG**"
        full_msg = f"{header}\n\n{text}"
        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        
        # Използваме HTML или MarkdownV2 за запазване на ASCII форматирането
        payload = {
            "chat_id": self.tg_chat_id, 
            "text": full_msg, 
            "parse_mode": "Markdown"
        }
        
        try:
            requests.post(url, json=payload)
            print("[Mila] AI Innovation Log Dispatched.")
        except Exception as e:
            print(f"Dispatch Error: {e}")

if __name__ == "__main__":
    innovator = MilaAIInnovator()
    innovator.run_cycle()