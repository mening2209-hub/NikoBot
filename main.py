from datetime import datetime
import threading
import tkinter as tk
from ai_chat import ask_ai  # <-- ask_gemini o'rniga ask_ai qilindi
from app_control import handle_in_app_actions, listen_voice_command
from app_launcher import open_app_or_web, open_last_app
from screen_vision import analyze_screen, capture_and_remember, get_memories_summary
from system_controls import handle_system_command
from voice_output import speak_response  # Ovoz chiqarib o'qish funksiyasi


def get_time_stamp():
    return datetime.now().strftime("[%H:%M:%S]")


# ASOSIY BUYRUQLARNI QAYTA ISHLASH FUNKSIYASI
def process_command(event=None):
    user_text = entry_field.get().strip()
    if not user_text:
        return

    chat_log.insert(tk.END, f"{get_time_stamp()} SIZ: {user_text}\n", "user_tag")
    entry_field.delete(0, tk.END)

    raw = user_text.lower()
    raw_lower = raw

    # 1. ENG BIRINCHI NAVBATDA: Tizim va ichki amallar (Ombor, qoldiq, mahsulot va moliyaviy yozuvlar)
    financial_keywords = [
        "kirim", "chiqdi", "chiqim", "sotdi", "sotish", "olindi", "berdi", "xarid", 
        "qarzga", "xarajatga", "xarajat", "summasi", "so'm ber", "som ber", "kirdi:", 
        "chiqdi:", "tovar sotish", "hisobot", "oylik", "excelda", "statistika", 
        "sklad", "qoldiq", "miqdor", "qancha", "ombordagi", "ombor", "omordan", 
        "bor", "qolgan", "miqdorini", "maxsulot", "mahsulot", "hamma", "barchasi", "korsat", "ko'rsat", "ro'yxat", "royxat"
    ]

    has_number = any(char.isdigit() for char in raw_lower)
    has_financial_word = any(word in raw_lower for word in financial_keywords)

    if (has_financial_word or (has_number and len(raw_lower.split()) >= 2)) and not "errno" in raw_lower and not "failed" in raw_lower:
        in_app_executed, in_app_msg = handle_in_app_actions(user_text)
        if in_app_executed:
            finish_response(in_app_msg)
            return

    # 2. Dastur va saytlarni ochish
    launch_keywords = ["och", "ochish", "ach", "qidir", "saytga kir", "brauzerni och"]
    has_launch_word = any(word in raw_lower for word in launch_keywords)

    if has_launch_word:
        app_executed, app_msg = open_app_or_web(user_text)
        if app_executed:
            finish_response(app_msg)
            return

    # 3. Oxirgi ishlatilgan dasturni ochish
    if any(
        phrase in raw_lower
        for phrase in [
            "oxirgi dasturni och",
            "oldingi dasturni och",
            "oxirgi programmani och",
            "oxirgi ochilgan",
        ]
    ):
        success, msg = open_last_app()
        finish_response(msg)
        return

    # 4. Xotira va ekran buyruqlari
    if any(
        phrase in raw_lower
        for phrase in [
            "nimani eslab",
            "eslab qolgan",
            "xotirani ko'rsat",
            "nimalarni eslab",
            "eslab qolganding",
        ]
    ):
        summary = get_memories_summary()
        finish_response(summary)
        return

    if any(
        phrase in raw_lower
        for phrase in ["eslab qol", "esda saqla", "eslab qoling", "ekranni eslab"]
    ):
        chat_log.insert(
            tk.END,
            f"{get_time_stamp()} AI: Ekran tahlil qilinib, xotiraga saqlanmoqda...\n",
            "ai_tag",
        )
        chat_log.see(tk.END)

        def run_remember():
            success, result_msg = capture_and_remember()
            root.after(0, finish_response, result_msg)

        threading.Thread(target=run_remember, daemon=True).start()
        return

    if (
        any(
            word in raw_lower
            for word in [
                "ekran",
                "ekranda",
                "nima turibdi",
                "oqib",
                "o'qib",
            ]
        )
        and not "xatolik" in raw_lower
    ):
        chat_log.insert(
            tk.END, f"{get_time_stamp()} AI: Ekran tahlil qilinmoqda...\n", "ai_tag"
        )
        chat_log.see(tk.END)

        def run_vision():
            success, result_msg = analyze_screen(user_text)
            root.after(0, finish_response, result_msg)

        threading.Thread(target=run_vision, daemon=True).start()
        return

    # 5. QOLGAN BARCHA HOLATLAR -> LOCAL OLLAMA / AI CHAT
    chat_log.insert(tk.END, f"{get_time_stamp()} AI: O'ylayapman...\n", "ai_tag")
    chat_log.see(tk.END)

    def run_ai():
        # ask_gemini o'rniga ask_ai ishlatildi
        ai_response = ask_ai(user_text)
        root.after(0, lambda: update_ai_response(ai_response))

    threading.Thread(target=run_ai, daemon=True).start()


