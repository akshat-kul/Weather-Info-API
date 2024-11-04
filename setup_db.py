# setup_db.py
from utils.database import Base, engine
from weather_info.models import Location, WeatherData  # import all models

# Create all tables
Base.metadata.create_all(bind=engine)
