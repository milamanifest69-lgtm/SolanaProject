import os
import google.generativeai as genai
from dotenv import load_dotenv

# Зареждаме новия платен ключ
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Използваме модела директно без цикли за чакане
model = genai.GenerativeModel('gemini-pro')

print("--- Тестване на ПЛАТЕНАТА връзка (Nivel 1) ---")
try:
    response = model.generate_content("Mila, are we online with the paid key?")
    print("Отговор от Mila:")
    print(response.text)
    print("------------------------------------------")
    print("СТАТУС: Връзката е УСПЕШНА. Готови сме за Cloud!")
except Exception as e:
    print(f"Грешка: {e}")