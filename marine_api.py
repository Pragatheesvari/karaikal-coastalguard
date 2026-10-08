import requests

latitude = 10.9254
longitude = 79.8380

url = "https://marine-api.open-meteo.com/v1/marine"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "wave_height,wave_direction,wave_period,sea_level_height_msl",
    "timezone": "Asia/Kolkata"
}

response = requests.get(
    url,
    params=params,
    timeout=10
)

if response.status_code == 200:

    data = response.json()

    current = data["current"]

    print("🌊 Karaikal Marine Data")
    print("-------------------------")

    print(
        "Wave Height:",
        current["wave_height"],
        "m"
    )

    print(
        "Wave Direction:",
        current["wave_direction"],
        "°"
    )

    print(
        "Wave Period:",
        current["wave_period"],
        "seconds"
    )

    print(
        "Sea Level:",
        current["sea_level_height_msl"],
        "m"
    )

else:

    print(
        "❌ Marine API Error:",
        response.status_code
    )