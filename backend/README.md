# Apollo Krishi Rakshak Backend API

Production inference backend for `apollokrushi.chatakeinnoworks.com`.

## Endpoints

- `GET /health` - service and model readiness
- `POST /api/detect` - image-based crop+disease inference

## Required Model Files

Place the following files in `backend/models/`:

- `best_crop_model.keras`
- `crop_class_names.npy`
- `<crop>_disease_model.keras` (example: `wheat_disease_model.keras`)
- `<crop>_class_names.npy` (example: `wheat_class_names.npy`)

## Core Model Pack Included In Repo

The repository currently ships a working core set:

- `best_crop_model.keras`
- `crop_class_names.npy`
- `wheat_disease_model.keras`
- `wheat_class_names.npy`

If a disease model for predicted crop is unavailable, API falls back to wheat disease model and returns a `note` field.

## Run Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Run

```bash
cd backend
docker build -t apollo-inference-api .
docker run -p 8000:8000 apollo-inference-api
```

## Environment Variables

- `APOLLO_MODEL_DIR` (optional): absolute path to model directory
- `CORS_ORIGINS` (optional): comma-separated allowed origins
- `APOLLO_DEFAULT_DISEASE_CROP` (optional): fallback disease model crop, default `wheat`

Example:

```bash
CORS_ORIGINS=https://apollokrushi.chatakeinnoworks.com,https://apollo.paper.chatakeinnoworks.com
```

## Cloudflare DNS (for backend)

Add DNS after deploying backend service to your host:

- Type: `CNAME`
- Name: `api.apollokrushi`
- Target: `<your-backend-hostname>`
- Proxy: DNS only during setup, then optional proxied

Then set frontend API URL to:

`https://api.apollokrushi.chatakeinnoworks.com/api/detect`
