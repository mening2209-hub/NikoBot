import datetime
import os
import requests
import speech_recognition as sr
from ai_chat import ask_ai

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# OMBDORDAN NARX VA QOLDIQNI ODAMIY TARZda QIDIRISH
def check_product_in_inventory(query):
    file_txt = "ombor.txt"
    if not os.path.exists(file_txt):
        return None
    
    query = query.lower().strip()
    stop_words = ["narxi", "qancha", "bor", "qoldimi", "necha", "nichi", "niki", "degan", "atma"]
    clean_q = query
    for w in stop_words:
        clean_q = clean_q.replace(w, "")
    clean_q = clean_q.strip()
    
    if len(clean_q) < 2:
        return None
    
    try:
        with open(file_txt, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4:
                    turi, name, qty, price = parts[0], parts[1], parts[2], parts[3]
                    if clean_q in name.lower() or name.lower() in clean_q:
                        return f"Ha, {name} bor. Narxi {price} so'm, hozirda omborda {qty} ta mavjud. Nechta olmoqchisiz?"
    except Exception:
        pass
    return None

# MIJOZLAR BILAN JONLI, ODAMDEK MULOQOT
def handle_business_chat(user_text):
    system_prompt = (
        "Siz Telegram'da mijozlar bilan yozishadigan jonli, samimiy va tajribali do'kon xodimisiz. "
        "Hech qachon robotdek yoki o'ta rasmiy gapirmang. Xuddi haqiqiy inson kabi oddiy, iliq va qisqa javob bering. "
        "Agar mahsulot yo'q bo'lsa, 'hozirda yo'q ekan, lekin tez orada kelib qoladi' deb oddiygina tushuntiring."
    )
    full_prompt = f"{system_prompt}\nMijoz yozdi: {user_text}"
    return ask_ai(full_prompt)

def handle_in_app_actions(user_text):
    try:
        raw = user_text.lower().strip()
        greetings = ["salom", "assalomu alaykum", "salomatsizmi", "privet", "hello"]
        if raw in greetings or any(raw == g for g in greetings):
            return True, "Assalomu alaykum! Qanday yordam bera olaman, qaysi mahsulot kerak edi?"

        # Ombordan qidiramiz
        inventory_result = check_product_in_inventory(raw)
        if inventory_result:
            return True, inventory_result

        # Ilovalarni ochish
        if any(word in raw for word in ["och", "ochish", "telegram", "excel", "word", "notepad", "chrome", "google", "youtube"]):
            try:
                from app_launcher import open_app_or_web
                app_executed, app_msg = open_app_or_web(user_text)
                if app_executed:
                    return True, app_msg
            except ImportError:
                pass

        # Qolgan barcha savollar uchun odamdek gaplashadigan chat
        business_reply = handle_business_chat(user_text)
        return True, business_reply

    except Exception as e:
        return False, f"Xatolik: {e}"

def listen_voice_command():
    try:
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            print("🎤 NIKO eshitmoqda, gapiring...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio, language="uz-UZ")
            return text
    except Exception as e:
        return f"Xatolik: {e}"
