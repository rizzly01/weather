import streamlit as st
import requests
from datetime import datetime

# API Configuration
API_KEY = "57e00c15d85b13d67a6f52afdd0f3377"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Custom CSS styling
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f8ff;
        color: #333;
    }

    .weather-title {
        font-size: 3em;
        text-align: center;
        margin-top: 20px;
        color: #4CAF50;
    }

    .stTextInput > div > div > input {
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #aaa;
        font-size: 16px;
        color: #333;
        background-color: #ffffff;
    }

    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }

    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 12px 25px;
        border-radius: 10px;
        width: 100%;
        border: none;
    }

    .stButton > button:hover {
        background-color: #45a049;
    }

    .weather-card {
        padding: 25px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        margin-top: 30px;
    }

    .output-text {
        font-size: 1.2em;
        color: black;
        text-align: center;
    }

    .metric {
        font-size: 1.2em;
        text-align: center;
        margin-top: 10px;
    }

    .metric div {
        margin-bottom: 10px;
    }

    .metric-icon {
        font-size: 2em;
        margin-right: 10px;
    }

    .footer {
        text-align: center;
        font-size: 0.9em;
        color: #888;
        margin-top: 50px;
    }

    .error-message {
        color: red;
        font-size: 1.2em;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='weather-title'>🌤️ Weather Finder</h1>", unsafe_allow_html=True)

# City input field and button
city = st.text_input("Enter the city name:", placeholder="Type your city name")
button_clicked = st.button("Get Weather")

def get_weather(city):
    try:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            st.markdown(f"<div class='error-message'>City not found! Please check the spelling.</div>", unsafe_allow_html=True)
            return None
    except Exception as e:
        st.markdown(f"<div class='error-message'>Unable to connect to weather service. Please try again later.</div>", unsafe_allow_html=True)
        return None

# Check if button was clicked and city is entered
if button_clicked and city:
    weather_data = get_weather(city)
    
    if weather_data:
        # Extracting data
        main_weather = weather_data['weather'][0]['main']
        icon = get_weather_icon(main_weather)
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']
        max_temp = weather_data['main']['temp_max']
        min_temp = weather_data['main']['temp_min']
        country = weather_data['sys']['country']

        # Display weather card
        st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
        
        # Greeting and location
        st.markdown(f"<h2 class='output-text'>Weather in {city.title()}, {country}</h2>", unsafe_allow_html=True)
        
        # Main weather
        st.markdown(f"<div class='output-text'><span style='font-size: 3em;'>{icon}</span><h3>{temp}°C</h3><p>{description.title()}</p></div>", unsafe_allow_html=True)

        # Weather metrics (humidity, wind speed, feels like)
        st.markdown(f"<div class='metric'><span class='metric-icon'>💧</span><div><strong>Humidity</strong><br>{humidity}%</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric'><span class='metric-icon'>💨</span><div><strong>Wind Speed</strong><br>{wind_speed} m/s</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric'><span class='metric-icon'>🌡️</span><div><strong>Feels Like</strong><br>{feels_like}°C</div></div>", unsafe_allow_html=True)

        # Additional metrics (max and min temperature)
        st.markdown(f"<div class='metric'><span class='metric-icon'>⬆️</span><div><strong>Max Temp</strong><br>{max_temp}°C</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric'><span class='metric-icon'>⬇️</span><div><strong>Min Temp</strong><br>{min_temp}°C</div></div>", unsafe_allow_html=True)

        # Timestamp
        st.markdown(f"<div class='output-text'>Last updated: {datetime.now().strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)  # End weather card

# Footer
st.markdown("<div class='footer'>Powered by OpenWeatherMap API</div>", unsafe_allow_html=True)

def get_weather_icon(condition):
    icons = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '🌧️',
        'Drizzle': '🌦️',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
        'Smoke': '🌫️',
        'Haze': '🌫️',
        'Dust': '🌫️',
        'Fog': '🌫️',
    }
    return icons.get(condition, '🌈')
