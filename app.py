from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


from services.cache_service import get_cached_weather, set_cached_weather
from services.weather_service import fetch_weather_from_api

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)



# initialize Flask app
app = Flask(__name__)
load_dotenv()

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]
)


# Define route
@limiter.limit("100 per hour")
@app.route('/weather', methods=['GET'])
def get_weather():
    # Get query parameters
    city = request.args.get('city')

    # Check if parameters are provided
    if not city:
        logging.warning("Missing or empty 'city' parameter")
        return jsonify({"error": "Please provide both city."}), 400
    
    
    try:
        # Check cache
        cached = get_cached_weather(city)
        if cached:
            logging.info(f"Cache hit for city: {city}")
            return jsonify(json.loads(cached)), 200

        # Fetch from external API
        logging.info(f"Cache miss for city: {city}. Fetching from API...")
        weather_info = fetch_weather_from_api(city)

        # Save to cache
        set_cached_weather(city, weather_info)

        return jsonify(weather_info), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)