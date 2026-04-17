import io
import os
from typing import Dict, Optional, Tuple

import numpy as np
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

try:
    import tensorflow as tf
except Exception as exc:  # pragma: no cover
    tf = None
    TF_IMPORT_ERROR = str(exc)
else:
    TF_IMPORT_ERROR = ""


APP_NAME = "Apollo Krishi Rakshak Inference API"
APP_VERSION = "1.0.0"
MODEL_DIR = os.getenv("APOLLO_MODEL_DIR", os.path.join(os.path.dirname(__file__), "..", "models"))
ALLOWED_ORIGINS = [x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(",") if x.strip()]

app = FastAPI(title=APP_NAME, version=APP_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crop_model = None
crop_classes = None
disease_model_cache: Dict[str, Tuple[object, np.ndarray]] = {}


def _model_path(file_name: str) -> str:
    return os.path.abspath(os.path.join(MODEL_DIR, file_name))


def _ensure_tensorflow() -> None:
    if tf is None:
        raise RuntimeError(f"TensorFlow import failed: {TF_IMPORT_ERROR}")


def _load_crop_assets() -> None:
    global crop_model, crop_classes
    if crop_model is not None and crop_classes is not None:
        return

    _ensure_tensorflow()

    crop_model_path = _model_path("best_crop_model.keras")
    crop_classes_path = _model_path("crop_class_names.npy")

    if not os.path.exists(crop_model_path):
        raise FileNotFoundError(f"Missing crop model: {crop_model_path}")
    if not os.path.exists(crop_classes_path):
        raise FileNotFoundError(f"Missing crop classes file: {crop_classes_path}")

    crop_model = tf.keras.models.load_model(crop_model_path, compile=False)
    crop_classes = np.load(crop_classes_path, allow_pickle=True)


def _load_disease_assets(crop_name: str) -> Tuple[object, np.ndarray]:
    key = crop_name.lower().strip()
    if key in disease_model_cache:
        return disease_model_cache[key]

    _ensure_tensorflow()

    model_file = f"{key}_disease_model.keras"
    classes_file = f"{key}_class_names.npy"

    model_path = _model_path(model_file)
    classes_path = _model_path(classes_file)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Missing disease model for crop '{key}': {model_path}")
    if not os.path.exists(classes_path):
        raise FileNotFoundError(f"Missing disease classes for crop '{key}': {classes_path}")

    model = tf.keras.models.load_model(model_path, compile=False)
    classes = np.load(classes_path, allow_pickle=True)
    disease_model_cache[key] = (model, classes)
    return model, classes


def _prepare_image_bytes(image_bytes: bytes, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(target_size)
    array = np.array(image, dtype=np.float32) / 255.0
    return np.expand_dims(array, axis=0)


def _predict_crop(image_tensor: np.ndarray) -> Tuple[str, float]:
    _load_crop_assets()
    preds = crop_model.predict(image_tensor, verbose=0)[0]
    idx = int(np.argmax(preds))
    confidence = float(preds[idx])
    crop_name = str(crop_classes[idx])
    return crop_name, confidence


def _predict_disease(crop_name: str, image_tensor: np.ndarray) -> Tuple[str, float]:
    model, classes = _load_disease_assets(crop_name)
    preds = model.predict(image_tensor, verbose=0)[0]
    idx = int(np.argmax(preds))
    confidence = float(preds[idx])
    label = str(classes[idx])
    return label, confidence


def _recommendation(crop_name: str, disease_label: str) -> str:
    disease = disease_label.lower()
    if "healthy" in disease:
        return f"{crop_name.title()} appears healthy. Continue scheduled monitoring and irrigation balance."
    if "rust" in disease or "blight" in disease or "fung" in disease:
        return "Potential fungal risk detected. Inspect surrounding plants and begin targeted treatment workflow."
    if "deficiency" in disease or "nutrient" in disease:
        return "Nutrient stress pattern detected. Run soil and leaf nutrition checks before next intervention cycle."
    return "Anomaly detected. Trigger a field review and confirm with agronomy specialist workflow."


@app.get("/")
def root() -> Dict[str, str]:
    return {"service": APP_NAME, "version": APP_VERSION, "status": "running"}


@app.get("/health")
def health() -> Dict[str, object]:
    model_files = [
        _model_path("best_crop_model.keras"),
        _model_path("crop_class_names.npy"),
    ]
    available = all(os.path.exists(path) for path in model_files)
    return {
        "status": "ok" if available else "degraded",
        "tensorflow_ready": tf is not None,
        "model_dir": os.path.abspath(MODEL_DIR),
        "core_models_present": available,
        "version": APP_VERSION,
    }


@app.post("/api/detect")
async def detect(file: UploadFile = File(...), crop: Optional[str] = Form(default="")) -> Dict[str, object]:
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    payload = await file.read()
    if not payload:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    try:
        image_tensor = _prepare_image_bytes(payload)

        if crop and crop.strip():
            crop_name = crop.strip().lower()
            crop_conf = None
        else:
            crop_name, crop_conf = _predict_crop(image_tensor)

        disease_label, disease_conf = _predict_disease(crop_name, image_tensor)
        response = {
            "crop": crop_name,
            "crop_confidence": crop_conf,
            "disease": disease_label,
            "disease_confidence": round(disease_conf, 4),
            "recommendation": _recommendation(crop_name, disease_label),
            "model_dir": os.path.abspath(MODEL_DIR),
        }
        return response
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc
