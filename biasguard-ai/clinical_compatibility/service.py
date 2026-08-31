# clinical_compatibility/service.py

from clinical_compatibility.model_registry import MODEL_REGISTRY


def check_model_compatibility(standardized_features: dict):
    """
    Compare standardized clinical features against every
    registered disease prediction model.
    """

    # Get available feature names from the standardized report
    available_features = set(standardized_features.keys())

    results = []

    for model_id, model_info in MODEL_REGISTRY.items():

        required_features = set(model_info["required_features"])

        # Features required by model and available in report
        matched_features = sorted(
            available_features.intersection(required_features)
        )

        # Required model features missing from report
        missing_features = sorted(
            required_features.difference(available_features)
        )

        # Features present in report but not required by this model
        extra_features = sorted(
            available_features.difference(required_features)
        )

        total_required = len(required_features)
        total_matched = len(matched_features)

        # Calculate compatibility percentage
        if total_required > 0:
            compatibility_percentage = round(
                (total_matched / total_required) * 100,
                2
            )
        else:
            compatibility_percentage = 0.0

        minimum_compatibility = model_info.get(
            "minimum_compatibility",
            100
        )

        # Determine whether prediction can safely proceed
        if compatibility_percentage >= minimum_compatibility:
            prediction_status = "READY_FOR_PREDICTION"
        else:
            prediction_status = "INCOMPLETE"

        results.append({
            "model_id": model_id,
            "model_name": model_info["model_name"],
            "disease_group": model_info["disease_group"],
            "description": model_info["description"],

            "total_required_features": total_required,
            "matched_features_count": total_matched,
            "missing_features_count": len(missing_features),

            "matched_features": matched_features,
            "missing_features": missing_features,
            "extra_features": extra_features,

            "compatibility_percentage": compatibility_percentage,
            "minimum_compatibility": minimum_compatibility,
            "prediction_status": prediction_status
        })

    # Sort: highest compatibility first
    results.sort(
        key=lambda item: item["compatibility_percentage"],
        reverse=True
    )

    return {
        "success": True,
        "total_models_checked": len(results),
        "available_features_count": len(available_features),
        "available_features": sorted(available_features),
        "model_compatibility": results
    }