import requests
import matplotlib.pyplot as plt
from datetime import datetime

API_KEY = '7136d46d4edf4c9bbcf124053242205'
BASE_URL = 'http://api.weatherapi.com/v1/'

def get_weather_data(city):
    current_weather_url = f"{BASE_URL}current.json?key={API_KEY}&q={city}"
    forecast_url = f"{BASE_URL}forecast.json?key={API_KEY}&q={city}&days=5"
    
    current_weather_response = requests.get(current_weather_url)
    forecast_response = requests.get(forecast_url)
    
    if current_weather_response.status_code == 200 and forecast_response.status_code == 200:
        current_weather = current_weather_response.json()
        forecast = forecast_response.json()
        return current_weather, forecast
    else:
        print(f"Error fetching weather data. Status codes: {current_weather_response.status_code}, {forecast_response.status_code}")
        if current_weather_response.status_code != 200:
            print(f"Current weather response: {current_weather_response.text}")
        if forecast_response.status_code != 200:
            print(f"Forecast response: {forecast_response.text}")
        return None, None

def display_current_weather(current_weather):
    print("Current Weather:")
    location = current_weather['location']
    current = current_weather['current']
    print(f"Location: {location['name']}, {location['country']}")
    print(f"Temperature: {current['temp_c']}°C")
    print(f"Weather: {current['condition']['text']}")
    print(f"Humidity: {current['humidity']}%")
    print(f"Wind Speed: {current['wind_kph']} kph")
    print("-" * 40)

def display_forecast(forecast):
    print("5-Day Forecast:")
    forecast_days = forecast['forecast']['forecastday']
    for day in forecast_days:
        date = day['date']
        day_info = day['day']
        temp = day_info['avgtemp_c']
        weather = day_info['condition']['text']
        print(f"{date}: {temp}°C, {weather}")
    print("-" * 40)

def plot_temperature_trends(forecast):
    dates = []
    temps = []

    forecast_days = forecast['forecast']['forecastday']
    for day in forecast_days:
        date = datetime.strptime(day['date'], '%Y-%m-%d')
        temp = day['day']['avgtemp_c']
        dates.append(date)
        temps.append(temp)
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o', linestyle='-', color='b')
    plt.title('Temperature Trends Over Next 5 Days')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()

def main():
    city = input("Enter the city name: ")
    current_weather, forecast = get_weather_data(city)
    
    if current_weather and forecast:
        display_current_weather(current_weather)
        display_forecast(forecast)
        plot_temperature_trends(forecast)
    else:
        print("Could not retrieve weather data.")

if __name__ == "__main__":
    main()
