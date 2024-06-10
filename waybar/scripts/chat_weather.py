#!/usr/bin/env python

import json
import requests
from datetime import datetime
from typing import Dict, List

WEATHER_CODES = {
    '113': '🌈',
    '116': '⛅️',
    '119': '☁️',
    '122': '☁️',
    '143': '🌫',
    '176': '🌦',
    '179': '🌧',
    '182': '🌧',
    '185': '🌧',
    '200': '⛈',
    '227': '🌨',
    '230': '❄️',
    '248': '🌫',
    '260': '🌫',
    '263': '🌦',
    '266': '🌦',
    '281': '🌧',
    '284': '🌧',
    '293': '🌦',
    '296': '🌦',
    '299': '🌧',
    '302': '🌧',
    '305': '🌧',
    '308': '🌧',
    '311': '🌧',
    '314': '🌧',
    '317': '🌧',
    '320': '🌨',
    '323': '🌨',
    '326': '🌨',
    '329': '❄️',
    '332': '❄️',
    '335': '❄️',
    '338': '❄️',
    '350': '🌧',
    '353': '🌦',
    '356': '🌧',
    '359': '🌧',
    '362': '🌧',
    '365': '🌧',
    '368': '🌨',
    '371': '❄️',
    '374': '🌧',
    '377': '🌧',
    '386': '⛈',
    '389': '🌩',
    '392': '⛈',
    '395': '❄️'
}

def fetch_weather_data(url: str) -> Dict:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}

def format_time(time: str) -> str:
    return time.replace("00", "").zfill(2)

def format_temp(temp: str) -> str:
    return (temp + "°").ljust(3)

def format_chances(hour: Dict) -> str:
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }
    conditions = [f"{event} {hour[event]}%" for event in chances if int(hour[event]) > 0]
    return ", ".join(conditions)

def build_tooltip(weather: Dict) -> str:
    tooltip = f"<b>Now:</b>\n"
    current = weather['current_condition'][0]
    tooltip += f"{current['weatherDesc'][0]['value']}\n"
    tooltip += f"Feels like: {current['FeelsLikeC']}°C\n"
    tooltip += f"Wind: {current['windspeedKmph']} Km/h\n"
    tooltip += f"Humidity: {current['humidity']}%\n"
    
    for i, day in enumerate(weather['weather']):
        tooltip += f"\n<b>{['Today', 'Tomorrow', 'Day After'][i]}, {day['date']}</b> "
        tooltip += f"󰖜 {day['astronomy'][0]['sunrise']} 󰖛 {day['astronomy'][0]['sunset']}\n"
        tooltip += f"󰸃 {day['maxtempC']}° 󰸂 {day['mintempC']}°\n"
        
        for hour in day['hourly']:
            if i == 0 and int(format_time(hour['time'])) < datetime.now().hour - 2:
                continue
            tooltip += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"
    
    return tooltip

def main():
    url = "https://wttr.in/?format=j1"
    weather = fetch_weather_data(url)
    
    if not weather:
        return

    current = weather['current_condition'][0]
    data = {
        'text': WEATHER_CODES[current['weatherCode']] + " " + current['FeelsLikeC'] + "°",
        'tooltip': build_tooltip(weather)
    }

    print(json.dumps(data))

if __name__ == "__main__":
    main()

