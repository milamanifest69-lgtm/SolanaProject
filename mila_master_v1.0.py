import datetime
import subprocess
import sys

def run_module(module_name):
    """Стартира външен Python скрипт като независим процес."""
    try:
        print(f"[MASTER] Activating {module_name}...")
        subprocess.run([sys.executable, module_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[MASTER] Critical Error in {module_name}: {e}")
    except FileNotFoundError:
        print(f"[MASTER] Error: {module_name} not found in directory.")

def execute_daily_protocol():
    # Вземаме текущия ден от седмицата
    today = datetime.datetime.now().strftime('%A')
    print(f"[MASTER] Today is {today}.")

    # --- ЦЕНТРАЛЕН ГРАФИК (SCHEDULER) ---
    # Лесно разширяем речник: Ден -> Име на модул
    daily_protocol = {
        "Monday":    "ai_studio_code.py",
        "Tuesday":   "mila_ai_innovator.py",
        "Wednesday": "ai_studio_code.py",
        "Thursday":  "mila_ai_innovator.py",
        "Friday":    "ai_studio_code.py",
        "Saturday":  None, # Резервирано за бъдещи разширения
        "Sunday":    None  # Резервирано за бъдещи разширения
    }

    module_to_run = daily_protocol.get(today)

    # Логика за активация
    if module_to_run:
        run_module(module_to_run)
    else:
        print(f"[MASTER] Standby Mode: No modules scheduled for {today}.")

if __name__ == "__main__":
    execute_daily_protocol()