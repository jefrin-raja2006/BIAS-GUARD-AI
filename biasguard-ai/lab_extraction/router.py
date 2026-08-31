from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException

from lab_extraction.service import process_lab_report

from clinical_standardization.service import (
    standardize_clinical_parameters
)

from disease_prediction.service import (
    run_disease_predictions
)


router = APIRouter(
    prefix="/lab",
    tags=["Laboratory Extraction"]
)


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# UPLOAD DIRECTORY
# ==========================================================

UPLOAD_DIR = (
    BASE_DIR
    / "uploads"
    / "lab_reports"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# EXTRACT + STANDARDIZE + PREDICT
# ==========================================================

@router.post("/extract")
async def extract_laboratory_report(
    file: UploadFile = File(...)
):
    """
    Complete BiasGuard AI pipeline:

    1. Upload laboratory report
    2. Extract clinical parameters using AI
    3. Standardize and clinically match parameters
    4. Match standardized features with trained
       Endocrinology models
    5. Run prediction only when all required
       features are available
    """

    try:

        print("\n" + "=" * 70)
        print("[BiasGuard AI] LABORATORY PROCESSING PIPELINE")
        print("=" * 70)

        print(
            f"[BiasGuard AI] Receiving file: "
            f"{file.filename}"
        )

        # --------------------------------------------------
        # VALIDATE FILE
        # --------------------------------------------------

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file selected."
            )

        allowed_extensions = {
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg"
        }

        original_filename = file.filename

        file_extension = (
            Path(original_filename)
            .suffix
            .lower()
        )

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Please upload PDF, PNG, JPG, or JPEG."
                )
            )

        # --------------------------------------------------
        # SAVE UPLOADED FILE
        # --------------------------------------------------

        unique_filename = (
            f"{uuid4().hex}{file_extension}"
        )

        saved_file_path = (
            UPLOAD_DIR / unique_filename
        )

        print(
            f"[BiasGuard AI] Saving file to: "
            f"{saved_file_path}"
        )

        file_content = await file.read()

        with open(
            saved_file_path,
            "wb"
        ) as output_file:

            output_file.write(file_content)

        print(
            "[BiasGuard AI] File saved successfully."
        )

        print(
            f"[BiasGuard AI] File size: "
            f"{len(file_content)} bytes"
        )

        # --------------------------------------------------
        # STEP 1: EXTRACT LABORATORY DATA
        # --------------------------------------------------

        print("\n[STEP 1] Starting AI laboratory extraction...")

        extraction_result = process_lab_report(
            str(saved_file_path)
        )

        if not extraction_result:
            raise ValueError(
                "Laboratory report processing returned "
                "no result."
            )

        # --------------------------------------------------
        # GET EXTRACTED PARAMETERS
        # --------------------------------------------------

        parameters = extraction_result.get(
            "parameters",
            []
        )

        if not parameters:
            raise ValueError(
                "No clinical parameters could be extracted "
                "from the laboratory report."
            )

        print(
            f"[BiasGuard AI] Extracted "
            f"{len(parameters)} clinical parameter(s)."
        )

        # --------------------------------------------------
        # STEP 2: CLINICAL STANDARDIZATION
        # --------------------------------------------------

        print(
            "\n[STEP 2] Starting clinical feature "
            "standardization..."
        )

        clinical_standardization = (
            standardize_clinical_parameters(
                parameters
            )
        )

        if not clinical_standardization:
            raise ValueError(
                "Clinical standardization returned no result."
            )

        print(
            "[BiasGuard AI] Clinical standardization complete."
        )

        print(
            f"[BiasGuard AI] Standardized features: "
            f"{clinical_standardization.get(
                'total_standardized_features',
                0
            )}"
        )

        print(
            f"[BiasGuard AI] Review required: "
            f"{clinical_standardization.get(
                'total_review_required',
                0
            )}"
        )

        # --------------------------------------------------
        # GET STANDARDIZED FEATURES
        # --------------------------------------------------

        standardized_features = (
            clinical_standardization.get(
                "standardized_features",
                {}
            )
        )

        # --------------------------------------------------
        # STEP 3: DISEASE PREDICTION
        # --------------------------------------------------

        print(
            "\n[STEP 3] Starting Endocrinology "
            "disease prediction..."
        )

        if standardized_features:

            disease_predictions = (
                run_disease_predictions(
                    standardized_features
                )
            )

        else:

            print(
                "[WARNING] No standardized features "
                "available for disease prediction."
            )

            disease_predictions = {
                "success": False,
                "available_features": [],
                "predictions": {},
                "message": (
                    "No standardized clinical features "
                    "were available for prediction."
                )
            }

        print(
            "[BiasGuard AI] Disease prediction complete."
        )

        print("\n" + "=" * 70)
        print("[BiasGuard AI] PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)

        # --------------------------------------------------
        # RETURN COMPLETE RESULT
        # --------------------------------------------------

        return {

            "success": True,

            "message": (
                "Laboratory report extracted, clinically "
                "standardized, and checked against the "
                "Endocrinology disease prediction models."
            ),

            "original_filename": original_filename,

            "file_type": file_extension,

            # ----------------------------------------------
            # STEP 1 OUTPUT
            # ----------------------------------------------

            "extraction_result": extraction_result,

            # ----------------------------------------------
            # STEP 2 OUTPUT
            # ----------------------------------------------

            "clinical_standardization": (
                clinical_standardization
            ),

            # ----------------------------------------------
            # STEP 3 OUTPUT
            # ----------------------------------------------

            "disease_predictions": (
                disease_predictions
            )
        }


    except HTTPException:
        raise


    except Exception as error:

        print("\n" + "=" * 70)
        print(
            f"[BiasGuard AI] ERROR: {str(error)}"
        )
        print("=" * 70)

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to process laboratory report: "
                f"{str(error)}"
            )
        )