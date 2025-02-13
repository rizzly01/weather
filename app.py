import streamlit as st
import requests

# Custom CSS styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 20px;
        border-radius: 10px;
    }
    
    /* Title styling */
    .title {
        color: #2c3e50;
        text-align: center;
        padding: 20px;
        font-size: 3em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Weather info container */
    .weather-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    /* Weather metrics styling */
    .metric {
        font-size: 1.2em;
        color: #34495e;
        margin: 10px 0;
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input {
        background-color: #f8f9fa;
        border: 2px solid #ddd;
        padding: 10px;
        border-radius: 5px;
        color: #2c3e50;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3498db;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Error and warning messages */
    .stAlert {
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title with custom class
st.markdown("<h1 class='title'>✨ Weather App ✨</h1>", unsafe_allow_html=True)

# Create columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    # Input for API key
    api_key = st.text_input("57e00c15d85b13d67a6f52afdd0f3377", type="password")

with col2:
    # Input for city name
    city = st.text_input("Enter City Name")

# Function to get weather data
def get_weather(city, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        
        if response.status_code == 200:
            return data
        else:
            st.error("Error fetching weather data. Please check your city name.")
            return None
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Button to get weather
if st.button("Get Weather"):
    if api_key and city:
        # Get weather data
        weather_data = get_weather(city, api_key)
        
        if weather_data:
            # Display weather information in a container
            st.markdown("<div class='weather-info'>", unsafe_allow_html=True)
            
            # City name with emoji
            st.markdown(f"<h2 style='text-align: center; color: #2c3e50;'>🌍 Weather in {city}</h2>", unsafe_allow_html=True)
            
            # Create two columns for weather info
            col1, col2 = st.columns(2)
            
            with col1:
                # Temperature with emoji
                temp = weather_data['main']['temp']
                st.markdown(f"<div class='metric'>🌡️ Temperature: {temp}°C</div>", unsafe_allow_html=True)
                
                # Weather description with emoji
                description = weather_data['weather'][0]['description']
                st.markdown(f"<div class='metric'>☁️ Description: {description.title()}</div>", unsafe_allow_html=True)
            
            with col2:
                # Humidity with emoji
                humidity = weather_data['main']['humidity']
                st.markdown(f"<div class='metric'>💧 Humidity: {humidity}%</div>", unsafe_allow_html=True)
                
                # Wind Speed with emoji
                wind_speed = weather_data['wind']['speed']
                st.markdown(f"<div class='metric'>🌪️ Wind Speed: {wind_speed} m/s</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.warning("Please enter both API key and city name")

# Footer
st.markdown("""
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        Made with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)
