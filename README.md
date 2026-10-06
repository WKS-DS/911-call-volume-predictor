# 911 Call Volume Predictor

A full-stack machine learning pipeline that predicts Seattle Fire Department 911 call volume by hour. Built with PostgreSQL, scikit-learn, FastAPI, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange)

## Overview

This project demonstrates an end-to-end data science workflow:

1. **Data ingestion** — Load 2.2M Seattle 911 dispatch records into PostgreSQL
2. **Feature engineering** — Aggregate raw calls into hourly counts with temporal features
3. **Model training** — Train a Random Forest regressor on calendar-based features
4. **API deployment** — Serve predictions via FastAPI REST endpoint
5. **Dashboard** — Interactive Streamlit UI for non-technical users

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Seattle 911   │────▶│   PostgreSQL    │────▶│  Random Forest  │
│   CSV (2.2M)    │     │   dispatch_911  │     │     Model       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌───────────────────────────────┘
                        ▼
              ┌─────────────────┐     ┌─────────────────┐
              │    FastAPI      │◀───▶│    Streamlit    │
              │   /predict      │     │    Dashboard    │
              └─────────────────┘     └─────────────────┘
```

## Results

| Metric | Value |
|--------|-------|
| Training samples | 159,222 |
| Test samples | 39,806 |
| MAE | 3.19 calls |
| R² Score | 0.373 |

The baseline model uses only calendar features (year, month, day of week, hour). Future iterations will add weather data, holidays, and lagged features to improve accuracy.

## Project Structure

```
911-call-volume-predictor/
├── api/
│   └── main.py              # FastAPI prediction endpoint
├── dashboard/
│   └── app.py               # Streamlit interactive UI
├── data/
│   └── seattle_fire_911.csv # Raw data (not tracked)
├── models/
│   └── model.pkl            # Trained model (not tracked)
├── notebooks/
│   └── 01_data_exploration.ipynb
├── src/
│   ├── data_loader.py       # CSV → PostgreSQL ETL
│   ├── features.py          # Hourly aggregation via SQL
│   └── model.py             # Training and evaluation
├── requirements.txt
└── README.md
```

## Tech Stack

- **Database:** PostgreSQL 15 with SQLAlchemy
- **ML:** scikit-learn (Random Forest Regressor)
- **API:** FastAPI with Pydantic validation
- **Dashboard:** Streamlit
- **Data processing:** pandas, NumPy

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 15+
- [Seattle Fire 911 Dataset](https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj)

### Installation

```bash
# Clone repository
git clone https://github.com/WKS-DS/911-call-volume-predictor.git
cd 911-call-volume-predictor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Additional dependencies for API and dashboard
pip install fastapi uvicorn streamlit requests
```

### Database Setup

```bash
# Create database
createdb dispatch_911

# Load data (place CSV in data/ directory first)
python src/data_loader.py

# Create hourly aggregations
python src/features.py
```

### Train Model

```bash
python src/model.py
```

### Run API

```bash
uvicorn api.main:app --reload
# API available at http://127.0.0.1:8000
# Docs at http://127.0.0.1:8000/docs
```

### Run Dashboard

```bash
streamlit run dashboard/app.py
# Dashboard available at http://localhost:8501
```

## API Usage

```bash
# Health check
curl http://127.0.0.1:8000/health

# Predict calls for Thursday at 5 PM
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"year": 2026, "month": 10, "day_of_week": 4, "hour": 17}'

# Response: {"predicted_calls": 20.3}
```

## Data Source

[Seattle Real Time Fire 911 Calls](https://data.seattle.gov/Public-Safety/Seattle-Real-Time-Fire-911-Calls/kzjm-xkqj) — Open data from the City of Seattle covering emergency dispatch records.

## Roadmap

- [ ] Add weather features (temperature, precipitation)
- [ ] Add holiday indicators
- [ ] Add lagged features (calls in previous hours)
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)
- [ ] GitHub Actions CI/CD

## License

MIT

---

Built by [Will Scott](https://github.com/WKS-DS) as part of the Gonzaga University M.S. Data Science program.
