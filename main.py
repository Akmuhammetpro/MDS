import requests

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