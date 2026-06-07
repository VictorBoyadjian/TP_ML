from enum import Enum
from pydantic import BaseModel, Field


class FitnessLevel(str, Enum):
    DEBUTANT = 'Débutant'
    INTERMEDIAIRE = 'Intermédiaire'
    AVANCE = 'Avancé'


FITNESS_LEVEL_MAP = {
    1: FitnessLevel.DEBUTANT,
    2: FitnessLevel.INTERMEDIAIRE,
    3: FitnessLevel.AVANCE,
}


class UserInput(BaseModel):
    session_duration: float = Field(..., gt=0, example=39.1, description='Durée de la session (minutes)')
    workout_frequency: float = Field(..., gt=0, example=18.7, description='Fréquence des entraînements (sessions par semaine)')
    bmi: float = Field(..., gt=0, example=181.0, description='Indice de masse corporelle (IMC)')
    age: float = Field(..., gt=0, example=3750.0, description='Âge (années)')


class PredictionOutput(BaseModel):
    level: FitnessLevel
    confidence: float
    message: str