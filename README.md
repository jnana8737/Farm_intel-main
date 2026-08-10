# Farm_intel

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![REST API](https://img.shields.io/badge/REST-API-25D366?style=flat)

## What it does

An end-to-end precision-agriculture platform covering the full soil-to-sale pipeline — instead of a farmer needing five different tools for soil analysis, crop choice, fertilizer planning, disease detection, and price forecasting, this puts all five behind one decision engine.

## Key features

- **Land suitability assessment** — CNN + GIS analysis on field data
- **Crop recommendation** — Random Forest / XGBoost on N/P/K/pH/OC/EC soil features + climate data
- **Fertilizer prediction & crop rotation planning**
- **Disease & pest detection** — CNN on field images
- **Market price forecasting** — ARIMA / LSTM time-series models
- **Weather Forecast API** — regression + time-series on historical climate data, fed live into crop recommendation and irrigation scheduling, **reducing simulated resource consumption by 22%**
- **Decision Fusion Engine** — resolves trade-offs between profit maximization and sustainability targets across all module outputs

## Architecture

```
Data Acquisition
(soil sensors, weather API, field images)
            │
            ▼
     ML Intelligence Layer
  ┌─────────┬─────────┬──────────┐
  Crop Rec   Disease    Price
  (RF/XGB)   Detection  Forecast
             (CNN)      (ARIMA/LSTM)
  └─────────┴─────────┴──────────┘
            │
            ▼
     Decision Fusion Engine
  (profit vs. sustainability trade-off resolution)
            │
            ▼
        Mobile App
   (farmer-facing, multilingual)
```

## Tech stack

| Layer | Tools |
|---|---|
| ML | Scikit-learn, Random Forest, XGBoost, CNN, ARIMA, LSTM |
| API | REST API (Weather Forecast service) |
| Data | N/P/K/pH/OC/EC soil features, GIS, historical climate data |

## Design decisions

- **Decision Fusion Engine as a separate layer** rather than baking trade-offs into each model — keeps profit/sustainability weighting tunable without retraining individual models.
- **Virtual sensing** where physical soil sensors aren't available — estimates key soil parameters from satellite/climate proxies, since this needed to work for farmers without sensor hardware.
- **Cloud-native, scalable design** chosen over a single-farm desktop tool, since the eventual goal is multi-region deployment.

## Setup

```bash
git clone https://github.com/jnana8737/Farm_intel-main.git
cd Farm_intel-main
pip install -r requirements.txt
python app.py
```

## What I'd add next

- Swap the manual feature engineering for an automated feature pipeline
- Add test coverage on the recommendation and forecasting modules
- Containerize the full pipeline (currently runs as separate scripts)
