import requests
import pandas as pd
from datetime import datetime
import os
import time

# --- 1. CONFIGURATION ---
# Use the Key starting with 'qxI9...' from your screenshot
WEATHER_KEY = "b6612e5cf066f9f4863f67e19177f9c9"
TOMTOM_KEY = "qxI92nsuogy3Df6EScUC2v8PDywNO4g6"  # REPLACE THIS with your FULL COPIED KEY
LAT, LON = 12.9716, 77.5946
FILE_NAME = "city_data.csv"


def get_weather():
    """Fetches humidity from OpenWeatherMap"""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={WEATHER_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['main']['humidity']
        else:
            print(f"Weather API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Weather Connection Error: {e}")
        return None


def get_traffic():
    """Fetches real-time traffic speed from TomTom"""
    # Important: No spaces in the point parameter
    point = f"{LAT},{LON}"
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?key={TOMTOM_KEY}&point={point}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['flowSegmentData']['currentSpeed']
        else:
            # This captures the 403 error if the key is still activating
            print(f"Traffic API Error: {response.status_code} - {response.reason}")
            return None
    except Exception as e:
        print(f"Traffic Connection Error: {e}")
        return None


def save_to_log(humidity, speed):
    """Saves the data point to a CSV file for future analysis"""
    new_data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Humidity": humidity,
        "Traffic_Speed_KMH": speed
    }

    df = pd.DataFrame([new_data])

    # If file doesn't exist, create it with headers. If it does, append without headers.
    if not os.path.isfile(FILE_NAME):
        df.to_csv(FILE_NAME, index=False)
    else:
        df.to_csv(FILE_NAME, mode='a', header=False, index=False)

    print(f"✅ Data Logged: {new_data}")


# --- 2. EXECUTION LOOP ---
if __name__ == "__main__":
    print("🚀 Starting City Pulse Data Collection...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            h = get_weather()
            s = get_traffic()

            save_to_log(h, s)

            # Wait 5 minutes (300 seconds) before the next pulse
            # This keeps you safely within the FREE TIER limits
            print("💤 Sleeping for 5 minutes...")
            time.sleep(300)

    except KeyboardInterrupt:
        print("\nStopping collection. Your data is saved in 'city_data.csv'.")