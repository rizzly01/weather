import streamlit as st
import requests

# Function to get weather data
def get_weather(city, api_key):
    # OpenWeatherMap API URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    # Send request to the OpenWeatherMap API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Error if city not found
        st.error("City not found or there was an issue fetching the data.")
        return None

# Streamlit app layout
st.title("Weather App")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #4CAF50;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
        }
        .weather-info {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .weather-info h3 {
            color: #333;
        }
        .weather-info p {
            font-size: 18px;
            color: #555;
        }
        .error-message {
            color: red;
            font-weight: bold;
        }
        .input-box {
            margin-bottom: 20px;
        }
        .city-input {
            width: 300px;
            padding: 10px;
            font-size: 18px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
    </style>
""", unsafe_allow_html=True)

# Input for the city
city = st.text_input("Enter the city name:", "")

# API Key (Replace 'your_api_key' with your actual OpenWeatherMap API key)
api_key = "5b99e0b82d756d68fd1f5523ad5d15eb"

# Show weather details if the city is entered
if city:
    weather_data = get_weather(city, api_key)
    
    # Display weather data if the response is valid
    if weather_data:
        st.markdown(f'<div class="weather-info">', unsafe_allow_html=True)
        st.markdown(f'<h3>Weather in {city}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p>Temperature: {weather_data["main"]["temp"]}°C</p>', unsafe_allow_html=True)
        st.markdown(f'<p>Humidity: {weather_data["main"]["humidity"]}%</p>', unsafe_allow_html=True)
        st.markdown(f'<p>Weather: {weather_data["weather"][0]["description"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p>Wind Speed: {weather_data["wind"]["speed"]} m/s</p>', unsafe_allow_html=True)
        st.markdown(f'</div>', unsafe_allow_html=True)

# Display error message if city is not found or an error occurs
if city and not weather_data:
    st.markdown('<p class="error-message">City not found or there was an issue fetching the data.</p>', unsafe_allow_html=True)
