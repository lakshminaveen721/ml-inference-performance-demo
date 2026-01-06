import time
import torch
from fastapi import FastAPI
from prometheus_client import (
    Histogram,
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from starlette.responses import Response

from app.model import ModelService
from app.schemas import PredictionRequest, PredictionResponse
from app.batcher import DynamicBatcher


# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(
    title="ML Inference Performance Demo",
    description="Inference service with dynamic batching and performance metrics",
    version="1.0.0",
)

model_service = ModelService()

batcher = DynamicBatcher(
    model_service=model_service,
    max_batch_size=8,
    max_wait_ms=5,
)


# -----------------------------
# Prometheus Metrics
# -----------------------------
INFERENCE_LATENCY = Histogram(
    "inference_latency_seconds",
    "Latency for model inference",
    buckets=(0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0),
)

INFERENCE_REQUESTS = Counter(
    "inference_requests_total",
    "Total inference requests",
)

INFERENCE_ERRORS = Counter(
    "inference_errors_total",
    "Total inference errors",
)


# -----------------------------
# Routes
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_ready": model_service.ready,
        "device": model_service.device,
        "precision": model_service.precision,
    }




@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    start_time = time.time()
    INFERENCE_REQUESTS.inc()

    try:
        # Dummy input (batch=1)
        input_tensor = torch.randn(1, 3, 224, 224)

        # Submit to dynamic batcher
        class_id = batcher.submit(input_tensor)

    except Exception:
        INFERENCE_ERRORS.inc()
        raise

    finally:
        latency = time.time() - start_time
        INFERENCE_LATENCY.observe(latency)

    return PredictionResponse(
        class_id=class_id,
        latency_ms=latency * 1000,
    )


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
