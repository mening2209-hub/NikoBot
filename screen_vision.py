import os
import json
import pyautogui
import ollama
from datetime import datetime

MEMORY_FILE = "screen_memories.json"

def save_memory(text):
    memories = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memories = json.load(f)
        except Exception:
            memories = []
    
    timestamp = datetime.now().strftime("%Y-%m-%d [%H:%M:%S]")
    memories.append({"time": timestamp, "content": text})
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, ensure_ascii=False, indent=4)

def get_memories_summary():
    if not os.path.exists(MEMORY_FILE):
        return "Hozircha eslab qolingan ekran ma'lumotlari yo'q."
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memories = json.load(f)
        if not memories:
            return "Hozircha eslab qolingan ekran ma'lumotlari yo'q."
        
        result = "Men eslab qolgan oxirgi ekran ma'lumotlari:\n"
        for m in memories[-3:]:  
            result += f"\n• [{m['time']}]:\n{m['content']}\n"
        return result
    except Exception as e:
        return f"Xotirani o'qishda xatolik: {e}"

def analyze_screen(prompt_text):
    screenshot_path = os.path.abspath("screen_temp.png")
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        response = ollama.chat(
            model='llava', 
            messages=[{
                'role': 'user',
                'content': prompt_text if prompt_text else "Ekrandagi ma'lumotlarni tushuntirib ber.",
                'images': [screenshot_path]
            }]
        )
        return True, response['message']['content']
    except Exception as e:
        return False, f"Ekranni o'qishda xatolik: {e}. 'ollama run llava' modelini o'rnatganingizga ishonch hosil qiling."
    finally:
        # Faylni xavfsiz o'chirish
        if os.path.exists(screenshot_path):
            try:
                os.remove(screenshot_path)
            except:
                pass

def capture_and_remember():
    screenshot_path = os.path.abspath("screen_temp.png")
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        response = ollama.chat(
            model='llava', 
            messages=[{
                'role': 'user',
                'content': "Bu ekranda nima borligini, muhim matnlar yoki elementlarni qisqacha va aniq tasvirlab ber.",
                'images': [screenshot_path]
            }]
        )
        content = response['message']['content']
        save_memory(content)
        return True, f"Ekrandagi ma'lumotlar eslab qolindi:\n{content}"
    except Exception as e:
        return False, f"Ekranni eslab qolishda xatolik: {e}"
    finally:
        if os.path.exists(screenshot_path):
            try:
                os.remove(screenshot_path)
            except:
                pass