import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Използваме стабилния Flash модел от твоя списък
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    # Ограничаваме заявката до минимум
    response = model.generate_content("Status check.")
    # Печатаме само чистия текст
    if response.text:
        print(f"System: {response.text.strip()}")
except Exception as e:
    print("System status: Busy. Retrying in 60 seconds.")