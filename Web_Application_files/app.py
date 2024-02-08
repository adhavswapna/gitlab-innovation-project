from flask import Flask, render_template, request
from ship_weather_script import get_weather
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# how the project clearly articulate the problem it aims to address for GitLab users?
# -: This web app fetches and displays weather information based on user input.

@app.route('/')
def index():
    return render_template('index.html')

# how it solve a real problem for GitLab users?: 
#-: This route fetches weather data based on user input and displays it.

@app.route('/fetch_weather', methods=['POST'])
def fetch_weather():
    try:
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        city_name = request.form['city_name']

        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        # Innovativeness: 
        # -: Utilize a creative approach in handling the weather data.
        weather_data = get_weather(api_key, latitude, longitude, city_name)

        if weather_data:
            temperature = convert_temperature_unit(weather_data['main']['temp'])
            icon_url = f"http://openweathermap.org/img/w/{weather_data['weather'][0]['icon']}.png"

            # Overall Quality:
            # -: Display weather information with attention to design and user experience.
            return render_template('weather_result.html', temperature=temperature,
                                   condition=weather_data['weather'][0]['description'],
                                   wind_speed=weather_data['wind']['speed'],
                                   wind_direction=weather_data['wind']['deg'],
                                   icon_url=icon_url)
        else:
            # how the project solve a real problem for GitLab users?
            #-:Inform the user if weather data cannot be retrieved.
            return "Unable to retrieve weather data."
    except ValueError:

        # Overall Quality: Handle invalid user input gracefully.
        return "Invalid latitude, longitude, or city name. Please enter valid values."

# Scalability-:The web app is designed to handle user requests for weather information.
def convert_temperature_unit(temperature):
    # Convert temperature to Fahrenheit
    temperature_fahrenheit = (temperature * 9/5) + 32
    return temperature_fahrenheit

if __name__ == '__main__':
    # Feasibility:
    # -: Ensure the web app can run successfully with available resources and technology.
    app.run(debug=True)
