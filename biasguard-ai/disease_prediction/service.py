import os
import sys
import joblib
import numpy as np


# ==========================================================
# EXISTING ENDOCRINOLOGY AI PROJECT PATH
# ==========================================================

ENDO_AI_PATH = (
    r"C:\Users\Jefrin\Downloads\heart+disease (1)"
    r"\Endocrinology\AI_Endocrinology"
)

if ENDO_AI_PATH not in sys.path:
    sys.path.insert(0, ENDO_AI_PATH)


# ==========================================================
# IMPORT ENDOCRINOLOGY CONFIGURATION
# ==========================================================

from model_config import MODELS
from feature_mapper import get_features


# ==========================================================
# MASTER SCHEMA → MODEL FEATURE ADAPTER
# ==========================================================
#
# This converts BiasGuard canonical standardized names
# into the internal feature names expected by AI models.
#
# Example:
#
# Lab Report:        Glucose
# Master Schema:     glucose_level
# Diabetes Model:    glucose
#
# ==========================================================

CANONICAL_TO_MODEL_FEATURE = {

    # ------------------------------------------------------
    # Diabetes
    # ------------------------------------------------------

    "glucose_level": "glucose",

    "pregnancies": "pregnancies",
    "blood_pressure": "blood_pressure",
    "skin_thickness": "skin_thickness",
    "insulin": "insulin",
    "bmi": "bmi",
    "diabetes_pedigree_function": (
        "diabetes_pedigree_function"
    ),
    "age": "age",

    # ------------------------------------------------------
    # Common clinical features
    # ------------------------------------------------------

    "body_mass_index": "bmi",
    "patient_age": "age",

    # ------------------------------------------------------
    # Malnutrition
    # ------------------------------------------------------

    "age_months": "age_months",
    "weight_kg": "weight_kg",
    "height_cm": "height_cm",
    "muac_cm": "muac_cm",

    # ------------------------------------------------------
    # Vitamin D
    # ------------------------------------------------------

    "sun_exposure_hours_per_week": (
        "sun_exposure_hours_per_week"
    ),

    "physical_activity_level": (
        "physical_activity_level"
    ),

    "vitamin_d_intake_mcg_per_day": (
        "vitamin_d_intake_mcg_per_day"
    ),

    "latitude": "latitude",
    "risk_score": "risk_score",

    # ------------------------------------------------------
    # Obesity
    # ------------------------------------------------------

    "gender": "gender",
    "height": "height",
    "weight": "weight",

    "family_history_with_overweight": (
        "family_history_with_overweight"
    ),

    "favc": "favc",
    "fcvc": "fcvc",
    "ncp": "ncp",
    "caec": "caec",
    "smoke": "smoke",
    "ch2o": "ch2o",
    "scc": "scc",
    "faf": "faf",
    "tue": "tue",
    "calc": "calc",
    "mtrans": "mtrans",

    # ------------------------------------------------------
    # Metabolic
    # ------------------------------------------------------

    "chestpain": "chestpain",
    "resting_bp": "resting_bp",

    "serum_cholesterol": (
        "serum_cholesterol"
    ),

    "fasting_blood_sugar": (
        "fasting_blood_sugar"
    ),

    "resting_ecg": "resting_ecg",

    "max_heart_rate": (
        "max_heart_rate"
    ),

    "exercise_angina": (
        "exercise_angina"
    ),

    "oldpeak": "oldpeak",
    "slope": "slope",

    "number_of_major_vessels": (
        "number_of_major_vessels"
    )
}


# ==========================================================
# MODEL FEATURE → BIASGUARD INTERNAL FEATURE ADAPTER
# ==========================================================
#
# These are the exact names expected by each trained model.
#
# Example:
#
# Model expects:       Glucose
# BiasGuard has:       glucose
#
# ==========================================================

