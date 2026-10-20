import os
import subprocess
import webbrowser

def open_app_or_web(user_text):
    raw = user_text.lower().strip()
    if "telegram" in raw and not any(w in raw for w in ["dan", "ga", "top", "yoz"]):
        try:
            tg_path = os.path.expanduser(r"~\AppData\Roaming\Telegram Desktop\Telegram.exe")
            if os.path.exists(tg_path):
                subprocess.Popen([tg_path])
            else:
                os.system("start telegram")
            return True, "Telegram ochildi."
        except Exception as e:
            return False, f"Telegramni ochishda xatolik: {e}"
    
    if "youtube" in raw:
        webbrowser.open("https://youtube.com")
        return True, "YouTube ochildi."
        
    if "chrome" in raw or "google" in raw:
        webbrowser.open("https://google.com")
        return True, "Google ochildi."
        
    return False, ""

def open_last_app():
    return False, "Oxirgi dastur mavjud emas."
