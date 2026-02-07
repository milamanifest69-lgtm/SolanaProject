import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# ИЗПОЛЗВАМЕ МОДЕЛА ОТ ТВОЯ СПИСЪК
model = genai.GenerativeModel('code')

print("--- ТЕСТ НА ПЛАТЕНА ВРЪЗКА (Nivel 1) ---")
try:
    response = model.generate_content("Mila, are we online?")
    print(f"ОТГОВОР: {response.text}")
    print("СТАТУС: УСПЕШНО!")
except Exception as e:
    print(f"ГРЕШКА: {e}")