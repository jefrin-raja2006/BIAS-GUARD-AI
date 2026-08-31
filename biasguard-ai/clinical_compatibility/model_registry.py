# clinical_compatibility/model_registry.py

MODEL_REGISTRY = {

    "diabetes_e08_e13": {
        "model_name": "Diabetes Prediction Model",
        "disease_group": "E08-E13 Diabetes Mellitus",
        "description": "Predicts diabetes using clinical and laboratory features.",

        # Features used when your E08_E13 model was trained
        "required_features": [
            "pregnancies",
            "glucose",
            "blood_pressure",
            "skin_thickness",
            "insulin",
            "bmi",
            "diabetes_pedigree_function",
            "age"
        ],

        "model_path": "saved_models/E08_E13_Diabetes/model.joblib",
        "scaler_path": "saved_models/E08_E13_Diabetes/scaler.joblib",

        # Minimum percentage required to consider compatibility
        "minimum_compatibility": 100
    },

}