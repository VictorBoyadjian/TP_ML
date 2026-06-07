from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import UserInput, PredictionOutput
from app.service import PredictionService
import sqlite3, datetime

app = FastAPI(title='Expercience predictor', description='API ML - APIE686', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
svc = PredictionService()

def init_db():
    con = sqlite3.connect('predictions.db')
    con.execute('''CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT, levels TEXT, confidence REAL,
    age REAL, session_duration REAL, workout_frequency REAL, bmi REAL
    )''')
    con.commit(); con.close()

init_db()

@app.get('/health')
def health():
    return {"status": "ok", "model": "RandomForestClassifier"}

@app.post('/predict', response_model=PredictionOutput)
def predict(user_input: UserInput):
    try:
        result = svc.predict(user_input)
        con = sqlite3.connect('predictions.db')
        con.execute('INSERT INTO predictions VALUES (NULL,?,?,?,?,?,?,?)',
        (datetime.datetime.now().isoformat(), result.level.value, result.confidence,
        user_input.age, user_input.session_duration,
        user_input.workout_frequency, user_input.bmi))
        con.commit(); con.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get('/logs', response_model=list)
def get_logs():
    con = sqlite3.connect('predictions.db')
    rows = con.execute('SELECT * FROM predictions ORDER BY id DESC').fetchall()
    con.close()
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "levels": r[2],
            "confidence": r[3],
            "age": r[4],
            "session_duration": r[5],
            "workout_frequency": r[6],
            "bmi": r[7]
        } for r in rows
    ]