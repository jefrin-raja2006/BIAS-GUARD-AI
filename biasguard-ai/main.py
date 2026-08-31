from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.bias_detect import router as bias_router
from routers.bias_mitigate import router as mitigate_router
from routers.predict import router as predict_router
from lab_extraction.router import router as lab_router
from clinical_standardization.router import router as clinical_router
from clinical_compatibility.router import router as compatibility_router
from disease_prediction.router import router as disease_router
app = FastAPI(
    title="BiasGuard AI — Backend",
    description=(
        "Bias detection and mitigation for 8 endocrinology disease models.\n\n"
        "**Supported diseases:** thyroid, diabetes, glucose, pcos, "
        "malnutrition, vitamin_d, obesity, metabolic\n\n"
        "**Endpoints:**\n"
        "- `GET /bias/check?disease=<name>` — bias metrics for one disease\n"
        "- `GET /bias/check/all` — bias summary across all diseases\n"
        "- `POST /mitigate/smote?disease=<name>` — SMOTE balancing\n"
        "- `POST /mitigate/synthetic?disease=<name>` — synthetic data generation"
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bias_router)
app.include_router(mitigate_router)
app.include_router(predict_router)
app.include_router(lab_router)
app.include_router(clinical_router)
app.include_router(compatibility_router)
app.include_router(disease_router)
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "BiasGuard AI backend running",
        "version": "2.0.0",
        "supported_diseases": [
            "thyroid", "diabetes", "glucose", "pcos",
            "malnutrition", "vitamin_d", "obesity", "metabolic"
        ],
        "endpoints": {
            "bias_check_single": "GET /bias/check?disease=diabetes",
            "bias_check_all":    "GET /bias/check/all",
            "smote":             "POST /mitigate/smote?disease=diabetes",
            "synthetic":         "POST /mitigate/synthetic?disease=diabetes&num_rows=200",
            "docs":              "GET /docs",
        }
    }