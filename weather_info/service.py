from datetime import datetime, timedelta, timezone
import requests
from sqlalchemy.orm import Session
from .models import Location, WeatherData  
from config.settings import settings

def fetch_or_store_location(pincode: str, db: Session) -> Location:
    # Check if location for this pincode already exists in the database
    location = db.query(Location).filter(Location.pincode == pincode).first()
    
    if location:
        # Location already exists, so return it
        return location

    # If not, fetch the coordinates using an external API
    try:
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={pincode},IN&appid={settings.open_weather_map_api_key}"
        response = requests.get(geocoding_url)
        
        if response.status_code != 200:
            raise Exception("Failed to fetch location data")
        
        location_data = response.json()
        
        # Extract latitude and longitude
        lat = location_data.get("lat")
        lon = location_data.get("lon")

        if lat is None or lon is None:
            raise ValueError("Latitude or Longitude not found in API response")

        # Store the new location in the database
        new_location = Location(
            pincode=pincode,
            latitude=lat,
            longitude=lon
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)

        return new_location

    except Exception as e:
        print(f"Error fetching or storing location data: {e}")
        raise


def format_weather_data(weather_record) -> dict:
    # Helper function to format weather data as a dictionary
    return {
        "main": {
            "temp": weather_record.temperature,
            "feels_like": weather_record.feels_like,
            "temp_min": weather_record.temp_min,
            "temp_max": weather_record.temp_max,
            "pressure": weather_record.pressure,
            "humidity": weather_record.humidity
        },
        "weather": [{
            "description": weather_record.weather_desc,
            "icon": weather_record.icon,
            "main": weather_record.weather_main
        }],
        "wind": {
            "speed": weather_record.wind_speed,
            "deg": weather_record.wind_deg
        },
        "visibility": weather_record.visibility,
        "sunrise": weather_record.sunrise,
        "sunset": weather_record.sunset,
        "clouds": weather_record.clouds_all,
        "rain_1h": weather_record.rain_1h
    }


def get_weather_data(lat: float, lon: float, location_id: int, for_date: str, db: Session) -> dict:
    # Check if weather data for this location and date already exists in the database
    weather_record = db.query(WeatherData).filter(
        WeatherData.location_id == location_id,
        WeatherData.for_date == for_date
    ).first()

    if weather_record:
        # Return formatted data if record exists
        return format_weather_data(weather_record)

    # Fetch new weather data from the API
    api_key = settings.open_weather_map_api_key
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch weather data")
    
    weather_data = response.json()

    # Convert sunrise and sunset to IST timezone
    def to_ist(timestamp: int) -> str:
        return (datetime.fromtimestamp(timestamp, tz=timezone.utc) + timedelta(hours=5, minutes=30)).strftime('%b %d, %Y, %I:%M:%S %p')

    new_weather_record = WeatherData(
        location_id=location_id,
        for_date=for_date,
        temperature=weather_data["main"]["temp"],
        feels_like=weather_data["main"]["feels_like"],
        temp_min=weather_data["main"]["temp_min"],
        temp_max=weather_data["main"]["temp_max"],
        pressure=weather_data["main"]["pressure"],
        humidity=weather_data["main"]["humidity"],
        wind_speed=weather_data["wind"]["speed"],
        wind_deg=weather_data["wind"].get("deg"),
        rain_1h=weather_data.get("rain", {}).get("1h"),
        clouds_all=weather_data["clouds"]["all"],
        weather_main=weather_data["weather"][0]["main"],
        weather_desc=weather_data["weather"][0]["description"],
        icon=weather_data["weather"][0]["icon"],
        visibility=weather_data.get("visibility"),
        sunrise=to_ist(weather_data["sys"]["sunrise"]),
        sunset=to_ist(weather_data["sys"]["sunset"]),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    db.add(new_weather_record)
    db.commit()
    db.refresh(new_weather_record)

    # Return formatted data for the newly added record
    return format_weather_data(new_weather_record)