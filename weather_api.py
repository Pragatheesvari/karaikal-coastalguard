import requests

latitude = 10.9254
longitude = 79.8380

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,wind_speed_10m",
    "hourly": "precipitation",
    "forecast_days": 1
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    print("🌍 Karaikal Weather Data")
    print("-------------------------")

    print("Temperature:",
          data["current"]["temperature_2m"], "°C")

    print("Wind Speed:",
          data["current"]["wind_speed_10m"], "km/h")

    rainfall = sum(data["hourly"]["precipitation"])

    print("Rainfall:",
          rainfall, "mm")

else:
    print("❌ API Error:", response.status_code)