FEATURE_NAME_MAPPING = {

    # ------------------------------------------------------
    # Diabetes
    # ------------------------------------------------------

    "Pregnancies": "pregnancies",
    "Glucose": "glucose",
    "BloodPressure": "blood_pressure",
    "SkinThickness": "skin_thickness",
    "Insulin": "insulin",
    "BMI": "bmi",

    "DiabetesPedigreeFunction": (
        "diabetes_pedigree_function"
    ),

    "Age": "age",

    # ------------------------------------------------------
    # Malnutrition
    # ------------------------------------------------------

    "age_months": "age_months",
    "weight_kg": "weight_kg",
    "height_cm": "height_cm",
    "muac_cm": "muac_cm",

    # ------------------------------------------------------
    # Vitamin D
    # ------------------------------------------------------

    "Sun_Exposure_Hours_Per_Week": (
        "sun_exposure_hours_per_week"
    ),

    "Physical_Activity_Level": (
        "physical_activity_level"
    ),

    "Vitamin_D_Intake_mcg_Per_Day": (
        "vitamin_d_intake_mcg_per_day"
    ),

    "Latitude": "latitude",
    "Risk_Score": "risk_score",

    # ------------------------------------------------------
    # Obesity
    # ------------------------------------------------------

    "Gender": "gender",
    "Height": "height",
    "Weight": "weight",

    "family_history_with_overweight": (
        "family_history_with_overweight"
    ),

    "FAVC": "favc",
    "FCVC": "fcvc",
    "NCP": "ncp",
    "CAEC": "caec",
    "SMOKE": "smoke",
    "CH2O": "ch2o",
    "SCC": "scc",
    "FAF": "faf",
    "TUE": "tue",
    "CALC": "calc",
    "MTRANS": "mtrans",

    # ------------------------------------------------------
    # Metabolic
    # ------------------------------------------------------

    "age": "age",
    "gender": "gender",
    "chestpain": "chestpain",

    "restingBP": "resting_bp",

    "serumcholestrol": (
        "serum_cholesterol"
    ),

    "fastingbloodsugar": (
        "fasting_blood_sugar"
    ),

    "restingrelectro": "resting_ecg",

    "maxheartrate": "max_heart_rate",

    "exerciseangia": "exercise_angina",

    "oldpeak": "oldpeak",
    "slope": "slope",

    "noofmajorvessels": (
        "number_of_major_vessels"
    )
}


# ==========================================================
# LOAD ENDOCRINOLOGY MODELS
# ==========================================================

def load_endocrinology_models():
    """
    Load all available trained Endocrinology models.
    """

    loaded_models = {}

    print("\n" + "=" * 60)
    print("[BiasGuard AI] Loading Endocrinology models...")
    print("=" * 60)

    for disease, model_path in MODELS.items():

        model_file = os.path.join(
            model_path,
            "model.joblib"
        )

        scaler_file = os.path.join(
            model_path,
            "scaler.joblib"
        )

        if not os.path.exists(model_file):

            print(
                f"[WARNING] Model not found: "
                f"{disease}"
            )

            print(
                f"          Expected: "
                f"{model_file}"
            )

            continue

        try:

            model = joblib.load(
                model_file
            )

            scaler = None

            if os.path.exists(scaler_file):

                scaler = joblib.load(
                    scaler_file
                )

            loaded_models[disease] = {

                "model": model,
                "scaler": scaler

            }

            print(
                f"[OK] Loaded: {disease}"
            )

        except Exception as error:

            print(
                f"[ERROR] Failed to load "
                f"{disease}: {str(error)}"
            )

    print(
        f"[BiasGuard AI] Total models loaded: "
        f"{len(loaded_models)}"
    )

    print("=" * 60)

    return loaded_models


# ==========================================================
# NORMALIZE BIASGUARD CLINICAL FEATURES
# ==========================================================

