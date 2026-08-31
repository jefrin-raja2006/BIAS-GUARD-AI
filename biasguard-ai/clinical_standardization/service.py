from typing import Dict, List, Any


def standardize_clinical_parameters(
    parameters: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Standardizes clinically matched laboratory parameters.

    Only parameters that already have a canonical_feature_name
    are converted into standardized model-ready features.
    """

    standardized_features = {}
    review_required = []

    for parameter in parameters:
        original_name = parameter.get("original_name", "")
        value = parameter.get("value")
        unit = parameter.get("unit", "")
        reference_range = parameter.get("reference_range", "")

        canonical_feature_id = parameter.get("canonical_feature_id", "")
        canonical_feature_name = parameter.get(
            "canonical_feature_name", ""
        )

        confidence_score = parameter.get(
            "confidence_score", 0
        )

        match_status = parameter.get(
            "match_status", "REVIEW_REQUIRED"
        )

        # Only safely matched clinical parameters are standardized
        if (
            match_status == "MATCHED"
            and canonical_feature_name
        ):
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                review_required.append(
                    {
                        "original_name": original_name,
                        "value": value,
                        "unit": unit,
                        "reference_range": reference_range,
                        "reason": (
                            "Parameter value could not be "
                            "converted to a numeric value"
                        )
                    }
                )
                continue

            standardized_features[
                canonical_feature_name
            ] = {
                "feature_id": canonical_feature_id,
                "feature_name": canonical_feature_name,
                "value": numeric_value,
                "original_value": str(value),
                "unit": unit,
                "reference_range": reference_range,
                "confidence_score": confidence_score,
                "original_name": original_name
            }

        else:
            review_required.append(
                {
                    "original_name": original_name,
                    "value": value,
                    "unit": unit,
                    "reference_range": reference_range,
                    "reason": (
                        "Clinical feature could not be safely "
                        "standardized"
                    )
                }
            )

    return {
        "success": True,
        "total_standardized_features": len(
            standardized_features
        ),
        "total_review_required": len(review_required),
        "standardized_features": standardized_features,
        "review_required": review_required
    }


# Optional alias for compatibility with older code
def standardize_parameters(
    parameters: List[Dict[str, Any]]
) -> Dict[str, Any]:
    return standardize_clinical_parameters(parameters)
def standardize_lab_result(parameter):
    """
    Standardize a single laboratory parameter.
    Used by the lab extraction router.
    """

    result = standardize_clinical_parameters([parameter])

    # If successfully standardized, return the standardized feature
    if result["total_standardized_features"] > 0:
        return list(
            result["standardized_features"].values()
        )[0]

    # Otherwise return the review-required result
    if result["review_required"]:
        return result["review_required"][0]

    return None