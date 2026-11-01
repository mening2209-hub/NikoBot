import json
import os

PRODUCTS_FILE = "products.json"

# Boshlang'ich mahsulotlar bazasi (agar fayl bo'lmasa)
DEFAULT_PRODUCTS = {
    "pepsi": {"name": "Pepsi", "price": 11500, "stock": 40},
    "coca cola": {"name": "Coca Cola", "price": 12000, "stock": 50},
    "fanta": {"name": "Fanta", "price": 11000, "stock": 30},
    "nestle suv": {"name": "Nestle suv", "price": 3000, "stock": 100}
}

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Fayl bo'lmasa yaratib qo'yamiz
    save_products(DEFAULT_PRODUCTS)
    return DEFAULT_PRODUCTS

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

def handle_in_app_actions(user_text):
    text_lower = user_text.lower().strip()
    products = load_products()

    # 1. Mahsulotlar ro'yxatini so'raganda
    if any(word in text_lower for word in ["nima", "maxsulot", "mahsulot", "bor", "katalog", "menyusi"]):
        response = "Assalomu alaykum! Hozirda do'konimizda quyidagi mahsulotlar mavjud:\n\n"
        for key, p in products.items():
            response += f"- {p['name']} — {p['price']:,} so'm ({p['stock']} ta bor)\n".replace(",", " ")
        response += "\nQaysi biridan yetkazib beraylik, nechta olmoqchisiz?"
        return True, response

    # 2. Buyurtma berishni aniqlash (raqam va mahsulot nomi qatnashgan bo'lsa)
    # Masalan: "21 ta pepsi kerek" yoki "10 ta coca cola"
    words = text_lower.split()
    quantity = None
    
    # Matn ichidan sonni qidirish
    for i, word in enumerate(words):
        if word.isdigit():
            quantity = int(word)
            # Sonning yonidagi so'zlarni mahsulot nomi sifatida qidiramiz
            target_product = None
            for p_key, p_data in products.items():
                if p_key in text_lower:
                    target_product = p_key
                    break
            
            if target_product and quantity:
                p = products[target_product]
                if p["stock"] >= quantity:
                    total_price = quantity * p["price"]
                    # Ombordan ayirib qo'shamiz
                    p["stock"] -= quantity
                    save_products(products)
                    
                    response = (f"✅ Buyurtmangiz qabul qilindi!\n\n"
                                f"📦 Mahsulot: {p['name']}\n"
                                f"🔢 Miqdori: {quantity} ta\n"
                                f"💰 Umumiy narx: {total_price:,} so'm\n\n"
                                f"Yetkazib berish uchun manzilingizni yozib yuboring!").replace(",", " ")
                    return True, response
                else:
                    return True, f"Kechirasiz, hozirda {p['name']}dan faqat {p['stock']} ta qolgan."

    # 3. Agar shunchaki salomlashish yoki tushunarsiz bo'lsa
    if any(word in text_lower for word in ["salom", "assalomu", "alo"]):
        return True, "Assalomu alaykum! Qanday mahsulot kerak edi? Mahsulotlarni ko'rish uchun 'nima mahsulot bor' deb yozing."

    return False, None