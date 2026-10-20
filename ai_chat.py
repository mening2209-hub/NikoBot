import os

def ask_ai(user_text, context_info=""):
    text = user_text.lower().strip()
    
    # 1. Ombor faylini o'qish
    products = []
    if os.path.exists("ombor.txt"):
        with open("ombor.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if ":" in line:
                    parts = line.split(":")
                    if len(parts) >= 3:
                        products.append({
                            "name": parts[0].strip().lower(),
                            "price": int(parts[1].strip()),
                            "count": int(parts[2].strip())
                        })

    # 2. Agar ombor bo'sh bo'lsa
    if not products:
        return "Assalomu alaykum! Hozircha omborimizda mahsulotlar tugagan edi, tez orada yangi mahsulotlar keltiriladi."

    # 3. Mijoz barcha mahsulotlar ro'yxatini so'rasa
    if any(word in text for word in ["nima", "katalog", "ro'yxat", "qanday", "hamma"]):
        res = "Assalomu alaykum! Hozirda do'konimizda quyidagi mahsulotlar mavjud:\n\n"
        for p in products:
            res += f"• {p['name'].capitalize()} — {p['price']:,} so'm ({p['count']} ta bor)\n".replace(',', ' ')
        res += "\nQaysi biridan yetkazib beraylik, nechta olmoqchisiz?"
        return res

    # 4. Aniq bir mahsulot va soni so'ralganda (masalan: "30 ta pepsi" yoki "pepsi 30 ta")
    for p in products:
        if p["name"] in text:
            # Soni aytilgan bo'lsa hisoblash
            words = text.split()
            nums = [int(w) for w in words if w.isdigit()]
            if nums:
                qty = nums[0]
                if qty <= p["count"]:
                    total = qty * p["price"]
                    return f"Tushundim! {qty} ta {p['name'].capitalize()} jami {total:,} so'm bo'ladi.\n\nYetkazib berish uchun manzilingizni qoldirasizmi?".replace(',', ' ')
                else:
                    return f"Afsuski, omborimizda hozirda {p['count']} ta {p['name'].capitalize()} bor ekan. {p['count']} ta yetkazib beraylikmi?"
            
            # Shunchaki narxi so'ralganda
            return f"Ha, {p['name'].capitalize()} bor! Narxi {p['price']:,} so'm, omborda {p['count']} ta mavjud. Nechta olmoqchisiz?".replace(',', ' ')

    # 5. Boshqa umumiy vaqtda
    return "Assalomu alaykum! Bemalol so'rashingiz mumkin. Qaysi mahsulotimiz haqida ma'lumot beray?"
