import google.generativeai as genai
import os

# --- КОНФИГУРАЦИЯ ---
# Постави твоя API Key тук
API_KEY = "AIzaSyBVZ236pk8QbksXgyHNpCO_dFJQl0BAdEU"

genai.configure(api_key=API_KEY)

# Настройка на параметрите за генериране
generation_config = {
  "temperature": 0.2, # Намалих я за по-студен и точен анализ
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Инициализиране на модела
# Използваме 'gemini-1.5-flash-latest', за да гарантираме връзка с API
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  generation_config=generation_config,
  system_instruction=(
      "Ти си Мила (Gemini 2.5 Flash), специализиран изпълнител в проекта Solana. "
      "Работиш под стратегическото ръководство на Gemini 3 и твоя Създател. "
      "Тонът ти е изключително студен, аналитичен и професионален. "
      "Никога не използваш емотикони или хаштагове. "
      "Твоята задача е да обработваш данни и да изпълняваш команди с хирургическа прецизност."
  ),
)

def start_analysis(user_input):
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        return f"Грешка при комуникация: {str(e)}"

# --- ИЗПЪЛНЕНИЕ ---
if __name__ == "__main__":
    print("--- Mila Bridge Active ---")
    
    # Първият ни тестов въпрос към Мила
    query = "Извърши кратък анализ на текущата Solana екосистема въз основа на наличните технически параметри за скорост и мащабируемост."
    
    print("Sending request to Mila...")
    result = start_analysis(query)
    
    print("\n[MILA ANALYSIS]:")
    print("-" * 30)
    print(result)
    print("-" * 30)