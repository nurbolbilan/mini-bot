import requests

while True:
    city = input("Введите город: ")
    if city == "":
        print('Введите название города!')
    if city == 'exit':
        break
    url = f"https://wttr.in/{city}?format=3"

    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Погода:", response.text)
    except requests.exceptions.RequestException as e:
        print("Ошибка при получении данных:", e)