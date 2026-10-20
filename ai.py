import os
import webbrowser
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import ollama

MEMORY_FILE = "memory.txt"


def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def save_memory(text):
    with open(MEMORY_FILE, "a", encoding="utf-8") as file:
        file.write(text + "\n")


def web_search(query):
    text = ""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            for r in results:
                text += f"Sarlavha: {r.get('title', '')}\nLola: {r.get('href', '')}\n\n"
    except Exception as e:
        text = f"Qidiruvda xatolik: {e}"
    return text


def ask_ai(prompt):
    response = ollama.chat(
        model="qwen2.5:7b", messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


print("MyAI ishga tushdi!")
print("Xotira: ishlaydi")
print("Internet: ishlaydi")
print("Video senariy: ishlaydi")
print()
print("Chiqish uchun: chiqish")
print()

while True:
    savol = input("Sen: ").strip()

    if not savol:
        continue

    savol_lower = savol.lower()

    # CHIQISH
    if savol_lower == "chiqish":
        print("AI: Xayr!")
        break

    # INSTAGRAM VA DASTURLARNI OCHISH MANTIQI
    if savol_lower in [
        "insta",
        "instagram",
        "instagramni och",
        "instagramga kir",
    ]:
        webbrowser.open("https://www.instagram.com")
        print("AI: Instagram sahifasi brauzerda ochildi.")
        continue

    elif "instagram" in savol_lower and any(
        k in savol_lower for k in ["akaunt", "profil", "qidir"]
    ):
        # Akkaunt nomini ajratib olish (masalan: "instagramdan messi profilini qidir")
        target = (
            savol_lower.replace("instagramdan", "")
            .replace("instagram", "")
            .replace("akaunt", "")
            .replace("profilini", "")
            .replace("profil", "")
            .replace("qidir", "")
            .replace("ni", "")
            .strip()
        )
        if target:
            url = f"https://www.instagram.com/{target}/"
            webbrowser.open(url)
            print(f"AI: Instagram'da @{target} profili ochilmoqda...")
        else:
            webbrowser.open("https://www.instagram.com")
            print("AI: Instagram ochildi.")
        continue

    # XOTIRA
    if savol_lower.startswith("eslab qol"):
        malumot = savol[9:].strip()
        if malumot:
            save_memory(malumot)
            print("AI: Xo'p, eslab qolaman.")
        else:
            print("AI: Nimani eslab qolishimni yoz.")
        continue

    # INTERNET
    if savol_lower.startswith("internet"):
        qidiruv = savol[9:].strip()
        if not qidiruv:
            print("AI: Nima qidirishimni yoz.")
            continue

        print("Internetdan qidiryapman...")
        try:
            natijalar = web_search(qidiruv)
            if not natijalar:
                print("AI: Natija topilmadi.")
                continue

            prompt = (
                "Sen MyAI yordamchisisan.\n"
                "Faqat tabiiy va ravon o'zbek tilida javob ber.\n"
                "Tarjima qilingandek g'alati gaplar ishlatma.\n"
                "Javobni oddiy odam tushunadigan qilib yoz.\n\n"
                "Savol:\n" + qidiruv + "\n\n"
                "Internet natijalari:\n" + natijalar
            )
            javob = ask_ai(prompt)
            print("AI:", javob)
        except Exception as error:
            print("Internet xatosi:", error)
        continue

    # VIDEO
    if savol_lower.startswith("video"):
        mavzu = savol[5:].strip()
        if not mavzu:
            print("AI: Qanday video kerakligini yoz.")
            continue

        print("Video senariysi tayyorlanmoqda...")
        prompt = (
            "Sen professional video senariy yozuvchisisan.\n"
            "Mavzu: " + mavzu + "\n\n"
            "30 soniyalik qisqa video senariysi yoz.\n"
            "Faqat tabiiy va ravon o'zbek tilidan foydalan.\n"
            "Juda oddiy so'zlardan foydalan.\n"
            "Tarjima qilingandek yozma.\n"
            "Bir xil gaplarni takrorlama.\n"
            "Keraksiz tushuntirish yozma.\n"
            "Qahramon o'zini Qwen deb atamasin.\n\n"
            "Faqat quyidagi formatda javob ber:\n\n"
            "Sarlavha: ...\n\n"
            "Kirish:\n...\n\n"
            "1-kadr:\n...\n\n"
            "2-kadr:\n...\n\n"
            "3-kadr:\n...\n\n"
            "Yakun:\n...\n\n"
            "Hech qanday tarjima yoki qo'shimcha izoh yozma."
        )
        senariy = ask_ai(prompt)
        print("\nVIDEO SENARIYSI:\n" + senariy + "\n")
        continue

    # ODDIY SUHBAT
    memory = load_memory()
    prompt = (
        "Sen mening shaxsiy MyAI yordamchimsan.\n"
        "Faqat tabiiy va ravon o'zbek tilida javob ber.\n"
        "Tarjima qilingandek g'alati gaplar ishlatma.\n"
        "Javobni oddiy odam tushunadigan qilib yoz.\n\n"
        "Foydalanuvchi haqidagi xotira:\n"
        + memory
        + "\n\n"
        "Foydalanuvchining savoli:\n"
        + savol
    )

    try:
        javob = ask_ai(prompt)
        print("AI:", javob)
    except Exception as error:
        print("AI xatosi:", error)