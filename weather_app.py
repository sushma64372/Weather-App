import requests


# Weather Conditions
weather_codes = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Heavy Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Moderate Rain Showers",
    82: "Heavy Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Heavy Thunderstorm"
}


# Get Weather Information
def get_weather():

    print("\n===== WEATHER APP =====")

    city = input("Enter city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    try:

        # Step 1: Search City in India
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 10,
            "language": "en",
            "format": "json",
            "countryCode": "IN"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params,
            timeout=15
        )

        geo_response.raise_for_status()

        geo_data = geo_response.json()

        results = geo_data.get("results", [])

        # Find Indian City
        location = next(
            (
                item for item in results
                if item.get("country_code") == "IN"
            ),
            None
        )

        if location is None:
            print("Indian city not found!")
            return

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get Weather Data
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto"
        }

        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        current = data["current"]

        # Step 3: Get Weather Condition
        condition = weather_codes.get(
            current["weather_code"],
            "Unknown"
        )

        # Step 4: Display Weather Report
        print("\n" + "=" * 40)
        print("           WEATHER REPORT")
        print("=" * 40)

        print("City:", location["name"])
        print("Country:", location.get("country", "Unknown"))

        print("-" * 40)

        print(
            "Temperature:",
            current["temperature_2m"], "°C"
        )

        print(
            "Feels Like:",
            current["apparent_temperature"], "°C"
        )

        print(
            "Humidity:",
            current["relative_humidity_2m"], "%"
        )

        print(
            "Wind Speed:",
            current["wind_speed_10m"], "km/h"
        )

        print("Weather Condition:", condition)

        print("=" * 40)

        print("\nWeather data fetched successfully!")

    except requests.exceptions.RequestException as error:

        print("\nUnable to connect to weather service.")
        print("Error:", error)

    except (KeyError, IndexError, ValueError):

        print("\nUnable to process weather data.")


# Main Program
while True:

    get_weather()

    choice = input(
        "\nCheck another city? (yes/no): "
    ).strip().lower()

    if choice != "yes":

        print("\nThank you for using Weather App!")
        break