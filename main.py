import requests
from openai import OpenAI

client = OpenAI(
    base_url="http://host.docker.internal:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="tinyllama",
    messages=[
        {"role": "user", "content": "What is heavier between a kilogram of lead or a kilogram of feathers?"}
    ],
)
print(response.choices[0].message.content)
url = "https://api.open-meteo.com/v1/forecast?latitude=44.4268&longitude=26.1025&current_weather=true"
try:
    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    vreme_curenta = data["current_weather"]

    print(" Informații Meteo Live ")
    print(f"Temperatură: {vreme_curenta['temperature']}°C")
    print(f"Viteză vânt: {vreme_curenta['windspeed']} km/h")
    print(f"Direcție vânt: {vreme_curenta['winddirection']}°")

except requests.exceptions.RequestException as e:
    print(f"A apărut o eroare la conectarea la API: {e}")



