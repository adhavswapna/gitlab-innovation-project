import requests
import os

class ShipLocationProvider:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_ship_location(self):
        try:
            # For this example, we'll manually input latitude and longitude
            latitude = float(input("Enter ship's latitude: "))
            longitude = float(input("Enter ship's longitude: "))
            return latitude, longitude
        except ValueError as ve:
            print(f"Error: {ve}")

        return None, None

def get_weather(api_key, latitude, longitude, city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric",  # Use metric units for Celsius
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print(f"Error: {response.status_code}")
        return None

def display_weather(weather_data):
    if weather_data:
        print(f"Weather at the ship's location:")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Condition: {weather_data['weather'][0]['description']}")
    else:
        print("Unable to retrieve weather data.")

if __name__ == "__main__":
    ip2location_api_key = os.getenv("IP2LOCATION_API_KEY")
    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    ship_location_provider = ShipLocationProvider(api_url="", api_key=ip2location_api_key)
    latitude, longitude = ship_location_provider.get_ship_location()

    if latitude is not None and longitude is not None:
        weather_data = get_weather(openweathermap_api_key, latitude, longitude)
        display_weather(weather_data)
    else:
        print("Cannot proceed without a valid ship location.")
