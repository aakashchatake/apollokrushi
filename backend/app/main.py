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
DEFAULT_DISEASE_CROP = os.getenv("APOLLO_DEFAULT_DISEASE_CROP", "wheat").strip().lower()

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


def _select_disease_crop(preferred_crop: str) -> Tuple[str, Optional[str]]:
    preferred = preferred_crop.lower().strip()
    preferred_model = _model_path(f"{preferred}_disease_model.keras")
    preferred_classes = _model_path(f"{preferred}_class_names.npy")
    if os.path.exists(preferred_model) and os.path.exists(preferred_classes):
        return preferred, None

    fallback_model = _model_path(f"{DEFAULT_DISEASE_CROP}_disease_model.keras")
    fallback_classes = _model_path(f"{DEFAULT_DISEASE_CROP}_class_names.npy")
    if os.path.exists(fallback_model) and os.path.exists(fallback_classes):
        reason = (
            f"Disease model for '{preferred}' not found. "
            f"Used fallback disease model '{DEFAULT_DISEASE_CROP}'."
        )
        return DEFAULT_DISEASE_CROP, reason

    raise FileNotFoundError(
        f"No disease model available for '{preferred}' and fallback '{DEFAULT_DISEASE_CROP}' is missing"
    )


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
    """Comprehensive disease recommendation with symptoms, management, and prevention."""
    disease = disease_label.lower().strip()
    
    # Disease Information Database
    disease_db = {
        "wheat": {
            "healthy": {
                "symptoms": "No visible disease signs. Leaf tissue appears normal with green coloration.",
                "management": "Continue regular monitoring. Maintain optimal irrigation (55-60mm during growth). Scout fields weekly for early disease detection.",
                "prevention": "Rotate crops to break disease cycles. Use resistant varieties. Monitor weather for humidity spikes."
            },
            "rust": {
                "symptoms": "Orange-brown or yellow pustules on leaf surfaces. Develop rapidly in 15-20°C with high humidity. Three types: leaf rust (small orange pustules), stripe rust (lemon-yellow striped), stem rust (dark reddish-brown).",
                "management": "Apply foliar fungicides (Propiconazole, Azoxystrobin) when disease appears on top 3 leaves. Early application critical. Repeat every 10-14 days if conditions favor spread.",
                "prevention": "Plant rust-resistant varieties (Lok-1, Raj-3961 in India). Space plants for air circulation. Avoid overhead irrigation in evening."
            },
            "blight": {
                "symptoms": "Water-soaked lesions that turn brown/gray. May have yellow halo. Often starts on lower leaves and moves upward.",
                "management": "Remove infected leaves. Apply copper-based fungicides (Bordeaux mixture 1%) or systemic fungicides (Mancozeb). Spray every 7-10 days during wet season.",
                "prevention": "Improve drainage. Avoid dense planting. Remove plant debris. Use disease-free seed."
            },
            "tan_spot": {
                "symptoms": "Tan, lens-shaped lesions (2-4mm) with yellow halo and dark center spot. Highly visible on flag leaves.",
                "management": "Fungicide application at boot stage (critical). Use Pyraclostrobin, Propiconazole, or Azoxystrobin. Two sprays 2 weeks apart effective.",
                "prevention": "Rotate crops (minimum 2 years without wheat). Incorporate wheat residue to reduce inoculum. Use resistant varieties."
            },
            "powdery_mildew": {
                "symptoms": "White to grayish powdery coating on leaves and stems. Occurs in cool, dry conditions. Reduces photosynthesis.",
                "management": "Sulfur dust (10kg/ha) or wettable sulfur spray. Alternate with Karathane (0.1%) if sulfur resistance develops. Apply at first sign.",
                "prevention": "Improve air circulation. Reduce nitrogen fertilizer (promotes susceptibility). Choose resistant varieties."
            },
            "nutrient_deficiency": {
                "symptoms": "Leaf yellowing (Nitrogen: older leaves first), purple tinting (Phosphorus), chlorosis (Iron). Stunted growth common.",
                "management": "Conduct soil and leaf tissue testing. Nitrogen: apply 25-50kg/ha urea. Phosphorus: 60-80kg/ha DAP. Micronutrients via foliar spray (2% solution).",
                "prevention": "Balanced fertilizer schedule. Soil pH 6.0-7.5 optimal. Organic matter addition improves nutrient availability."
            }
        },
        "rice": {
            "healthy": {
                "symptoms": "Uniform green color, upright growth, no lesions or discoloration present.",
                "management": "Maintain 5-7cm standing water during growing season. Monitor for pests weekly. Nitrogen timing critical at tillering and panicle initiation.",
                "prevention": "Certified disease-free seed. Sanitation of field equipment. Proper water management."
            },
            "leaf_blast": {
                "symptoms": "Eye-shaped lesions with gray center and brown/purple border. Start on lower leaves. Severe cases cause leaf death.",
                "management": "Apply Tricyclazole (0.6%) or Propiconazole at first sign. Spray 2-3 times at 10-day intervals. Most critical before heading.",
                "prevention": "Use blast-resistant varieties. Avoid excess nitrogen. Maintain balanced potassium. Ensure proper drainage."
            },
            "brown_spot": {
                "symptoms": "Dark brown spots (1-3mm) with yellow border. Numerous lesions coalesce causing leaf browning. Associated with nutrient deficiency.",
                "management": "Improve plant nutrition (especially Potassium: 40-60kg MOP/ha). Fungicide spray if severe (Mancozeb 0.25%).",
                "prevention": "Balanced fertilization. Use resistant varieties. Disease-free seed treatment with fungicide."
            },
            "sheath_blight": {
                "symptoms": "Oblong lesions on leaf sheath, water-soaked appearance. Gray-white mycelium visible. Spread via contact to upper leaves.",
                "management": "Remove infected tillers. Fungicide spray (Hexaconazole 5%, Trifloxystrobin 0.5%) at boot stage and flowering.",
                "prevention": "Field sanitation. Destroy infected straw immediately. Wide plant spacing. Avoid excess nitrogen."
            }
        },
        "cotton": {
            "healthy": {
                "symptoms": "Vibrant green foliage, no lesions, normal boll development, no pest damage visible.",
                "management": "Monitor for bollworms, jassids, and mites weekly. Maintain irrigation schedule (60-90mm per season). Watch for fruiting body development.",
                "prevention": "Pest-resistant varieties. Balanced nutrition. Proper spacing for air circulation."
            },
            "bacterial_blight": {
                "symptoms": "Angular, water-soaked spots with yellow halo on leaves. Spread along veins. Affects bolls causing rot.",
                "management": "No cure once systemic. Remove and destroy infected plants immediately. Prevent spread with copper fungicides (Bordeaux 1%).",
                "prevention": "Use resistant varieties (MCU-5, H-274). Seed treatment with Streptomycin. Avoid wounding plants during operations."
            },
            "fusarium_wilt": {
                "symptoms": "Yellowing on one side of plant, wilting despite adequate water. Brown discoloration inside stems. Progressive plant death.",
                "management": "Remove infected plants completely (don't compost). Soil solarization (45 days in sun) kills fungal spores for next crop.",
                "prevention": "Crop rotation (3-4 years, no Okra/Guar). Use wilt-resistant varieties. Soil drainage essential."
            },
            "spider_mite_damage": {
                "symptoms": "Fine webbing on undersides, leaf stippling, bronzing. Severe infestation causes leaf drop and reduced fruiting.",
                "management": "Spray Buprofezin (0.5%) or Emamectin benzoate (0.015%). Repeat every 5-7 days. Monitor hot-dry weather closely.",
                "prevention": "Avoid excessive nitrogen. Sulfur dust (not with oils). Encourage predatory mites. Spray water to increase humidity."
            }
        }
    }
    
    # Get crop-specific diseases or use default
    crop_key = crop_name.lower().strip()
    crop_info = disease_db.get(crop_key, {})
    
    # Find disease match (check for keywords)
    for disease_key, info in crop_info.items():
        if disease_key.replace("_", "") in disease.replace(" ", "").replace("_", ""):
            return (
                f"**DISEASE: {disease_label.title()}**\n\n"
                f"SYMPTOMS:\n{info['symptoms']}\n\n"
                f"MANAGEMENT & TREATMENT:\n{info['management']}\n\n"
                f"PREVENTION:\n{info['prevention']}"
            )
    
    # Default comprehensive response for unknown diseases
    return (
        f"**FINDING: {disease_label.title()}**\n\n"
        f"STATUS: Condition detected on {crop_name.title()} crop.\n\n"
        f"RECOMMENDED ACTIONS:\n"
        f"1. IMMEDIATE: Inspect surrounding plants within 5m radius\n"
        f"2. SAMPLE: Collect leaf samples for lab testing and confirmation\n"
        f"3. TREATMENT: Consult extension officer with photos for precise diagnosis\n"
        f"4. MONITOR: Scout field daily for disease progression\n"
        f"5. PREVENT: Isolate affected area, do not harvest until confirmed\n\n"
        f"STATUS: Contact agronomy specialist for definitive identification and treatment plan."
    )


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

        disease_crop_used, fallback_note = _select_disease_crop(crop_name)
        disease_label, disease_conf = _predict_disease(disease_crop_used, image_tensor)
        response = {
            "crop": crop_name,
            "crop_confidence": crop_conf,
            "disease": disease_label,
            "disease_confidence": round(disease_conf, 4),
            "disease_model_crop": disease_crop_used,
            "recommendation": _recommendation(crop_name, disease_label),
            "model_dir": os.path.abspath(MODEL_DIR),
        }
        if fallback_note:
            response["note"] = fallback_note
        return response
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc
