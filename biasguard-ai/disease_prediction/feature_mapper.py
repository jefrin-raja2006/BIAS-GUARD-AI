"""
BiasGuard AI - Model Feature Alias Mapper

Maps canonical clinical feature names to the exact feature
names expected by individual trained disease prediction models.
"""


MODEL_FEATURE_ALIASES = {

    "diabetes": {
        "pregnancies": "Pregnancies",
        "glucose": "Glucose",
        "blood_pressure": "BloodPressure",
        "skin_thickness": "SkinThickness",
        "insulin": "Insulin",
        "bmi": "BMI",
        "diabetes_pedigree_function": "DiabetesPedigreeFunction",
        "age": "Age"
    },

    "metabolic": {
        "age": "age",
        "gender": "gender",
        "chestpain": "chestpain",
        "resting_bp": "restingBP",
        "serum_cholesterol": "serumcholestrol",
        "fasting_blood_sugar": "fastingbloodsugar",
        "resting_ecg": "restingrelectro",
        "max_heart_rate": "maxheartrate",
        "exercise_angina": "exerciseangia",
        "oldpeak": "oldpeak",
        "slope": "slope",
        "number_of_major_vessels": "noofmajorvessels"
    }
}


def get_model_features(model_name: str) -> list[str]:
    """
    Return the canonical clinical features supported
    for a specific model.
    """
    aliases = MODEL_FEATURE_ALIASES.get(model_name.lower(), {})
    return list(aliases.keys())


def map_features_for_model(
    model_name: str,
    standardized_features: dict
) -> dict:
    """
    Convert canonical BiasGuard clinical feature names
    into the exact feature names required by a trained model.
    """

    aliases = MODEL_FEATURE_ALIASES.get(model_name.lower(), {})

    mapped_features = {}

    for canonical_name, model_feature_name in aliases.items():

        if canonical_name in standardized_features:

            feature_data = standardized_features[canonical_name]

            if isinstance(feature_data, dict):
                mapped_features[model_feature_name] = feature_data.get(
                    "value"
                )
            else:
                mapped_features[model_feature_name] = feature_data

    return mapped_features