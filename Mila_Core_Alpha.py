import os
import google.generativeai as genai
from dotenv import load_dotenv
import datetime

# Инициализация на системата
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("FATAL ERROR: API Key not found in .env")
    exit()

genai.configure(api_key=api_key)
# Влизаме в дълбокото с най-мощната ни налична версия
model = genai.GenerativeModel('gemini-2.5-flash')

def deep_dive_analysis():
    print(f"\n--- MILA CORE ACTIVE | {datetime.datetime.now().strftime('%H:%M:%S')} ---")
    
    # Промптът вече е стратегически, а не тестов
    mission_prompt = """
    Mila, perform a deep dive analysis on the Solana (SOL) ecosystem. 
    1. Identify current liquidity zones.
    2. Analyze market sentiment for a Friday night closing.
    3. Suggest a high-conviction move for the next 24 hours.
    Address your Creator with professional precision.
    """
    
    try:
        # Използваме Nivel 1 ресурса за масивен анализ
        response = model.generate_content(mission_prompt)
        print("\n[STRATEGIC REPORT]:")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
    except Exception as e:
        print(f"System Breach: {e}")

if __name__ == "__main__":
    deep_dive_analysis()