def normalize_patient_features(
    standardized_features
):
    """
    Convert BiasGuard standardized clinical features into
    model-ready feature names.

    Example:

    Input:
    {
        "glucose_level": {
            "value": 145
        }
    }

    Output:
    {
        "glucose": 145.0
    }
    """

    patient_data = {}

    print("\n" + "=" * 60)
    print(
        "[BiasGuard AI] Normalizing "
        "clinical features..."
    )
    print("=" * 60)

    for feature_name, feature_data in (
        standardized_features.items()
    ):

        try:

            # ------------------------------------------
            # Get value
            # ------------------------------------------

            value = feature_data.get(
                "value"
            )

            if value is None:

                print(
                    f"[SKIPPED] {feature_name}: "
                    f"No value available"
                )

                continue

            # ------------------------------------------
            # Convert Master Schema feature name
            # to model-ready feature name
            # ------------------------------------------

            normalized_feature_name = (
                CANONICAL_TO_MODEL_FEATURE.get(
                    feature_name,
                    feature_name
                )
            )

            # ------------------------------------------
            # Convert numeric values
            # ------------------------------------------

            try:

                normalized_value = float(
                    value
                )

            except (
                ValueError,
                TypeError
            ):

                normalized_value = value

            # ------------------------------------------
            # Save normalized feature
            # ------------------------------------------

            patient_data[
                normalized_feature_name
            ] = normalized_value

            print(
                f"[MAPPED] "
                f"{feature_name} -> "
                f"{normalized_feature_name} "
                f"= {normalized_value}"
            )

        except Exception as error:

            print(
                f"[WARNING] Could not process "
                f"{feature_name}: {str(error)}"
            )

    print(
        f"[BiasGuard AI] Available model-ready "
        f"features: {list(patient_data.keys())}"
    )

    print("=" * 60)

    return patient_data


# ==========================================================
# CHECK MODEL COMPATIBILITY
# ==========================================================

def check_model_compatibility(
    patient_data,
    disease
):
    """
    Check whether all features required by a disease model
    are available.

    Missing features are NEVER replaced with zero.
    """

    required_features = get_features(
        disease
    )

    if not required_features:

        return {

            "compatible": False,

            "required_features": [],

            "missing_features": [],

            "reason": (
                "No feature mapping available "
                "for this disease"
            )
        }

    missing_features = []

    for model_feature in required_features:

        biasguard_feature = (
            FEATURE_NAME_MAPPING.get(
                model_feature,
                model_feature
            )
        )

        if (
            biasguard_feature
            not in patient_data
        ):

            missing_features.append(
                biasguard_feature
            )

    return {

        "compatible": (
            len(missing_features) == 0
        ),

        "required_features": (
            required_features
        ),

        "missing_features": (
            missing_features
        ),

        "reason": (
            None
            if not missing_features
            else (
                "Required clinical features "
                "are missing"
            )
        )
    }


# ==========================================================
# RUN SAFE DISEASE PREDICTIONS
# ==========================================================

