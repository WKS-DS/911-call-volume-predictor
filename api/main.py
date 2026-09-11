from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from pathlib import Path
import pandas as pd

app = FastAPI(title="911 Call Volume Predictor")

MODEL_PATH = Path(__file__).resolve().parent.parent / 'models' / 'model.pkl'
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

class PredictionRequest(BaseModel):
    year: int
    month: int
    day_of_week: int  # 0=Sunday, 6=Saturday
    hour: int

class PredictionResponse(BaseModel):
    predicted_calls: float

@app.get("/")
def root():
    return {"message": "911 Call Volume Predictor API"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    X = pd.DataFrame([{
        'year': request.year,
        'month': request.month,
        'day_of_week': request.day_of_week,
        'hour': request.hour
    }])
    prediction = model.predict(X)[0]
    return PredictionResponse(predicted_calls=round(prediction, 1))

@app.get("/health")
def health():
    return {"status": "healthy"}