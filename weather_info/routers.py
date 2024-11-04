from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.database import get_db
from weather_info.schemas import WeatherRequestSchema, WeatherResponseSchema
from weather_info.service import fetch_or_store_location, get_weather_data

weather_info_router = APIRouter()

@weather_info_router.post("/fetch_weather_report", response_model=WeatherResponseSchema)
async def get_weather_info(request: WeatherRequestSchema, db: Session = Depends(get_db)):
    try:
        # Fetch or compute latitude and longitude for the pincode
        location = fetch_or_store_location(request.pincode, db) 

        # Get weather data for the specified date
        weather_data = get_weather_data(lat=location.latitude, lon=location.longitude, location_id=location.id, for_date=request.for_date, db=db)

        # Structure the response
        response = WeatherResponseSchema(
            pincode=request.pincode,
            date=request.for_date,
            lat=location.latitude,
            lon=location.longitude,
            weather=weather_data["weather"],
            main=weather_data["main"],
            wind=weather_data["wind"],
            visibility=weather_data.get("visibility"),
            clouds=weather_data["clouds"],
            sunrise=weather_data["sunrise"],
            sunset=weather_data["sunset"]
        )
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching weather information. {str(e)}")