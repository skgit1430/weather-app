# app.py — Weather Prediction App
# by Sujit Kanna RP
#
# HOW TO RUN:
# 1. pip install flask flask-cors requests
# 2. Get a FREE API key from https://openweathermap.org/api
# 3. Replace YOUR_API_KEY below with your key
# 4. Run: python app.py
# 5. Open http://localhost:5000 in your browser

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# ── CONFIG ──────────────────────────────────────────────
API_KEY = "06ba342eb917961440b8ae7a3e272406"   # <-- Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5"
# ────────────────────────────────────────────────────────


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get current weather for a city."""
    city = request.args.get('city', 'Chennai')
    units = request.args.get('units', 'metric')

    try:
        response = requests.get(
            f"{BASE_URL}/weather",
            params={
                'q': city,
                'appid': API_KEY,
                'units': units
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        return jsonify({
            'success': True,
            'city': data['name'],
            'country': data['sys']['country'],
            'temp': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s to km/h
            'visibility': data.get('visibility', 0) // 1000,       # m to km
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'icon_code': data['weather'][0]['main'],
            'sunrise': data['sys']['sunrise'],
            'sunset': data['sys']['sunset'],
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon'],
        })

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return jsonify({'success': False, 'error': 'City not found. Please check the spelling.'}), 404
        return jsonify({'success': False, 'error': 'Weather service error. Try again.'}), 500
    except requests.exceptions.ConnectionError:
        return jsonify({'success': False, 'error': 'No internet connection.'}), 503
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    """Get 5-day / 3-hour forecast for a city."""
    city = request.args.get('city', 'Chennai')
    units = request.args.get('units', 'metric')

    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                'q': city,
                'appid': API_KEY,
                'units': units,
                'cnt': 40  # 5 days × 8 intervals
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        # Group by day and pick one reading per day (noon preferred)
        daily = {}
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            hour = item['dt_txt'].split(' ')[1]
            if date not in daily or hour == '12:00:00':
                daily[date] = {
                    'date': date,
                    'temp_max': round(item['main']['temp_max']),
                    'temp_min': round(item['main']['temp_min']),
                    'temp': round(item['main']['temp']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'icon_code': item['weather'][0]['main'],
                    'wind_speed': round(item['wind']['speed'] * 3.6, 1),
                    'pop': round(item.get('pop', 0) * 100),  # precipitation %
                }

        forecast_list = list(daily.values())[:5]
        return jsonify({'success': True, 'forecast': forecast_list})

    except requests.exceptions.HTTPError:
        return jsonify({'success': False, 'error': 'City not found.'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/hourly', methods=['GET'])
def get_hourly():
    """Get next 24 hours of data for charts."""
    city = request.args.get('city', 'Chennai')
    units = request.args.get('units', 'metric')

    try:
        response = requests.get(
            f"{BASE_URL}/forecast",
            params={
                'q': city,
                'appid': API_KEY,
                'units': units,
                'cnt': 8  # next 24 hours (3h intervals)
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        hourly = []
        for item in data['list']:
            hourly.append({
                'time': item['dt_txt'][11:16],  # HH:MM
                'temp': round(item['main']['temp']),
                'humidity': item['main']['humidity'],
                'wind': round(item['wind']['speed'] * 3.6, 1),
                'pop': round(item.get('pop', 0) * 100),
            })

        return jsonify({'success': True, 'hourly': hourly})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    print("\n🌤  Weather App running at http://localhost:5000")
    print("⚠️  Make sure to add your OpenWeatherMap API key in app.py\n")
    app.run(debug=True, port=5000)
