from fastapi import APIRouter, Query, HTTPException
from services.bias_service import check_bias
from disease_config import SUPPORTED_DISEASES

router = APIRouter(prefix="/bias", tags=["Bias Detection"])


@router.get("/check")
def bias_check(
    disease: str = Query(
        ...,
        description=f"Disease to check. Supported: {SUPPORTED_DISEASES}",
        example="diabetes"
    )
):
    """
    Run Fairlearn bias analysis on the specified disease model and dataset.

    Returns:
    - demographic_parity_difference (ideal = 0)
    - equalized_odds_difference (ideal = 0)
    - per-group prediction rates
    - bias_detected flag + alert for the doctor
    """
    try:
        result = check_bias(disease)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bias check failed: {str(e)}")


@router.get("/check/all")
def bias_check_all():
    """
    Run bias analysis across ALL 8 diseases and return a summary.
    Useful for a doctor dashboard overview.
    """
    results = []
    errors = []

    for disease in SUPPORTED_DISEASES:
        try:
            result = check_bias(disease)
            results.append({
                "disease": disease,
                "bias_detected": result["bias_detected"],
                "demographic_parity_difference": result["demographic_parity_difference"],
                "equalized_odds_difference": result["equalized_odds_difference"],
                "alert": result["alert"],
            })
        except Exception as e:
            errors.append({"disease": disease, "error": str(e)})

    biased_diseases = [r["disease"] for r in results if r["bias_detected"]]

    return {
        "summary": {
            "total_checked": len(results),
            "biased_count": len(biased_diseases),
            "biased_diseases": biased_diseases,
            "clean_count": len(results) - len(biased_diseases),
        },
        "results": results,
        "errors": errors,
    }