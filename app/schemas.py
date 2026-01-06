from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    data: List[float]  # dummy input for now

class PredictionResponse(BaseModel):
    class_id: int
    latency_ms: float
