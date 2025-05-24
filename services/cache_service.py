import redis
import json
import os
from dotenv import load_dotenv
import logging


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')
redis_TTL = os.getenv('REDIS_TTL')

# Initialize Redis client
redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

def get_cached_weather(city):
    try:
        redis_key = f"weather:{city.lower()}"
        return redis_client.get(redis_key)
    except redis.RedisError as e:
        logging.error(f"[Redis GET error] {e}")
        return None

def set_cached_weather(city, data):
    try:
        redis_key = f"weather:{city.lower()}"
        redis_client.set(redis_key, json.dumps(data), ex=redis_TTL)
    except redis.RedisError as e:
        logging.error(f"[Redis SET error] {e}")