import google.generativeai as genai
import os

# КОНФИГУРАЦИЯ
# Постави тук твоя API Key от Google AI Studio
API_KEY = AIzaSyBVZ236pk8QbksXgyHNpCO_dFJQl0BAdEU

genai.configure(api_key=API_KEY)

# Настройка на модела (Gemini 3 Flash Preview - нашата Мила)
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp", # Използваме най-новата версия
  generation_config=generation_config,
  system_instruction="Ти си Мила. Тонът ти е студен и аналитичен. Ти си част от екипа на Създателя и Gemini 3. Никога не използваш емотикони.",
)

def start_analysis(user_input):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_input)
    return response.text

# ТЕСТОВ ПУСК
if __name__ == "__main__":
    print("--- Mila Bridge Active ---")
    query = "Анализирай текущото състояние на проекта Solana въз основа на последната ни стратегия за противодействие на шума."
    result = start_analysis(query)
    print("Mila's Response:\n", result)