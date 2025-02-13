import streamlit as st
import requests
from datetime import datetime

# API Configuration
API_KEY = "57e00c15d85b13d67a6f52afdd0f3377"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

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

def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning! ☀️"
    elif 12 <= hour < 17:
        return "Good Afternoon! 🌞"
    elif 17 <= hour < 21:
        return "Good Evening! 🌅"
    else:
        return "Good Night! 🌙"

# Streamlit page layout and styling
st.set_page_config(page_title="Weather Forecast", page_icon="☀️", layout="centered")

# Custom CSS to make sure output text is visible
st.markdown("""
    <style>
    .main {
        font-family: 'Poppins', sans-serif;
        padding: 15px;
    }

    .weather-title {
        font-size: 3em;
        text-align: center;
        margin-bottom: 20px;
        color: #2c3e50;
    }

    .stTextInput > div > div > input {
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 16px;
        color: #333333;  /* Dark text */
        background-color: #f8f9fa;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2980b9;
        box-shadow: 0 0 0 2px rgba(41,128,185,0.2);
    }

    .stButton > button {
        background-color: #2980b9;
        color: white;
        padding: 12px 25px;
        border-radius: 10px;
        width: 100%;
        border: none;
    }

    .stButton > button:hover {
        background-color: #8e44ad;
    }

    .weather-card {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        background-color: white;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }

    .output-text {
        color: black;
        font-size: 1.2em;
        text-align: center;
    }

    .metric {
        margin: 10px;
        text-align: center;
        font-size: 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 class='weather-title'>🌈 Weather Forecast</h1>", unsafe_allow_html=True)

# City input field
city = st.text_input("Enter a city name:", help="Type a city and press Enter")

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
            st.error("City not found! Please check the spelling.")
            return None

    except Exception as e:
        st.error("Unable to connect to weather service. Please try again later.")
        return None

if city:
    weather_data = get_weather(city)

    if weather_data:
        # Weather Card
        st.markdown("<div class='weather-card'>", unsafe_allow_html=True)

        # Greeting and Location
        st.markdown(f"<h2 class='output-text'>{get_time_greeting()}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 class='output-text'>📍 {city.title()}, {weather_data['sys']['country']}</h3>", unsafe_allow_html=True)

        # Weather Display
        main_weather = weather_data['weather'][0]['main']
        icon = get_weather_icon(main_weather)
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']

        st.markdown(f"""
            <div class='output-text'>
                <span style='font-size: 4em;'>{icon}</span>
                <h3>{temp}°C</h3>
                <p>{description.title()}</p>
            </div>
        """, unsafe_allow_html=True)

        # Weather Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='metric'><strong>Humidity</strong><br>{weather_data['main']['humidity']}%</div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='metric'><strong>Wind Speed</strong><br>{weather_data['wind']['speed']} m/s</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='metric'><strong>Feels Like</strong><br>{weather_data['main']['feels_like']}°C</div>", unsafe_allow_html=True)

        # Timestamp
        st.markdown(f"<p class='output-text'>Last updated: {datetime.now().strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # End Weather Card

# Footer
st.markdown("""
    <div class='output-text' style='text-align: center; padding: 10px; font-size: 0.8em;'>
        Powered by OpenWeatherMap API
    </div>
""", unsafe_allow_html=True)