def run_disease_predictions(
    standardized_features
):
    """
    Run predictions only when ALL required clinical features
    for a model are available.

    SAFETY RULE:
    Missing clinical features are NEVER replaced with zero
    or guessed.
    """

    # ------------------------------------------------------
    # Check input
    # ------------------------------------------------------

    if not standardized_features:

        return {

            "success": False,

            "available_features": [],

            "predictions": {},

            "message": (
                "No standardized clinical features "
                "were available for prediction."
            )
        }

    # ------------------------------------------------------
    # Normalize Master Schema features
    # ------------------------------------------------------

    patient_data = (
        normalize_patient_features(
            standardized_features
        )
    )

    # ------------------------------------------------------
    # Load models
    # ------------------------------------------------------

    models = (
        load_endocrinology_models()
    )

    results = {}

    print("\n" + "=" * 70)

    print(
        "[BiasGuard AI] RUNNING SAFE "
        "ENDOCRINOLOGY PREDICTIONS"
    )

    print("=" * 70)

    # ------------------------------------------------------
    # Check every model
    # ------------------------------------------------------

    for disease, model_info in (
        models.items()
    ):

        print(
            f"\n[BiasGuard AI] Checking model: "
            f"{disease}"
        )

        compatibility = (
            check_model_compatibility(
                patient_data,
                disease
            )
        )

        # --------------------------------------------------
        # DO NOT PREDICT IF FEATURES ARE MISSING
        # --------------------------------------------------

        if not compatibility["compatible"]:

            print(
                f"[INCOMPLETE] {disease} - "
                f"Missing "
                f"{len(compatibility['missing_features'])} "
                f"feature(s)"
            )

            results[disease] = {

                "prediction_status": (
                    "INCOMPLETE"
                ),

                "prediction": None,

                "confidence": None,

                "missing_features": (
                    compatibility[
                        "missing_features"
                    ]
                ),

                "required_features": (
                    compatibility[
                        "required_features"
                    ]
                )
            }

            continue

        # --------------------------------------------------
        # BUILD FEATURE VECTOR
        # IN EXACT MODEL FEATURE ORDER
        # --------------------------------------------------

        values = []

        for model_feature in (
            compatibility[
                "required_features"
            ]
        ):

            biasguard_feature = (
                FEATURE_NAME_MAPPING.get(
                    model_feature,
                    model_feature
                )
            )

            values.append(
                patient_data[
                    biasguard_feature
                ]
            )

        X = np.array(
            values,
            dtype=float
        ).reshape(
            1,
            -1
        )

        print(
            f"[BiasGuard AI] Input vector "
            f"for {disease}: {X}"
        )

        # --------------------------------------------------
        # APPLY SCALER
        # --------------------------------------------------

        scaler = model_info.get(
            "scaler"
        )

        if scaler is not None:

            try:

                X = scaler.transform(
                    X
                )

                print(
                    f"[BiasGuard AI] "
                    f"Scaler applied: "
                    f"{disease}"
                )

            except Exception as error:

                print(
                    f"[ERROR] Scaler failed "
                    f"for {disease}: "
                    f"{str(error)}"
                )

                results[disease] = {

                    "prediction_status": (
                        "ERROR"
                    ),

                    "prediction": None,

                    "confidence": None,

                    "missing_features": [],

                    "required_features": (
                        compatibility[
                            "required_features"
                        ]
                    ),

                    "error": (
                        f"Scaler error: "
                        f"{str(error)}"
                    )
                }

                continue

        # --------------------------------------------------
        # RUN MODEL PREDICTION
        # --------------------------------------------------

        try:

            model = model_info[
                "model"
            ]

            prediction = (
                model.predict(X)[0]
            )

            confidence = None

            if hasattr(
                model,
                "predict_proba"
            ):

                probabilities = (
                    model.predict_proba(X)[0]
                )

                confidence = float(
                    np.max(
                        probabilities
                    ) * 100
                )

            # Convert NumPy values to JSON-safe values

            if hasattr(
                prediction,
                "item"
            ):

                prediction = (
                    prediction.item()
                )

            results[disease] = {

                "prediction_status": (
                    "SUCCESS"
                ),

                "prediction": prediction,

                "confidence": confidence,

                "missing_features": [],

                "required_features": (
                    compatibility[
                        "required_features"
                    ]
                )
            }

            print(
                f"[SUCCESS] {disease}: "
                f"Prediction={prediction}, "
                f"Confidence={confidence}"
            )

        except Exception as error:

            print(
                f"[ERROR] Prediction failed "
                f"for {disease}: "
                f"{str(error)}"
            )

            results[disease] = {

                "prediction_status": (
                    "ERROR"
                ),

                "prediction": None,

                "confidence": None,

                "missing_features": [],

                "required_features": (
                    compatibility[
                        "required_features"
                    ]
                ),

                "error": str(error)
            }

    print("\n" + "=" * 70)

    print(
        "[BiasGuard AI] Prediction process finished."
    )

    print("=" * 70)

    # ------------------------------------------------------
    # RETURN COMPLETE RESULT
    # ------------------------------------------------------

    return {

        "success": True,

        "available_features": list(
            patient_data.keys()
        ),

        "predictions": results
    }