def update_ai_response(response_text):
    chat_log.delete("end-2l", "end-1c")
    chat_log.insert(tk.END, f"{get_time_stamp()} AI: {response_text}\n\n", "ai_tag")
    chat_log.see(tk.END)
    speak_response(response_text)


def finish_response(response):
    chat_log.insert(tk.END, f"{get_time_stamp()} AI: {response}\n\n", "ai_tag")
    chat_log.see(tk.END)
    speak_response(response)


def start_voice_recognition():
    def run_voice():
        text = listen_voice_command()
        if text:
            entry_field.insert(0, text)
            process_command()

    threading.Thread(target=run_voice, daemon=True).start()


# GUI INTERFEYS
root = tk.Tk()
root.title("MyAI - System Command Center")
root.geometry("650x650")
root.configure(bg="#0B0E14")

header_frame = tk.Frame(root, bg="#131722", bd=1, relief=tk.SOLID)
header_frame.pack(fill=tk.X, padx=10, pady=10)

title_label = tk.Label(
    header_frame,
    text="● SYSTEM ONLINE | AI CHAT ACTIVE",
    font=("Segoe UI", 11, "bold"),
    fg="#00F0FF",
    bg="#131722",
)
title_label.pack(side=tk.LEFT, padx=10, pady=5)

chat_log = tk.Text(
    root,
    bd=1,
    bg="#0F131C",
    fg="#A0AAB0",
    font=("Consolas", 10),
    wrap=tk.WORD,
    padx=12,
    pady=12,
)
chat_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
chat_log.tag_config("user_tag", foreground="#FFD700", font=("Consolas", 10, "bold"))
chat_log.tag_config("ai_tag", foreground="#00F0FF", font=("Consolas", 10))

input_frame = tk.Frame(root, bg="#0B0E14")
input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

entry_field = tk.Entry(
    input_frame,
    bg="#131722",
    fg="#00F0FF",
    font=("Consolas", 11),
    insertbackground="#00F0FF",
    bd=1,
    relief=tk.SOLID,
)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 8))
entry_field.bind("<Return>", process_command)

send_btn = tk.Button(
    input_frame,
    text="EXECUTE",
    font=("Segoe UI", 9, "bold"),
    bg="#00F0FF",
    fg="#0B0E14",
    bd=0,
    padx=14,
    command=process_command,
)
send_btn.pack(side=tk.RIGHT, ipady=6, padx=(0, 5))

voice_btn = tk.Button(
    input_frame,
    text="🎤 VOICE",
    font=("Segoe UI", 9, "bold"),
    bg="#FFD700",
    fg="#0B0E14",
    bd=0,
    padx=14,
    command=start_voice_recognition,
)
voice_btn.pack(side=tk.RIGHT, ipady=6)

root.mainloop()