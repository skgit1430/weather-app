# SkyCast — Weather Prediction App
**By Sujit Kanna RP**

A full-stack weather application built with Python (Flask) backend and a pure JS frontend.
Shows real-time weather, 5-day forecasts, and hourly charts for any city in the world.

---

## 🛠 Tech Stack
- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **API:** OpenWeatherMap

---

## 🚀 How to Run

### 1. Get a Free API Key
- Go to https://openweathermap.org/api
- Sign up for free
- Copy your API key

### 2. Add your API key
Open `app.py` and replace:
```python
API_KEY = "YOUR_API_KEY"
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
Visit: http://localhost:5000

---

## 📁 Project Structure
```
weather-app/
├── app.py              # Flask backend (3 API endpoints)
├── requirements.txt    # Python dependencies
├── README.md
└── static/
    └── index.html      # Frontend (HTML + CSS + JS)
```

---

## ✨ Features
- 🔍 Search any city worldwide
- 🌡️ Current temperature, feels like, humidity, wind, pressure, visibility
- 🌅 Sunrise & sunset times
- 📅 5-day forecast with rain probability
- 📊 24h temperature line chart
- 📊 24h humidity & rain bar/line chart
- ⏰ Hourly breakdown for next 24 hours
- 🌡️ Switch between °C and °F
- 📱 Fully responsive design

---

## 🔌 API Endpoints
| Endpoint | Description |
|---|---|
| `GET /api/weather?city=Chennai` | Current weather |
| `GET /api/forecast?city=Chennai` | 5-day forecast |
| `GET /api/hourly?city=Chennai` | 24-hour data for charts |
