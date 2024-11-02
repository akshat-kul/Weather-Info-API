# Weather Info API 🌦️

## Overview
This Weather Info API is a REST API that allows users to retrieve weather information based on a **pincode** and a **specific date**. It caches data to optimize API calls, fetching data only when needed from external sources. The primary data sources are the **OpenWeatherMap API** (for weather data and geocoding).

## Features
- Fetch weather info based on **pincode** and **date**
- Convert **pincode to latitude/longitude** using OpenWeatherMap Geocoding API
- Cache weather info in a relational database to avoid redundant API calls
- Exposes a **single REST API endpoint** for weather retrieval
- Easily testable via **Postman** or **Swagger** (FastAPI provides automatic documentation)

## Tech Stack
- **FastAPI** - Framework for building the REST API
- **PostgreSQL/MySQL** - Relational database to store location and weather info
- **SQLAlchemy** - ORM for database management
- **OpenWeatherMap API** - Weather data and geocoding
- **Docker** (optional) - For containerizing the application

## Installation 🛠️

Follow these steps to get the project up and running on your local machine.

### Prerequisites
1. **Python 3.8+**
2. **Database**: PostgreSQL or MySQL
3. **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api) to get your API key.

### Steps

1. **Clone the Repository**
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/weather-info-api.git
   cd weather-info-api
   ```
2. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Environment Variables
   ```bash
   OPENWEATHER_API_KEY=your_openweather_api_key
   DATABASE_URL=postgresql://username:password@localhost/weather_db
   ```
4. Run the Server
   ```bash
   python main.py
   ```
