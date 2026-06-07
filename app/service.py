import joblib, numpy as np
from pathlib import Path
from app.schemas import UserInput, PredictionOutput, FITNESS_LEVEL_MAP
import os, requests


MODELS_DIR = Path(__file__).parent.parent / 'models'

class PredictionService:
    def __init__(self):
        self.model = joblib.load(MODELS_DIR / 'model.pkl')
        self.encoder = joblib.load(MODELS_DIR / 'encoder.pkl')
        print("Model chargé")

    def predict(self, data: UserInput) -> PredictionOutput:
        X = np.array([[data.age, data.session_duration, 
                       data.workout_frequency, data.bmi]])
        idx = self.model.predict(X)[0]
        confidence = float(self.model.predict_proba(X)[0][idx])
        level = FITNESS_LEVEL_MAP[int(self.encoder.inverse_transform([idx])[0])]
        return PredictionOutput(
            level=level,
            confidence=confidence,
            message=f"{level.value} - confiance: {confidence:.1%}"
        )  