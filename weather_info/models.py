from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from utils.database import Base


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, index=True)
    pincode = Column(String, unique=True, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=func.now())

    # Relationship to access weather data from Location
    weather_data = relationship("WeatherData", back_populates="location")

    def __repr__(self):
        return f"<Location(pincode={self.pincode}, latitude={self.latitude}, longitude={self.longitude})>"

class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    for_date = Column(Date, nullable=False)
    temperature = Column(Float, nullable=False)  # Current temperature in Celsius
    feels_like = Column(Float, nullable=False)  # Feels like temperature in Celsius
    temp_min = Column(Float, nullable=False)     # Minimum temperature in Celsius
    temp_max = Column(Float, nullable=False)     # Maximum temperature in Celsius
    pressure = Column(Integer, nullable=False)   # Atmospheric pressure in hPa
    humidity = Column(Integer, nullable=False)    # Humidity percentage
    visibility = Column(Integer, nullable=False)    #Visibility
    sunrise = Column(String, nullable=False)       #Sunrise Time
    sunset = Column(String, nullable=False)         #Sunset Time
    wind_speed = Column(Float, nullable=False)    # Wind speed in m/s
    wind_deg = Column(Integer, nullable=True)     # Wind direction in degrees
    rain_1h = Column(Float, nullable=True)         # Rain volume in the last 1 hour
    clouds_all = Column(Integer, nullable=False)   # Cloudiness percentage
    weather_main = Column(String, nullable=False)   # Main weather condition
    weather_desc = Column(String, nullable=False)   # Weather condition description
    icon = Column(String, nullable=True)            # Weather icon code
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    # Relationship to access Location from WeatherData
    location = relationship("Location", back_populates="weather_data")

    def __repr__(self):
        return f"<WeatherData(for_date={self.for_date}, temperature={self.temperature}, location_id={self.location_id})>"

