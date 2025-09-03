from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

# Patient information (used if you extend user profiles later)
class Patient(BaseModel):
    patient_id: str
    weight_kg: Optional[float] = None
    insulin_sensitivity: Optional[float] = Field(
        default=None, description="mg/dL drop per unit insulin"
    )

# Record of a dose + glucose reading
class DoseEvent(BaseModel):
    patient_id: str
    timestamp: datetime
    dosage_units: float
    carbs_g: float = 0.0
    glucose_mgdl: float
    meal_tag: Optional[str] = None  # e.g., breakfast/lunch/dinner/snack

# Prediction request payload
class PredictionRequest(BaseModel):
    patient_id: str
    timestamp: datetime
    recent_window_min: int = 180

# Prediction response payload
class PredictionResponse(BaseModel):
    patient_id: str
    horizon_min: int
    predicted_glucose_mgdl: float
    risk: str  # "hypo" | "in-range" | "hyper"
    alerts: list[str]

# For bulk CSV ingestion
class IngestCSVRequest(BaseModel):
    csv_path: str
    tz_aware: bool = False
    model_config = ConfigDict(protected_namespaces=())
