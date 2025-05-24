# 🌦️ Weather API with Flask, Redis & Visual Crossing

This project is a weather data API built using **Flask**. 
It fetches real-time weather data from the [Visual Crossing API](https://www.visualcrossing.com/), caches responses using **Redis**, and includes features **rate limiting**

---

## 🚀 Features

- ✅ `/weather?city=CityName` endpoint
- 🌤️ Live weather info via Visual Crossing
- ⚡ In-memory caching using Redis
- 🔐 Rate limiting with Flask-Limiter (100 requests/hour/IP)
- 🧪 Unit tests with `pytest` and `requests-mock`
- 🔧 `.env` for API keys and config management

---

## 📦 Tech Stack

- **Flask** (Web Framework)
- **Redis** (Cache)
- **Visual Crossing** (Weather API)
- **python-dotenv** (Env variable management)
- **Flask-Limiter** (Rate limiting)
- **Pytest** (Testing)

---

## ⚙️ Setup Instructions

### 1. 🔧 Clone the Repository

```
git clone https://github.com/shdh23/weather_api.git
cd weather-api
```

### 2. 📦 Install Dependencies
```pip install -r requirements.txt```

### 3. 📄 Create a .env File

```
WEATHER_API_KEY=your_visual_crossing_api_key
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_TTL=43200
```

### 4. 🧪 Running the App
Start Redis server (locally or using Docker):

```docker run -d --name redis -p 6379:6379 redis```

Then run Flask app:

```python app.py```

🔎 Example Request

```GET http://localhost:5000/weather?city=London```

✅ Sample Response
```{
  "city": "London",
  "date": "2025-05-23",
  "temp": 15,
  "description": "Partly Cloudy",
  "humidity": 78,
  "precip": 0,
  "wind": 12
}
```

