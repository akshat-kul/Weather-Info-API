import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from weather_info.models import WeatherData
from weather_info.service import get_weather_data

# Helper function to create a mock WeatherData record
def create_mock_weather_record(location_id, for_date):
    return WeatherData(
        location_id=location_id,
        for_date=for_date,
        temperature=25.0,
        feels_like=24.0,
        temp_min=22.0,
        temp_max=27.0,
        pressure=1013,
        humidity=78,
        wind_speed=3.6,
        wind_deg=180,
        rain_1h=0.0,
        clouds_all=0,
        weather_main="Clear",
        weather_desc="clear sky",
        icon="01d",
        visibility=10000,
        sunrise="Sep 18, 2024, 05:13:04 AM",
        sunset="Sep 18, 2024, 06:13:04 PM",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@pytest.fixture
def db_session():
    # Create a mock SQLAlchemy session
    return Mock(spec=Session)

@pytest.fixture
def api_response():
    # Sample API response data
    return {
        "main": {
            "temp": 25.0,
            "feels_like": 24.0,
            "temp_min": 22.0,
            "temp_max": 27.0,
            "pressure": 1013,
            "humidity": 78
        },
        "weather": [
            {
                "description": "clear sky",
                "icon": "01d",
                "main": "Clear"
            }
        ],
        "wind": {
            "speed": 3.6,
            "deg": 180
        },
        "visibility": 10000,
        "clouds": {"all": 0},
        "sys": {
            "sunrise": int((datetime.now(timezone.utc) - timedelta(hours=5, minutes=30)).timestamp()),
            "sunset": int((datetime.now(timezone.utc) - timedelta(hours=5, minutes=30) + timedelta(hours=12)).timestamp())
        }
    }

@patch("weather_service.requests.get")  # Mock the requests.get call in your module
def test_get_weather_data_existing_record(mock_get, db_session):
    # Test with existing data in the database
    location_id = 1
    for_date = "2024-09-18"
    
    # Mock the database query to return an existing weather record
    mock_weather_record = create_mock_weather_record(location_id, for_date)
    db_session.query.return_value.filter.return_value.first.return_value = mock_weather_record

    # Call the function
    weather_data = get_weather_data(lat=28.7041, lon=77.1025, location_id=location_id, for_date=for_date, db=db_session)

    # Assertions
    assert weather_data["main"]["temp"] == 25.0
    assert weather_data["weather"][0]["description"] == "clear sky"
    mock_get.assert_not_called()  # Ensure API was not called since record exists in DB

@patch("weather_service.requests.get")
def test_get_weather_data_new_record(mock_get, db_session, api_response):
    # Test with no existing data, so it should fetch from API
    location_id = 1
    for_date = "2024-09-18"
    
    # Mock the database query to return None, simulating no existing record
    db_session.query.return_value.filter.return_value.first.return_value = None
    
    # Mock the API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = api_response

    # Call the function
    weather_data = get_weather_data(lat=28.7041, lon=77.1025, location_id=location_id, for_date=for_date, db=db_session)

    # Assertions
    assert weather_data["main"]["temp"] == api_response["main"]["temp"]
    assert weather_data["weather"][0]["description"] == api_response["weather"][0]["description"]
    assert "sunrise" in weather_data
    assert "sunset" in weather_data
    mock_get.assert_called_once()  # Ensure API was called since record was not in DB

@patch("weather_service.requests.get")
def test_get_weather_data_api_failure(mock_get, db_session):
    # Test API failure handling
    location_id = 1
    for_date = "2024-09-18"
    
    # Mock the database to return None
    db_session.query.return_value.filter.return_value.first.return_value = None
    
    # Mock a failed API response
    mock_get.return_value.status_code = 500

    with pytest.raises(Exception, match="Failed to fetch weather data"):
        get_weather_data(lat=28.7041, lon=77.1025, location_id=location_id, for_date=for_date, db=db_session)

    mock_get.assert_called_once()  # Ensure API was called and failed
