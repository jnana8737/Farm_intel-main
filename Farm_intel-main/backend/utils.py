import pandas as pd
import numpy as np
import joblib
import json
import requests
from geopy.geocoders import Nominatim
import ee

# ------------------ INIT ------------------

geolocator = Nominatim(user_agent="crop_app")

# ⚠️ IMPORTANT: Authenticate once manually before running
ee.Initialize(project='crop-suitability-project')

# ------------------ LOAD MODEL ------------------

model = joblib.load("final_model/rf_model.pkl")
le = joblib.load("final_model/label_encoder.pkl")

with open("final_model/district_crop_map.json") as f:
    district_crop_map = json.load(f)

with open("final_model/historical_lookup.json") as f:
    historical_lookup = json.load(f)

# ------------------ LOCATION ------------------

def get_district(lat, lon):
    location = geolocator.reverse((lat, lon), language='en')

    if location is None:
        return None

    address = location.raw.get('address', {})

    district = (
        address.get('state_district') or
        address.get('county') or
        address.get('district') or
        address.get('city')
    )

    if district:
        return district.lower().replace(" district", "").strip()

    return None


def get_lat_lon_from_district(district):
    location = geolocator.geocode(f"{district}, India")

    if location:
        return location.latitude, location.longitude
    return None, None

# ------------------ NDVI ------------------

def get_season_dates(season):
    season = season.lower()

    if season == "kharif":
        return '2025-06-01', '2025-10-31'
    elif season == "rabi":
        return '2025-10-01', '2026-03-31'
    else:
        return '2025-01-01', '2025-12-31'


def mask_s2_clouds(img):
    qa = img.select('QA60')
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11

    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(
           qa.bitwiseAnd(cirrus_bit_mask).eq(0))

    return img.updateMask(mask)


def get_ndvi(lat, lon, season):

    start, end = get_season_dates(season)
    region = ee.Geometry.Point([lon, lat]).buffer(500)

    col = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
           .filterBounds(region)
           .filterDate(start, end)
           .map(mask_s2_clouds))

    def add_ndvi(img):
        nd = img.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return img.addBands(nd)

    col = col.map(add_ndvi)

    ndvi_max = col.select('NDVI').max()

    stats = ndvi_max.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=region,
        scale=10,
        bestEffort=True
    ).getInfo()

    return stats.get('NDVI', 0.3)


def land_suitability(lat, lon, season):
    ndvi = get_ndvi(lat, lon, season)

    if ndvi > 0.5:
        return "Highly Suitable", ndvi
    elif ndvi > 0.25:
        return "Moderately Suitable", ndvi
    else:
        return "Low Suitable", ndvi

# ------------------ WEATHER ------------------

def get_weather(lat, lon):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m,precipitation"

    data = requests.get(url).json()

    temp = data['current_weather']['temperature']
    current_time = data['current_weather']['time']

    hourly_times = data['hourly']['time']

    idx = min(
        range(len(hourly_times)),
        key=lambda i: abs(pd.to_datetime(hourly_times[i]) - pd.to_datetime(current_time))
    )

    humidity = data['hourly']['relativehumidity_2m'][idx]
    rainfall = data['hourly']['precipitation'][idx]

    return temp, humidity, rainfall

# ------------------ MAIN SYSTEM ------------------

def full_system(
    lat=None,
    lon=None,
    district=None,
    season="kharif",
    mode="auto",
    N=None,
    P=None,
    K=None
):

    # LOCATION
    if mode == "auto":
        lat, lon = get_lat_lon_from_district(district)
        district = district.lower()

    elif mode == "coords":
        district = get_district(lat, lon)

    if lat is None or lon is None or district is None:
        return {"error": "Invalid location input"}

    # DEFAULT NPK
    if N is None: N = 90
    if P is None: P = 40
    if K is None: K = 40

    # NDVI
    try:
        suitability, ndvi = land_suitability(lat, lon, season)
    except:
        suitability, ndvi = "Moderately Suitable", 0.5

    # WEATHER
    try:
        temp, humidity, rainfall = get_weather(lat, lon)
    except:
        temp, humidity, rainfall = 25, 70, 200

    # MODEL INPUT
    input_df = pd.DataFrame([{
        'N': N,
        'P': P,
        'K': K,
        'temperature': temp,
        'humidity': humidity,
        'ph': 6.5,
        'rainfall': rainfall
    }])

    probs = model.predict_proba(input_df)[0]
    prob_dict = dict(zip(le.classes_, probs))

    # FALLBACK
    if district not in district_crop_map or season not in district_crop_map[district]:
        sorted_crops = sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)

        return {
            "Suitability": suitability,
            "NDVI": round(ndvi, 2),
            "Top Crops": sorted_crops[:3]
        }

    # FILTERED
    allowed = district_crop_map[district][season]

    results = []

    for crop in allowed:

        crop = crop.lower()

        agro = prob_dict.get(crop, prob_dict.get('maize', 0)*0.85)

        yield_s = historical_lookup.get(district, {}) \
            .get(season, {}) \
            .get(crop, {}) \
            .get("yield_score", 0)

        area_s = historical_lookup.get(district, {}) \
            .get(season, {}) \
            .get(crop, {}) \
            .get("area_share", 0)

        final_score = 0.5*agro + 0.3*yield_s + 0.2*area_s

        results.append((crop, final_score))

    results.sort(key=lambda x: x[1], reverse=True)

    return {
        "Suitability": suitability,
        "NDVI": round(ndvi, 2),
        "Top Crops": results[:3]
    }