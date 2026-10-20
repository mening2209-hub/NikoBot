import tkinter as tk
from tkinter import scrolledtext, ttk
from ai_chat import ask_ai
from app_control import handle_in_app_actions

def send_query(event=None):
    user_text = entry_field.get().strip()
    if not user_text:
        return
    
    # Foydalanuvchi xabarini oynaga chiqarish
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"Siz: {user_text}\n", "user")
    entry_field.delete(0, tk.END)
    
    # Vaqtinchalik "o'ylanmoqda" xabarini chiqarish
    chat_display.insert(tk.END, "NIKO: Javob tayyorlanmoqda...\n\n", "loading")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)
    root.update()

    # NIKO javobini olish (buyruq yoki Ollama AI orqali)
    executed, resp_msg = handle_in_app_actions(user_text)
    if not executed:
        resp_msg = ask_ai(user_text)

    # Vaqtinchalik xabarni o'chirib, haqiqiy javobni joylash
    chat_display.config(state=tk.NORMAL)
    chat_display.delete("end-2l", "end-1c")  # Oxirgi loading qatorini o'chirish
    chat_display.insert(tk.END, f"NIKO: {resp_msg}\n\n", "niko")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)

def quick_action(action_text):
    entry_field.delete(0, tk.END)
    entry_field.insert(0, action_text)
    send_query()

# Asosiy oyna sozlamalari
root = tk.Tk()
root.title("NIKO - Biznes va Ombor Menejeri")
root.geometry("580x680")
root.config(bg="#f4f6f9")

# Yuqori sarlavha (Header)
title_label = tk.Label(
    root, 
    text="🤖 NIKO - Intellektual Yordamchi", 
    font=("Segoe UI", 13, "bold"), 
    bg="#2c3e50", 
    fg="white", 
    pady=12
)
title_label.pack(fill=tk.X)

# Chat oynasi (Suhbat tarixi)
chat_display = scrolledtext.ScrolledText(
    root, 
    wrap=tk.WORD, 
    font=("Segoe UI", 10), 
    state=tk.DISABLED, 
    bg="#ffffff", 
    relief=tk.FLAT,
    bd=1
)
chat_display.pack(padx=12, pady=10, fill=tk.BOTH, expand=True)

# Chat teglari uchun ranglar va shriftlar
chat_display.tag_config("user", foreground="#2980b9", font=("Segoe UI", 10, "bold"))
chat_display.tag_config("niko", foreground="#27ae60", font=("Segoe UI", 10))
chat_display.tag_config("loading", foreground="#7f8c8d", font=("Segoe UI", 9, "italic"))

# Matn kiritish paneli
input_frame = tk.Frame(root, bg="#f4f6f9")
input_frame.pack(padx=12, pady=5, fill=tk.X)

entry_field = tk.Entry(
    input_frame, 
    font=("Segoe UI", 11), 
    relief=tk.SOLID, 
    bd=1
)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=6)
entry_field.bind("<Return>", send_query)

send_btn = tk.Button(
    input_frame, 
    text="Yuborish", 
    font=("Segoe UI", 10, "bold"), 
    bg="#2ecc71", 
    fg="white", 
    activebackground="#27ae60",
    activeforeground="white",
    relief=tk.FLAT,
    command=send_query, 
    padx=15, 
    pady=4,
    cursor="hand2"
)
send_btn.pack(side=tk.RIGHT)

# Pastki tezkor harakat tugmalari (Action Buttons)
btn_frame = tk.Frame(root, bg="#f4f6f9")
btn_frame.pack(padx=12, pady=(5, 12), fill=tk.X)

btn_style = {
    "font": ("Segoe UI", 9, "bold"),
    "fg": "white",
    "relief": tk.FLAT,
    "pady": 6,
    "cursor": "hand2"
}

tk.Button(btn_frame, text="👥 Mijozlar", bg="#3498db", command=lambda: quick_action("Mijozlar ro'yxati"), **btn_style).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
tk.Button(btn_frame, text="📦 Ombor", bg="#e67e22", command=lambda: quick_action("Omborda nima bor"), **btn_style).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)
tk.Button(btn_frame, text="📊 Tahlil", bg="#9b59b6", command=lambda: quick_action("Moliyaviy tahlil"), **btn_style).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=3)

root.mainloop()