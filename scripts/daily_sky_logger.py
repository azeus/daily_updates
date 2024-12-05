import requests
import os
import json
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import urlparse

# API Endpoints
SUNRISE_SUNSET_API = "https://api.sunrise-sunset.org/json"
OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"
WEBCAM_WORLD_URL = "https://www.webcams.travel/map"

# Function to generate random latitude and longitude
def get_random_coordinates():
    latitude = random.uniform(-90, 90)  # Random latitude
    longitude = random.uniform(-180, 180)  # Random longitude
    return latitude, longitude

# Function to fetch sunrise and sunset times
def fetch_sunrise_sunset(lat, lon):
    params = {
        "lat": lat,
        "lng": lon,
        "formatted": 0  # Return ISO 8601 format
    }
    response = requests.get(SUNRISE_SUNSET_API, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", {})
        return {
            "sunrise": results.get("sunrise"),
            "sunset": results.get("sunset")
        }
    else:
        print("Failed to fetch sunrise and sunset times.")
        return {}

# Function to fetch cloud cover for astronomical visibility
def fetch_night_sky_conditions(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "cloudcover",
        "timezone": "auto"
    }
    response = requests.get(OPEN_METEO_API, params=params)
    if response.status_code == 200:
        data = response.json()
        hourly_data = data.get("hourly", {}).get("cloudcover", [])
        return hourly_data[:12]  # Return next 12 hours of cloud cover
    else:
        print("Failed to fetch night sky conditions.")
        return []



def fetch_webcam_image(lat, lon):
    params = {
        "lat": lat,
        "lon": lon
    }
    response = requests.get(WEBCAM_WORLD_URL, params=params)
    if response.status_code == 200:
        html = response.text
        # Extract potential URL using simple string matching
        start = html.find("img src=") + len("img src=")
        end = html.find('"', start)
        image_url = html[start:end]

        # Validate the extracted URL
        if image_url and urlparse(image_url).scheme in ["http", "https"]:
            return image_url
        else:
            print("Invalid image URL found.")
            return None
    else:
        print("Failed to fetch webcam image.")
        return None

# Function to overlay data on an image
def overlay_text_on_image(image_url, text, output_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open("temp_image.jpg", "wb") as temp_file:
            temp_file.write(response.content)
        img = Image.open("temp_image.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((10, 10), text, fill="white", font=font)
        img.save(output_path)
        print(f"Image saved with overlay: {output_path}")
        os.remove("temp_image.jpg")
    else:
        print("Failed to download webcam image.")

# Main function
if __name__ == "__main__":
    # Generate random coordinates
    lat, lon = get_random_coordinates()
    print(f"Random Coordinates: Latitude {lat}, Longitude {lon}")

    # Fetch data
    sunrise_sunset = fetch_sunrise_sunset(lat, lon)
    night_sky_conditions = fetch_night_sky_conditions(lat, lon)
    webcam_image_url = fetch_webcam_image(lat, lon)

    # Log data
    log_data = {
        "date": datetime.utcnow().isoformat(),
        "coordinates": {"latitude": lat, "longitude": lon},
        "sunrise": sunrise_sunset.get("sunrise"),
        "sunset": sunrise_sunset.get("sunset"),
        "night_sky_conditions": night_sky_conditions
    }
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/sky_log_{datetime.utcnow().strftime('%Y-%m-%d')}.json", "w") as log_file:
        json.dump(log_data, log_file, indent=4)
    print("Daily log saved.")

    # Generate images
    os.makedirs("results", exist_ok=True)
    if webcam_image_url:
        # Sunrise Image
        sunrise_text = f"Coordinates: {lat:.2f}, {lon:.2f}\nSunrise: {sunrise_sunset.get('sunrise')}"
        overlay_text_on_image(webcam_image_url, sunrise_text, f"results/sunrise_image_{datetime.utcnow().strftime('%Y-%m-%d')}.jpg")

        # Sunset Image
        sunset_text = f"Coordinates: {lat:.2f}, {lon:.2f}\nSunset: {sunrise_sunset.get('sunset')}"
        overlay_text_on_image(webcam_image_url, sunset_text, f"results/sunset_image_{datetime.utcnow().strftime('%Y-%m-%d')}.jpg")

        # Night Sky Image
        night_text = f"Coordinates: {lat:.2f}, {lon:.2f}\nNight Sky Visibility (Cloud Cover %): {night_sky_conditions[:3]}"
        overlay_text_on_image(webcam_image_url, night_text, f"results/night_sky_image_{datetime.utcnow().strftime('%Y-%m-%d')}.jpg")
    else:
        print("No webcam image available for the selected location.")