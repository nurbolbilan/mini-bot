# currency_bot.py
import requests
import datetime
import sys
from xml.etree import ElementTree as ET

HEADERS = {"User-Agent": "currency-bot/1.0 (+https://github.com/yourname)"}
TIMEOUT = 10

def fetch_from_date(date_obj):
    date_str = date_obj.strftime("%d.%m.%Y")
    url = f"https://nationalbank.kz/rss/get_rates.cfm?fdate={date_str}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print("Ошибка соединения при запросе get_rates.cfm:", e)
        return None, url
    if r.status_code != 200:
        print(f"get_rates.cfm вернул код {r.status_code} для {date_str}")
        return None, url
    r.encoding = r.apparent_encoding or "utf-8"
    return r.text, url

def fetch_rates_all():
    url = "https://nationalbank.kz/rss/rates_all.xml"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        print("Ошибка соединения при запросе rates_all.xml:", e)
        return None, url
    if r.status_code != 200:
        print(f"rates_all.xml вернул код {r.status_code}")
        return None, url
    r.encoding = r.apparent_encoding or "utf-8"
    return r.text, url

def parse_xml_and_print(xml_text):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print("Не удалось распарсить XML:", e)
        return False

    items = root.findall(".//item")
    if not items:
        items = root.findall(".//rate") + root.findall(".//item")

    wanted = {"USD": None, "EUR": None, "RUB": None, "JPY": None}
    for item in items:
        title_el = item.find("title")
        desc_el = item.find("description")
        if title_el is None:
            continue
        code = title_el.text.strip()
        if desc_el is not None and desc_el.text:
            value = desc_el.text.strip()
        else:
            v = item.find("value") or item.find("rate") or item.find("amount")
            value = v.text.strip() if (v is not None and v.text) else None

        if code in wanted and value:
            wanted[code] = value

    today = datetime.date.today().isoformat()
    print("\n💰 Курс валют (по данным НБРК) —", today)
    print("-" * 40)
    for cur, val in wanted.items():
        if val:
            print(f"{cur}: {val} ₸")
        else:
            print(f"{cur}: не найдено в ответе")
    print("-" * 40)
    return True

def main():
    today = datetime.date.today()
    xml_text, source_url = fetch_from_date(today)
    if xml_text:
        print("Источник:", source_url)
        ok = parse_xml_and_print(xml_text)
        if ok:
            return

    # fallback: пробуем rates_all.xml
    print("Пробую fallback: rates_all.xml ...")
    xml_text, source_url = fetch_rates_all()
    if xml_text:
        print("Источник:", source_url)
        ok = parse_xml_and_print(xml_text)
        if ok:
            return

    print("Не удалось получить курсы. Проверь соединение или открой URL в браузере:")
    print("1) https://nationalbank.kz/rss/get_rates.cfm?fdate=DD.MM.YYYY (замени DD.MM.YYYY на сегодняшнюю дату)")
    print("2) https://nationalbank.kz/rss/rates_all.xml")
    sys.exit(1)

if __name__ == "__main__":
    main()
