from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List, Optional, Union

# Request schema to validate incoming data
class WeatherRequestSchema(BaseModel):
    pincode: Union[int, str] = Field(..., description="6-digit Indian pincode")
    for_date: str = Field(..., description="Date for weather information in YYYY-MM-DD format")

    @field_validator("pincode")
    def validate_pincode(cls, value):
        # Convert integer pincode to string for validation
        value_str = str(value)
        
        # Check if it's a 6-digit pincode
        if not value_str.isdigit() or len(value_str) != 6:
            raise ValueError("Pincode must be a 6-digit number.")
        
        return value_str  # Return as string if valid
# Response schema to structure the weather data
class WeatherDataSchema(BaseModel):
    description: str
    icon: str
    main: str

class MainWeatherSchema(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int

class WindSchema(BaseModel):
    speed: float
    deg: int

class WeatherResponseSchema(BaseModel):
    pincode: str
    date: date
    lat: float
    lon: float
    weather: List[WeatherDataSchema]
    main: MainWeatherSchema
    wind: WindSchema
    visibility: int
    clouds: Optional[int] = None
    sunrise: str
    sunset: str

    class Config:
        json_schema_extra = {
            "example": {
                "pincode": "411014",
                "date": "2020-10-15",
                "lat": 45.133,
                "lon": 7.367,
                "weather": [
                    {"description": "moderate rain", "icon": "10d", "main": "Rain"}
                ],
                "main": {
                    "temp": 284.2,
                    "feels_like": 282.93,
                    "temp_min": 283.06,
                    "temp_max": 286.82,
                    "pressure": 1021,
                    "humidity": 60
                },
                "wind": {"speed": 4.09, "deg": 121},
                "visibility": 10000,
                "clouds": 83,
                "sunrise": 1726636384,
                "sunset": 1726680975
            }
        }
