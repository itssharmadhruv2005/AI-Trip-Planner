# import random, json, io, os
# from datetime import datetime

# DATA_FILE = 'data/travel_data.json'
# SAVE_FILE = 'saved_itineraries.json'

# def load_data():
#     with open(DATA_FILE, 'r', encoding='utf-8') as f:
#         return json.load(f)

# def generate_itinerary(destination, days, budget, interests):
#     data = load_data()
#     if destination not in data:
#         return f"Sorry, {destination} is not in our database."

#     dest_data = data[destination]

#     attractions = []
#     for v in dest_data.values():
#         if isinstance(v, list):
#             attractions.extend(v)

#     itinerary = []
#     daily_budget = budget / days if days > 0 else 0

#     for day in range(1, days + 1):
#         activity = attractions[(day - 1) % len(attractions)]
#         itinerary.append({
#             "day": day,
#             "activities": [activity],
#             "estimated_cost": daily_budget
#         })

#     return itinerary


# def export_itinerary_text(destination, itinerary, total_cost, budget):
#     lines = []
#     lines.append(f'AI Trip Planner - Itinerary for {destination}')
#     lines.append(f'Generated: {datetime.utcnow().isoformat()} UTC')
#     lines.append('')
#     for day in itinerary:
#         lines.append(f"Day {day['day']}: {', '.join(day['activities'])} | Cost: ₹{day['estimated_cost']}")
#     lines.append('')
#     lines.append(f'Estimated Total Cost: ₹{total_cost} (Budget: ₹{budget})')
#     return '\n'.join(lines)

# def save_itinerary(destination, itinerary, total_cost, budget):
#     new_entry = {
#         "destination": destination,
#         "generated_at": datetime.utcnow().isoformat(),
#         "itinerary": itinerary,
#         "total_cost": total_cost,
#         "budget": budget
#     }
#     if os.path.exists(SAVE_FILE):
#         with open(SAVE_FILE, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#     else:
#         data = []
#     data.append(new_entry)
#     with open(SAVE_FILE, 'w', encoding='utf-8') as f:
#         json.dump(data, f, indent=2)

# def load_saved_itineraries():
#     if os.path.exists(SAVE_FILE):
#         with open(SAVE_FILE, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     return []


import json, os, requests
from datetime import datetime, timedelta

DATA_FILE = 'data/travel_data.json'
SAVE_FILE = 'saved_itineraries.json'
API_KEY = "2509b358692bbe6743ea5cd4c30e3ace"  # 🔑 replace with your OpenWeatherMap key


def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_hotels(destination):
    data = load_data()
    if destination in data and "hotels" in data[destination]:
        return data[destination]["hotels"]
    return []


def get_weather(destination, days):
    """Fetch weather forecast for destination city"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={destination}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        forecasts = []
        if "list" in data:
            # Take 1 forecast per day
            for i in range(days):
                idx = i * 8  # 8 intervals per day
                if idx < len(data["list"]):
                    date_txt = data["list"][idx]["dt_txt"].split(" ")[0]
                    temp = data["list"][idx]["main"]["temp"]
                    weather = data["list"][idx]["weather"][0]["description"]
                    forecasts.append(f"{date_txt}: {temp}°C, {weather}")
        return forecasts
    except:
        return ["Weather unavailable"] * days


def generate_itinerary(destination, days, budget, interests):
    data = load_data()
    if destination not in data:
        return f"Sorry, {destination} is not in our database."

    dest_data = data[destination]

    attractions = []
    for v in dest_data.values():
        if isinstance(v, list):
            attractions.extend(v)

    itinerary = []
    daily_budget = budget / days if days > 0 else 0

    # Fetch weather
    weather_forecast = get_weather(destination, days)

    for day in range(1, days + 1):
        activity = attractions[(day - 1) % len(attractions)]
        itinerary.append({
            "day": day,
            "activities": [activity],
            "weather": weather_forecast[day - 1] if day - 1 < len(weather_forecast) else "N/A",
            "estimated_cost": daily_budget
        })

    return itinerary


def export_itinerary_text(destination, itinerary, total_cost, budget):
    lines = []
    lines.append(f'AI Trip Planner - Itinerary for {destination}')
    lines.append(f'Generated: {datetime.utcnow().isoformat()} UTC')
    lines.append('')
    for day in itinerary:
        lines.append(f"Day {day['day']}: {', '.join(day['activities'])} | {day['weather']} | Cost: ₹{day['estimated_cost']}")
    lines.append('')
    lines.append(f'Estimated Total Cost: ₹{total_cost} (Budget: ₹{budget})')
    return '\n'.join(lines)


def save_itinerary(destination, itinerary, total_cost, budget):
    new_entry = {
        "destination": destination,
        "generated_at": datetime.utcnow().isoformat(),
        "itinerary": itinerary,
        "total_cost": total_cost,
        "budget": budget
    }
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    data.append(new_entry)
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_saved_itineraries():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
