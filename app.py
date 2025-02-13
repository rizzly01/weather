import streamlit as st
import requests
from datetime import datetime

# Custom CSS with more modern styling
st.markdown("""
    <style>
    /* Main Container */
    .main {
        font-family: 'Poppins', sans-serif;
        padding: 15px;
    }

    /* Title Styles */
    .weather-title {
        background: linear-gradient(120deg, #2980b9, #8e44ad);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Search Box */
    .stTextInput > div > div > input {
        font-family: 'Poppins', sans-serif;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        background: #f8f9fa;
        font-size: 16px;
        transition: all 0.3s ease;
        color: #333333;  /* Dark color for input text */
    }

    .stTextInput > div > div > input::placeholder {
        color: #555555;  /* Light grey color for placeholder text */
    }

    .stTextInput > div > div > input:focus {
        border-color: #2980b9;
        box-shadow: 0 0 0 2px rgba(41,128,185,0.2);
    }

    /* Weather Card */
    .weather-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        margin: 20px 0;
        transition: transform 0.3s ease;
    }

    .weather-card:hover {
        transform: translateY(-5px);
    }

    /* Weather Metrics */
    .metric {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
    }

    .metric:hover {
        background: #e9ecef;
        transform: scale(1.02);
    }

    .metric-icon {
        font-size: 24px;
        margin-right: 10px;
    }

    /* Button Style */
    .stButton > button {
        background: linear-gradient(120deg, #2980b9, #8e44ad);
        color: white;
        padding: 12px 25px;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Alert Styles */
    .stAlert {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }

    /* Output Text Styling */
    .output-text {
        color: black;  /* Make the text black for visibility */
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<h1 class='weather-title'>🌈 Weather Wizard</h1>", unsafe_allow_html=True)

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

# City input with better styling
city = st.text_input("", placeholder="Enter your city name...", help="Type your city name and press Enter")

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
        # Weather card container
        st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
        
        # Greeting and location
        st.markdown(f"<h2 style='text-align: center;'>{get_time_greeting()}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #2c3e50;'>📍 {city.title()}, {weather_data['sys']['country']}</h3>", unsafe_allow_html=True)
        
        # Main weather display
        main_weather = weather_data['weather'][0]['main']
        icon = get_weather_icon(main_weather)
        temp = weather_data['main']['temp']
        st.markdown(f"""
            <div style='text-align: center; padding: 20px;' class="output-text">
                <span style='font-size: 5em;'>{icon}</span>
                <h2 style='font-size: 3em; margin: 0;'>{temp}°C</h2>
                <p style='font-size: 1.5em; color: #696;'>{weather_data['weather'][0]['description'].title()}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class='metric'>
                    <span class='metric-icon'>💧</span>
                    <div>
                        <strong>Humidity</strong><br>
                        {weather_data['main']['humidity']}%
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div class='metric'>
                    <span class='metric-icon'>🌡️</span>
                    <div>
                        <strong>Feels Like</strong><br>
                        {weather_data['main']['feels_like']}°C
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
                <div class='metric'>
                    <span class='metric-icon'>💨</span>
                    <div>
                        <strong>Wind Speed</strong><br>
                        {weather_data['wind']['speed']} m/s
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # Additional metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class='metric'>
                    <span class='metric-icon'>⬆️</span>
                    <div>
                        <strong>Max Temp</strong><br>
                        {weather_data['main']['temp_max']}°C
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div class='metric'>
                    <span class='metric-icon'>⬇️</span>
                    <div>
                        <strong>Min Temp</strong><br>
                        {weather_data['main']['temp_min']}°C
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Timestamp
        st.markdown(f"""
            <div style='text-align: center; color: #666; padding: 10px;' class="output-text">
                Last updated: {datetime.now().strftime('%I:%M %p')}
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px; font-size: 0.8em;' class="output-text">
        Powered by OpenWeatherMap API<br>
    </div>
""", unsafe_allow_html=True)
