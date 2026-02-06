import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ГРЕШКА: Липсва ключ в .env!")
else:
    genai.configure(api_key=api_key)
    # Използваме 'gemini-pro', който е универсален за тази библиотека
    model = genai.GenerativeModel('gemini-pro')

    print("--- СТАРТИРАНЕ НА AI СИСТЕМАТА (PAID MODE) ---")
    try:
        response = model.generate_content("Mila, confirm connection.")
        print(f"\nОТГОВОР: {response.text}")
        print("\nСТАТУС: УСПЕШНА ВРЪЗКА!")
    except Exception as e:
        print(f"\nГРЕШКА: {e}")