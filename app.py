import streamlit as st
import requests

# Custom CSS styling
st.markdown("""
    <style>
    .title {
        color: #2c3e50;
        text-align: center;
        padding: 20px;
        font-size: 3em;
        font-weight: bold;
    }
    
    .weather-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .metric {
        font-size: 1.2em;
        color: #34495e;
        margin: 10px 0;
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    
    .stButton > button {
        background-color: #3498db;
        color: white;
        width: 100%;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title'>📍 Weather Checker</h1>", unsafe_allow_html=True)

# Input for city name
city = st.text_input("Enter City Name", placeholder="Example: London")

# Your API key (replace with your actual API key)
API_KEY = "57e00c15d85b13d67a6f52afdd0f3377"  # Replace this with your OpenWeatherMap API key

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            return data
        else:
            st.error("City not found! Please check the spelling.")
            return None
            
    except Exception as e:
        st.error("Something went wrong! Please try again.")
        return None

# Button to get weather
if st.button("Check Weather") and city:
    weather_data = get_weather(city)
    
    if weather_data:
        # Display weather information
        st.markdown("<div class='weather-info'>", unsafe_allow_html=True)
        
        # City name and country
        country = weather_data['sys']['country']
        st.markdown(f"<h2 style='text-align: center;'>Weather in {city}, {country}</h2>", unsafe_allow_html=True)
        
        # Create two columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature
            temp = weather_data['main']['temp']
            st.markdown(f"<div class='metric'>🌡️ Temperature: {temp}°C</div>", unsafe_allow_html=True)
            
            # Weather description
            description = weather_data['weather'][0]['description']
            st.markdown(f"<div class='metric'>☁️ Condition: {description.title()}</div>", unsafe_allow_html=True)
            
        with col2:
            # Humidity
            humidity = weather_data['main']['humidity']
            st.markdown(f"<div class='metric'>💧 Humidity: {humidity}%</div>", unsafe_allow_html=True)
            
            # Wind Speed
            wind_speed = weather_data['wind']['speed']
            st.markdown(f"<div class='metric'>🌪️ Wind: {wind_speed} m/s</div>", unsafe_allow_html=True)
            
        # Additional info
        feels_like = weather_data['main']['feels_like']
        st.markdown(f"<div class='metric'>🌡️ Feels like: {feels_like}°C</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
elif city:
    st.info("Please enter a city name to check the weather!")

# Footer
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        Weather data provided by OpenWeatherMap
    </div>
""", unsafe_allow_html=True)
