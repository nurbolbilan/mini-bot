import requests

def get_fact():
    data = requests.get("https://uselessfacts.jsph.pl/random.json?language=en").json()
    return f'📘 {data["text"]}'

print(get_fact())
