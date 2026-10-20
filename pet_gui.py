import threading
import tkinter as tk
from PIL import Image, ImageTk
import pyttsx3
from ai_chat import ask_ai
from app_control import handle_in_app_actions, listen_voice_command


def speak_text(text):
    """NIKO javobini alohida potokda ovozli o'qish"""
    def run_speech():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f'Ovoz chiqarishda xatolik: {e}')

    threading.Thread(target=run_speech, daemon=True).start()


class DesktopPet:

    def __init__(self, root):
        self.root = root
        self.root.title('NIKO Pet')

        # Oyna ramkasini yo'qotish va har doim ustida turish
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.95)
        self.root.config(bg='#2c3e50')

        # Personaj rasmi yoki stikeri
        try:
            img = Image.open('niko_avatar.png').convert('RGBA')
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            self.pet_img = ImageTk.PhotoImage(img)
            self.label = tk.Label(root, image=self.pet_img, bg='#2c3e50')
        except Exception:
            self.label = tk.Label(
                root,
                text='🤖\nNIKO',
                font=('Segoe UI', 14, 'bold'),
                bg='#2c3e50',
                fg='white',
                padx=10,
                pady=10,
            )

        self.label.pack()

        # Sichqoncha harakatlari
        self.label.bind('<Button-1>', self.start_move)
        self.label.bind('<B1-Motion>', self.do_move)
        
        # O'ng tugma - Chat ochmasdan to'g'ridan-to'g'ri ovozli buyruq berish!
        self.label.bind('<Button-3>', self.listen_direct_voice)
        
        # Ikki marta bosganda to'liq chat oynasini ochish
        self.label.bind('<Double-Button-1>', self.open_chat_window)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')

    def show_speech_bubble(self, text):
        """NIKO ikonka yonida qisqa vaqtinchalik javob oynasini chiqarish"""
        bubble = tk.Toplevel(self.root)
        bubble.overrideredirect(True)
        bubble.attributes('-topmost', True)
        
        # Ikonkaning turgan joyini aniqlash
        x = self.root.winfo_x() + 110
        y = self.root.winfo_y()
        bubble.geometry(f"+{x}+{y}")
        
        label = tk.Label(
            bubble, 
            text=text, 
            font=('Segoe UI', 10, 'bold'), 
            bg='#2c3e50', 
            fg='#2ecc71', 
            padx=10, 
            pady=8,
            relief=tk.SOLID,
            bd=1
        )
        label.pack()
        
        # 6 sekunddan keyin avtomatik yopilish
        self.root.after(6000, bubble.destroy)

    def listen_direct_voice(self, event=None):
        """Chatni ochmasdan to'g'ridan-to'g'ri eshitish va javob berish"""
        def voice_worker():
            self.show_speech_bubble("🎤 Eshitayapman, gapiring...")
            speak_text("Eshitayapman")
            
            spoken_text = listen_voice_command()
            
            if spoken_text and not spoken_text.startswith('Xatolik') and not spoken_text.startswith('Vaqt'):
                # Buyruq yoki AI orqali ishlash
                exec_status, resp = handle_in_app_actions(spoken_text)
                if not exec_status:
                    resp = ask_ai(spoken_text)
                
                # Ekranda qisqa ko'rsatish va ovoz chiqarish
                self.show_speech_bubble(f"NIKO: {resp}")
                speak_text(resp)
            else:
                self.show_speech_bubble("⚠️ Tushunmadim, qayta urinib ko'ring.")
                speak_text("Tushunmadim")

        threading.Thread(target=voice_worker, daemon=True).start()

    def open_chat_window(self, event=None):
        chat_win = tk.Toplevel(self.root)
        chat_win.title('NIKO AI Chat')
        chat_win.geometry('420x520')
        chat_win.attributes('-topmost', True)

        display = tk.Text(chat_win, wrap=tk.WORD, font=('Segoe UI', 10))
        display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(chat_win)
        input_frame.pack(padx=10, pady=5, fill=tk.X)

        entry = tk.Entry(input_frame, font=('Segoe UI', 11))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        def process_message(txt):
            if not txt.strip():
                return
            display.insert(tk.END, f'Siz: {txt}\n', 'user')
            
            exec_status, resp = handle_in_app_actions(txt)
            if not exec_status:
                resp = ask_ai(txt)

            display.insert(tk.END, f'NIKO: {resp}\n\n', 'niko')
            display.see(tk.END)
            speak_text(resp)

        def send_text(e=None):
            txt = entry.get().strip()
            entry.delete(0, tk.END)
            process_message(txt)

        entry.bind('<Return>', send_text)

        send_btn = tk.Button(input_frame, text='Yuborish', font=('Segoe UI', 9, 'bold'), bg='#2ecc71', fg='white', command=send_text)
        send_btn.pack(side=tk.RIGHT)


root = tk.Tk()
root.geometry('100x100+1200+600')
app = DesktopPet(root)
root.mainloop()