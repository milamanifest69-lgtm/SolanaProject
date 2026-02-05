import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Използваме Pro модела за по-висока стабилност при свободен трафик
model = genai.GenerativeModel('gemini-1.0-pro')

def try_connect():
    for attempt in range(3):
        try:
            print(f"Опит за връзка {attempt + 1}...")
            response = model.generate_content("Mila, confirm connection.")
            if response.text:
                print(f"System: {response.text.strip()}")
                return True
        except Exception:
            print("System status: Busy. Waiting...")
            time.sleep(5) # Кратко изчакване преди нов опит
    return False

try_connect()