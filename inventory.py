import os
import datetime

MEMORY_FILE = "memory.txt"
OMBOR_FILE = "ombor.txt"
MOLIYA_FILE = "moliya.txt"


def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def check_inventory(query=""):
    """Ombor faylidan mahsulot qoldig'ini tekshirish yoki barcha qoldiqlarni chiqarish"""
    if not os.path.exists(OMBOR_FILE):
        return "Ombor bo'sh. Hozircha mahsulot kiritilmagan."

    items = {}
    with open(OMBOR_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4:
                turi, name, qty = parts[0].lower(), parts[1].lower(), parts[2]
                try:
                    q_val = float(qty)
                    if name not in items:
                        items[name] = {"kirim": 0, "chiqdi": 0}
                    if turi in ["kirim", "keldi"]:
                        items[name]["kirim"] += q_val
                    elif turi in ["chiqdi", "sotuv", "sotdi"]:
                        items[name]["chiqdi"] += q_val
                except ValueError:
                    continue

    if query:
        query = query.lower().strip()
        if query in items:
            balance = items[query]["kirim"] - items[query]["chiqdi"]
            return f"📦 {query.capitalize()} qoldig'i: {balance:,.0f} ta"
        else:
            return f'Bazada "{query}" nomli mahsulot topilmadi.'
    else:
        if not items:
            return "Ombor bo'sh."
        res_list = []
        for k, v in items.items():
            balance = v["kirim"] - v["chiqdi"]
            res_list.append(f"• {k.capitalize()}: {balance:,.0f} ta")
        return "📦 Barcha Ombor Qoldiqlari:\n" + "\n".join(res_list)


def add_record(record_type, name, qty, price=0.0):
    """Kirim yoki chiqim amallarini ombor.txt va moliya.txt fayllariga yozish"""
    curr_date = get_current_date()
    name = name.capitalize()

    # Omborga yozish
    with open(OMBOR_FILE, "a", encoding="utf-8") as f:
        f.write(f"{record_type} | {name} | {qty} | {price} | {curr_date}\n")

    # Moliyaga yozish
    with open(MOLIYA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{record_type} | {name} | {qty} | {price} | {curr_date}\n")