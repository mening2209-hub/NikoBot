import pyttsx3
import threading
import queue

speech_queue = queue.Queue()

def _speech_worker():
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    while True:
        text = speech_queue.get()
        if text is None:
            break
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
        speech_queue.task_done()

# Ovozni bitta oqimda navbat bilan o'qydigan qilish
threading.Thread(target=_speech_worker, daemon=True).start()

def speak_response(text):
    if text:
        speech_queue.put(text)