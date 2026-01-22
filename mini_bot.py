import requests

def get_quote():
    data = requests.get("https://quotes.rest/qod?language=en").json()
    return f'💬 {data["content"]} — {data["author"]}'

def get_currency():
    data = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
    return f'💵 1 USD = {data["rates"]["KZT"]} KZT'

def get_fact():
    data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    return f'📘 {data["text"]}'

print("Выбери опцию:\n1 — Цитата дня\n2 — Курс валют\n3 — Факт дня")
choice = input("Твой выбор: ")

if choice == "1":
    print(get_quote())
elif choice == "2":
    print(get_currency())
elif choice == "3":
    print(get_fact())
else:
    print("Неверный выбор!")
