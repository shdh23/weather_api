import pytest
from unittest.mock import patch, MagicMock
import os
import sys
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set a dummy API key for test environment
os.environ["WEATHER_API_KEY"] = "test_key"

from services.weather_service import fetch_weather_from_api

# --- Test: Successful API response ---
@patch('services.weather_service.requests.get')
def test_fetch_weather_success(mock_get):
    # Mock response JSON
    mock_data = {
        "days": [
            {
                "datetime": "2025-05-23",
                "temp": 25,
                "description": "Sunny",
                "humidity": 40,
                "precip": 0,
                "windspeed": 12
            }
        ]
    }

    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mock_get.return_value = mock_response

    result = fetch_weather_from_api("TestCity")

    assert result["city"] == "TestCity"
    assert result["date"] == "2025-05-23"
    assert result["temp"] == 25
    assert result["description"] == "Sunny"
    assert result["humidity"] == 40
    assert result["precip"] == 0
    assert result["wind"] == 12

    mock_get.assert_called_once_with(
        'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/TestCity?key=test_key&unitGroup=metric',
        timeout=5
    )

# --- Test: API request exception ---
@patch('services.weather_service.requests.get')
def test_fetch_weather_request_exception(mock_get):
    mock_get.side_effect = requests.RequestException("Connection error")

    with pytest.raises(Exception) as exc_info:
        fetch_weather_from_api("Nowhere")

    assert "Weather service unavailable" in str(exc_info.value)

# --- Test: Bad response structure ---
@patch('services.weather_service.requests.get')
def test_fetch_weather_bad_response_format(mock_get):
    # Missing "days" key
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"unexpected": "structure"}
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as exc_info:
        fetch_weather_from_api("BadCity")

    assert "Invalid response format" in str(exc_info.value)
