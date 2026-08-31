import os
import re
import json
import uuid
from pathlib import Path

import pandas as pd
import requests
import pytesseract

from PIL import Image
from PyPDF2 import PdfReader
from pdf2image import convert_from_path


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads" / "lab_reports"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

SCHEMA_PATH = BASE_DIR / "master_schema_extended.xlsx"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

MAX_CHUNK_SIZE = 6000
OLLAMA_RETRIES = 3


# ============================================================
# WINDOWS TESSERACT CONFIGURATION
# ============================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    print(
        "[BiasGuard AI] Tesseract OCR configured successfully."
    )
else:
    print(
        "[BiasGuard AI] WARNING: Tesseract executable not found."
    )


# ============================================================
# WINDOWS POPPLER CONFIGURATION
# ============================================================

POPPLER_PATH = (
    Path.home()
    / "AppData"
    / "Local"
    / "Microsoft"
    / "WinGet"
    / "Packages"
    / "oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe"
    / "poppler-25.07.0"
    / "Library"
    / "bin"
)

if not POPPLER_PATH.exists():
    POPPLER_PATH = None


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value: str) -> str:
    """
    Convert text into a simplified comparison format.
    """

    if value is None:
        return ""

    value = str(value).lower().strip()

    value = value.replace("%", " percentage ")

    value = re.sub(
        r"[^a-z0-9]+",
        "",
        value
    )

    return value


# ============================================================
# CLINICAL NORMALIZATION
# ============================================================

def get_clinical_normalized_name(
    value: str
) -> str:
    """
    Normalize common clinical naming differences.
    """

    normalized = normalize_text(value)

    clinical_normalizations = {

        # ----------------------------------------------------
        # HEMOGLOBIN
        # ----------------------------------------------------

        "haemoglobin": "hemoglobin",
        "hb": "hemoglobin",
        "hgb": "hemoglobin",
        "hba": "hemoglobin",
        "glycosylatedhemoglobin": "hba1c",
        "hba1c": "hba1c",

        # ----------------------------------------------------
        # RBC / WBC
        # ----------------------------------------------------

        "rbc": "redbloodcellcount",
        "rbccount": "redbloodcellcount",
        "redbloodcells": "redbloodcellcount",
        "redcellcount": "redbloodcellcount",

        "wbc": "whitebloodcellcount",
        "wbccount": "whitebloodcellcount",
        "totalwbc": "whitebloodcellcount",
        "totalwhitebloodcellcount": "whitebloodcellcount",
        "totalwbcanddifferentialcount":
            "whitebloodcellcount",

        # ----------------------------------------------------
        # GLUCOSE
        # ----------------------------------------------------

        "fbs": "fastingglucose",
        "fpg": "fastingglucose",
        "fastingbloodsugar": "fastingglucose",
        "fastingplasmaglucose": "fastingglucose",
        "fastingglucose": "fastingglucose",

        "rbs": "randomglucose",
        "randombloodsugar": "randomglucose",
        "randomglucose": "randomglucose",

        # ----------------------------------------------------
        # LIVER
        # ----------------------------------------------------

        "sgpt": "alanineaminotransferase",
        "alt": "alanineaminotransferase",
        "alanineaminotransferase":
            "alanineaminotransferase",

        "sgot": "aspartateaminotransferase",
        "ast": "aspartateaminotransferase",
        "aspartateaminotransferase":
            "aspartateaminotransferase",

        # ----------------------------------------------------
        # KIDNEY
        # ----------------------------------------------------

        "creat": "serumcreatinine",
        "creatinine": "serumcreatinine",
        "creatinineserum": "serumcreatinine",
        "serumcreatinine": "serumcreatinine",

        "urea": "bloodurea",
        "serumurea": "bloodurea",
        "bloodurea": "bloodurea",

        # ----------------------------------------------------
        # ELECTROLYTES
        # ----------------------------------------------------

        "na": "serumsodium",
        "sodium": "serumsodium",
        "serumsodium": "serumsodium",

        "k": "serumpotassium",
        "potassium": "serumpotassium",
        "serumpotassium": "serumpotassium",

        "cl": "serumchloride",
        "chloride": "serumchloride",
        "serumchloride": "serumchloride",

        # ----------------------------------------------------
        # CBC
        # ----------------------------------------------------

        "plt": "plateletcount",
        "platelets": "plateletcount",
        "platelet": "plateletcount",
        "plateletcount": "plateletcount",

        "mcv": "meancorpuscularvolume",
        "meancorpuscularvolume":
            "meancorpuscularvolume",

        "mch": "meancorpuscularhemoglobin",
        "mchc":
            "meancorpuscularhemoglobinconcentration",

        "rdw": "redcelldistributionwidth",
        "rdwcv": "redcelldistributionwidth",

        "mpv": "meanplateletvolume",

        # ----------------------------------------------------
        # DIFFERENTIAL COUNT
        # ----------------------------------------------------

        "neutrophils": "neutrophilspercentage",
        "neutrophil": "neutrophilspercentage",

        "lymphocytes": "lymphocytespercentage",
        "lymphocyte": "lymphocytespercentage",

        "eosinophils": "eosinophilspercentage",
        "eosinophil": "eosinophilspercentage",

        "monocytes": "monocytespercentage",
        "monocyte": "monocytespercentage",

        # ----------------------------------------------------
        # LIPID PROFILE
        # ----------------------------------------------------

        "chol": "cholesterol",
        "serumcholesterol": "cholesterol",
        "totalcholesterol": "cholesterol",

        "triglyceride": "triglycerides",
        "triglycerides": "triglycerides",

        "hdl": "hdlcholesterol",
        "hdlcholesterol": "hdlcholesterol",

        "ldl": "ldlcholesterol",
        "ldlcholesterol": "ldlcholesterol",

        "vldl": "vldlcholesterol",
        "vldlcholesterol": "vldlcholesterol",

        # ----------------------------------------------------
        # VITAMINS
        # ----------------------------------------------------

        "vitamind": "vitamind",
        "25ohvitamind": "vitamind",
        "25hydroxyvitamind": "vitamind",
        # Hemoglobin variations and OCR errors
"hb": "hemoglobin",
"hgb": "hemoglobin",
"kb": "hemoglobin",
"haemoglobin": "hemoglobin",

# RBC variations
"rbc": "redbloodcellcount",
"rbccount": "redbloodcellcount",
"totalrbc": "redbloodcellcount",
"totalrbccount": "redbloodcellcount",
"redbloodcells": "redbloodcellcount",
"redbloodcellcount": "redbloodcellcount",

# WBC variations
"wbc": "whitebloodcellcount",
"wbccount": "whitebloodcellcount",
"totalwbc": "whitebloodcellcount",
"totalwbccount": "whitebloodcellcount",
"tlc": "whitebloodcellcount",
"wbccounttlc": "whitebloodcellcount",
"whitebloodcellcount": "whitebloodcellcount",
"totalwbcanddifferentialcount": "whitebloodcellcount",
# --------------------------------------------------
# DIABETES
# --------------------------------------------------

"hba1c": "hba1c",
"glycosylatedhemoglobin": "hba1c",
"hba1cglycosylatedhemoglobin": "hba1c",
"glycatedhemoglobin": "hba1c",


# --------------------------------------------------
# HOMOCYSTEINE
# --------------------------------------------------

"homocysteine": "homocysteine",
"homocysteineserum": "homocysteine",


# --------------------------------------------------
# KIDNEY / METABOLIC
# --------------------------------------------------

"urea": "bloodurea",
"ureal": "bloodurea",
"serumurea": "bloodurea",

"uricacid": "uricacid",
"uricacidmgdl": "uricacid",


# --------------------------------------------------
# MINERALS / ELECTROLYTES
# --------------------------------------------------

"calcium": "serumcalcium",
"calciummgdl": "serumcalcium",
"serumcalcium": "serumcalcium",

"sodium": "serumsodium",
"sodiummmoll": "serumsodium",

"potassium": "serumpotassium",
"potassiummmoll": "serumpotassium",

"chloride": "serumchloride",
"chloridemmoll": "serumchloride",


# --------------------------------------------------
# LIVER ENZYMES
# --------------------------------------------------

"sgpt": "alanineaminotransferase",
"sgptul": "alanineaminotransferase",
"alt": "alanineaminotransferase",

"sgot": "aspartateaminotransferase",
"sgotul": "aspartateaminotransferase",
"ast": "aspartateaminotransferase",


# --------------------------------------------------
# VITAMIN D
# --------------------------------------------------

"25ohvitamind": "vitamind",
"25ohvitamindngml": "vitamind",
"vitamind": "vitamind",
"vitamindngml": "vitamind",


# --------------------------------------------------
# PROSTATE
# --------------------------------------------------

"psa": "prostatespecificantigen",
"prostatespecificantigen": "prostatespecificantigen",
"psa": "prostatespecificantigen",
"prostatespecificantigen": "prostatespecificantigen",

# --------------------------------------------------
# HEMOGLOBIN FRACTIONS
# --------------------------------------------------

"hba2": "hemoglobina2",
"hba2percentage": "hemoglobina2",
"hemoglobina2": "hemoglobina2",
"hemoglobina2percentage": "hemoglobina2",

        "vitaminb12": "vitaminb12",
        "b12": "vitaminb12",

        # ----------------------------------------------------
        # OTHER
        # ----------------------------------------------------

        "ige": "immunoglobuline",
        "immunoglobuline": "immunoglobuline",

        "psa": "prostatespecificantigen",
        "prostatespecificantigen":
            "prostatespecificantigen",

        "urineglucose": "urineglucose",
    }

    return clinical_normalizations.get(
        normalized,
        normalized
    )


# ============================================================
# FIND SCHEMA COLUMN
# ============================================================

def find_column(
    records: list,
    possible_names: list
):
    """
    Find a column name from possible alternatives.
    """

    if not records:
        return None

    available_columns = records[0].keys()

    normalized_columns = {
        normalize_text(column): column
        for column in available_columns
    }

    for name in possible_names:

        normalized_name = normalize_text(name)

        if normalized_name in normalized_columns:
            return normalized_columns[
                normalized_name
            ]

    return None


# ============================================================
# LOAD MASTER SCHEMA
# ============================================================

def load_master_schema() -> list:
    """
    Load Master Clinical Schema Excel file.
    """

    if not SCHEMA_PATH.exists():

        raise FileNotFoundError(
            f"Master schema not found: {SCHEMA_PATH}"
        )

    print(
        f"[BiasGuard AI] Loading schema: "
        f"{SCHEMA_PATH.name}"
    )

    dataframe = pd.read_excel(
        SCHEMA_PATH
    )

    dataframe = dataframe.fillna("")

    records = dataframe.to_dict(
        orient="records"
    )

    print(
        f"[BiasGuard AI] Loaded "
        f"{len(records)} schema records"
    )

    return records


# ============================================================
# DIGITAL PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(
    file_path: str
) -> str:
    """
    Extract embedded text from a digital PDF.
    """

    reader = PdfReader(file_path)

    extracted_text = []

    for page in reader.pages:

        try:

            page_text = page.extract_text()

            if page_text:
                extracted_text.append(
                    page_text
                )

        except Exception as error:

            print(
                f"[BiasGuard AI] PDF page extraction "
                f"warning: {error}"
            )

    return "\n".join(
        extracted_text
    ).strip()


# ============================================================
# IMAGE OCR
# ============================================================

def extract_text_from_image(
    file_path: str
) -> str:
    """
    Extract text from image using Tesseract.
    """

    image = Image.open(
        file_path
    )

    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text.strip()


# ============================================================
# PDF OCR FALLBACK
# ============================================================

def extract_text_from_scanned_pdf(
    file_path: str
) -> str:
    """
    Convert scanned PDF pages to images
    and run Tesseract OCR.
    """

    print(
        "[BiasGuard AI] Starting OCR fallback "
        "for scanned PDF..."
    )

    try:

        convert_kwargs = {
            "dpi": 300
        }

        if POPPLER_PATH:
            convert_kwargs[
                "poppler_path"
            ] = str(POPPLER_PATH)

        pages = convert_from_path(
            file_path,
            **convert_kwargs
        )

    except Exception as error:

        raise RuntimeError(
            "Unable to convert PDF pages for OCR. "
            f"Error: {error}"
        )

    extracted_pages = []

    total_pages = len(
        pages
    )

    for index, page in enumerate(
        pages,
        start=1
    ):

        print(
            f"[BiasGuard AI] OCR processing "
            f"page {index}/{total_pages}"
        )

        try:

            text = pytesseract.image_to_string(
                page,
                config="--psm 6"
            )

            if text.strip():

                extracted_pages.append(
                    text
                )

        except Exception as error:

            print(
                f"[BiasGuard AI] OCR warning "
                f"on page {index}: {error}"
            )

    return "\n".join(
        extracted_pages
    ).strip()


# ============================================================
# UNIVERSAL TEXT EXTRACTION
# ============================================================

def extract_report_text(
    file_path: str
) -> str:
    """
    Extract report text from PDF or image.
    """

    extension = (
        Path(file_path)
        .suffix
        .lower()
    )

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if extension == ".pdf":

        print(
            "[BiasGuard AI] Trying normal "
            "PDF text extraction..."
        )

        text = extract_text_from_pdf(
            file_path
        )

        if text.strip():

            print(
                "[BiasGuard AI] Digital PDF text "
                "extraction successful."
            )

            return text.strip()

        print(
            "[BiasGuard AI] No embedded PDF text found."
        )

        text = extract_text_from_scanned_pdf(
            file_path
        )

        if text.strip():

            print(
                "[BiasGuard AI] Scanned PDF OCR "
                "extraction successful."
            )

        return text.strip()

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    if extension in [
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff"
    ]:

        print(
            "[BiasGuard AI] Starting image OCR..."
        )

        return extract_text_from_image(
            file_path
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


# ============================================================
# CLEAN EXTRACTED TEXT
# ============================================================

def clean_extracted_text(
    text: str
) -> str:
    """
    Clean common OCR formatting issues.
    """

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# CHUNK TEXT
# ============================================================

def chunk_text(
    text: str,
    max_chunk_size: int = MAX_CHUNK_SIZE
) -> list:
    """
    Split report text into manageable chunks.
    """

    if len(text) <= max_chunk_size:

        return [text]

    chunks = []

    current_chunk = ""

    lines = text.splitlines()

    for line in lines:

        if (
            len(current_chunk)
            + len(line)
            + 1
            > max_chunk_size
        ):

            if current_chunk.strip():

                chunks.append(
                    current_chunk.strip()
                )

            current_chunk = line

        else:

            current_chunk += (
                "\n"
                + line
            )

    if current_chunk.strip():

        chunks.append(
            current_chunk.strip()
        )

    return chunks


# ============================================================
# CLEAN LLM JSON RESPONSE
# ============================================================

def clean_json_response(
    response_text: str
):
    """
    Extract JSON safely from LLM response.
    """

    if not response_text:
        return []

    response_text = response_text.strip()

    response_text = re.sub(
        r"^```json",
        "",
        response_text,
        flags=re.IGNORECASE
    )

    response_text = re.sub(
        r"^```",
        "",
        response_text
    )

    response_text = re.sub(
        r"```$",
        "",
        response_text
    )

    response_text = response_text.strip()

    try:

        parsed = json.loads(
            response_text
        )

        if isinstance(
            parsed,
            dict
        ):

            if "parameters" in parsed:

                parsed = parsed[
                    "parameters"
                ]

        if isinstance(
            parsed,
            list
        ):

            return parsed

    except Exception:
        pass

    # Find JSON array inside response

    match = re.search(
        r"\[[\s\S]*\]",
        response_text
    )

    if match:

        try:

            return json.loads(
                match.group(0)
            )

        except Exception:
            return []

    return []


# ============================================================
# OLLAMA REQUEST
# ============================================================

def call_ollama(
    prompt: str
) -> str:
    """
    Send prompt to Ollama.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        ""
    )


# ============================================================
# PRIMARY CLINICAL EXTRACTION
# ============================================================

def extract_parameters_with_ollama(
    text: str
) -> list:
    """
    Extract laboratory parameters using Ollama.
    """

    prompt = f"""
You are a clinical laboratory data extraction system.

Extract ONLY actual laboratory test parameters from the
following laboratory report text.

For each parameter return:

- original_name
- value
- unit
- reference_range

IMPORTANT RULES:

1. Extract every laboratory measurement you can identify.
2. Do not invent values.
3. Ignore patient names, dates, addresses, doctors,
   laboratory names and administrative information.
4. Preserve the test name as written in the report.
5. Return valid JSON only.
6. Return a JSON object with this structure:

{{
  "parameters": [
    {{
      "original_name": "Hemoglobin",
      "value": "14.5",
      "unit": "g/dL",
      "reference_range": "13.0-17.0"
    }}
  ]
}}

LAB REPORT TEXT:

{text}
"""

    for attempt in range(
        1,
        OLLAMA_RETRIES + 1
    ):

        try:

            print(
                f"[BiasGuard AI] Chunk "
                f"- Ollama attempt "
                f"{attempt}/{OLLAMA_RETRIES}"
            )

            print(
                "[BiasGuard AI] Sending extraction "
                "request to Ollama..."
            )

            response_text = call_ollama(
                prompt
            )

            parameters = clean_json_response(
                response_text
            )

            if parameters:

                return parameters

        except Exception as error:

            print(
                f"[BiasGuard AI] Ollama attempt "
                f"{attempt}/{OLLAMA_RETRIES} "
                f"failed: {error}"
            )

    return []


# ============================================================
# OCR-FOCUSED SECOND AI EXTRACTION
# ============================================================

def extract_parameters_from_ocr_text(
    text: str
) -> list:
    """
    Second extraction prompt for imperfect OCR text.
    """

    prompt = f"""
You are reading OCR output from a medical laboratory report.

OCR may contain spelling mistakes, broken lines,
incorrect spacing, and characters such as:

I instead of 1
O instead of 0
l instead of 1

Identify laboratory test results despite these OCR errors.

Extract every line that appears to contain:

TEST NAME + VALUE

The unit and reference range are optional.

Return JSON only:

{{
  "parameters": [
    {{
      "original_name": "",
      "value": "",
      "unit": "",
      "reference_range": ""
    }}
  ]
}}

Do not return explanations.

OCR TEXT:

{text}
"""

    try:

        response_text = call_ollama(
            prompt
        )

        return clean_json_response(
            response_text
        )

    except Exception as error:

        print(
            "[BiasGuard AI] OCR-focused extraction "
            f"failed: {error}"
        )

        return []


# ============================================================
# SIMPLE RULE-BASED FALLBACK
# ============================================================

def rule_based_extraction(
    text: str
) -> list:
    """
    Last-resort extraction from OCR text.

    Looks for lines containing a likely clinical test name
    followed by a numeric result.
    """

    parameters = []

    known_tests = [
        "hemoglobin",
        "haemoglobin",
        "rbc",
        "wbc",
        "hematocrit",
        "pcv",
        "mcv",
        "mch",
        "mchc",
        "rdw",
        "platelet",
        "mpv",
        "neutrophils",
        "lymphocytes",
        "eosinophils",
        "monocytes",
        "basophils",
        "glucose",
        "blood sugar",
        "hba1c",
        "creatinine",
        "urea",
        "uric acid",
        "sodium",
        "potassium",
        "chloride",
        "calcium",
        "sgpt",
        "sgot",
        "alt",
        "ast",
        "cholesterol",
        "triglycerides",
        "hdl",
        "ldl",
        "vitamin d",
        "vitamin b12",
        "psa"
    ]

    for line in text.splitlines():

        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        line_lower = cleaned_line.lower()

        matched_test = None

        for test in known_tests:

            if test in line_lower:

                matched_test = test
                break

        if not matched_test:
            continue

        number_match = re.search(
            r"(?<![A-Za-z])"
            r"[-+]?\d+(?:\.\d+)?"
            r"(?![A-Za-z])",
            cleaned_line
        )

        if not number_match:
            continue

        value = number_match.group(0)

        remainder = cleaned_line[
            number_match.end():
        ].strip()

        unit = ""

        unit_match = re.match(
            r"([A-Za-z/%µμ^0-9]+(?:/[A-Za-z0-9]+)?)",
            remainder
        )

        if unit_match:

            unit = unit_match.group(
                1
            )

        parameters.append(
            {
                "original_name": matched_test,
                "value": value,
                "unit": unit,
                "reference_range": ""
            }
        )

    return parameters


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicate_parameters(
    parameters: list
) -> list:
    """
    Remove duplicate extracted parameters.
    """

    unique_parameters = []

    seen = set()

    for parameter in parameters:

        original_name = str(
            parameter.get(
                "original_name",
                ""
            )
        ).strip()

        value = str(
            parameter.get(
                "value",
                ""
            )
        ).strip()

        key = (
            get_clinical_normalized_name(
                original_name
            ),
            value
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        unique_parameters.append(
            {
                "original_name":
                    original_name,

                "value":
                    value,

                "unit":
                    str(
                        parameter.get(
                            "unit",
                            ""
                        )
                    ).strip(),

                "reference_range":
                    str(
                        parameter.get(
                            "reference_range",
                            ""
                        )
                    ).strip()
            }
        )

    return unique_parameters


# ============================================================
# MATCH PARAMETER TO MASTER SCHEMA
# ============================================================

def match_parameter_to_schema(
    parameter: dict,
    schema_records: list
) -> dict:
    """
    Match an extracted clinical/laboratory parameter against
    the Master Clinical Schema.

    Matching priority:
    1. Dataset Feature Name
    2. Canonical Feature Name
    3. Synonyms
    """

    original_name = parameter.get(
        "original_name",
        ""
    ).strip()

    normalized_input = get_clinical_normalized_name(
        original_name
    )

    print(
        f"[BiasGuard AI] Matching parameter: "
        f"{original_name} -> {normalized_input}"
    )

    # --------------------------------------------------
    # Helper: normalize any schema column name
    # Example:
    # "Canonical Feature Name"
    # -> "canonical_feature_name"
    # --------------------------------------------------

    def normalize_column_name(column_name):
        return (
            str(column_name)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )

    # --------------------------------------------------
    # Helper: safely get value from a row
    # --------------------------------------------------

    def get_row_value(row, possible_columns):

        normalized_columns = {}

        for key in row.keys():
            normalized_key = normalize_column_name(key)
            normalized_columns[normalized_key] = key

        for possible_column in possible_columns:

            normalized_possible = normalize_column_name(
                possible_column
            )

            if normalized_possible in normalized_columns:

                original_key = normalized_columns[
                    normalized_possible
                ]

                value = row.get(original_key, "")

                if value is not None:
                    return str(value).strip()

        return ""

    # --------------------------------------------------
    # Search every schema record
    # --------------------------------------------------

    for row in schema_records:

        # ----------------------------------------------
        # Get schema values
        # ----------------------------------------------

        feature_id = get_row_value(
            row,
            [
                "Feature ID",
                "feature_id",
                "canonical_feature_id",
                "id"
            ]
        )

        canonical_name = get_row_value(
            row,
            [
                "Canonical Feature Name",
                "canonical_feature_name",
                "canonical_name",
                "standardized_feature_name"
            ]
        )

        database_feature_name = get_row_value(
            row,
            [
                "Dataset Feature Name",
                "Database Feature Name",
                "dataset_feature_name",
                "database_feature_name",
                "original_feature_name",
                "feature_name"
            ]
        )

        synonyms = get_row_value(
            row,
            [
                "Synonyms",
                "synonyms",
                "synonym",
                "alternative_names",
                "aliases"
            ]
        )

        # ----------------------------------------------
        # Normalize values for comparison
        # ----------------------------------------------

        normalized_canonical = (
            get_clinical_normalized_name(canonical_name)
            if canonical_name
            else ""
        )

        normalized_database = (
            get_clinical_normalized_name(
                database_feature_name
            )
            if database_feature_name
            else ""
        )

        # ==============================================
        # MATCH 1: DATASET FEATURE NAME
        # Example: Glucose -> Glucose
        # ==============================================

        if (
            normalized_database
            and normalized_input == normalized_database
        ):

            print(
                f"[MATCHED] {original_name} matched "
                f"Dataset Feature Name: "
                f"{database_feature_name}"
            )

            return {
                **parameter,
                "canonical_feature_id": feature_id,
                "canonical_feature_name": canonical_name,
                "database_feature_name": (
                    database_feature_name
                ),
                "match_status": "MATCHED",
                "match_method": "EXACT_DATASET_FEATURE_MATCH",
                "confidence_score": 1.0
            }

        # ==============================================
        # MATCH 2: CANONICAL FEATURE NAME
        # ==============================================

        if (
            normalized_canonical
            and normalized_input == normalized_canonical
        ):

            print(
                f"[MATCHED] {original_name} matched "
                f"Canonical Feature Name: "
                f"{canonical_name}"
            )

            return {
                **parameter,
                "canonical_feature_id": feature_id,
                "canonical_feature_name": canonical_name,
                "database_feature_name": (
                    database_feature_name
                ),
                "match_status": "MATCHED",
                "match_method": "EXACT_CANONICAL_MATCH",
                "confidence_score": 1.0
            }

        # ==============================================
        # MATCH 3: SYNONYMS
        # ==============================================

        if synonyms:

            synonym_list = (
                synonyms
                .replace(";", ",")
                .split(",")
            )

            for synonym in synonym_list:

                synonym = synonym.strip()

                if not synonym:
                    continue

                normalized_synonym = (
                    get_clinical_normalized_name(
                        synonym
                    )
                )

                if (
                    normalized_input
                    == normalized_synonym
                ):

                    print(
                        f"[MATCHED] {original_name} "
                        f"matched synonym: {synonym}"
                    )

                    return {
                        **parameter,
                        "canonical_feature_id": (
                            feature_id
                        ),
                        "canonical_feature_name": (
                            canonical_name
                        ),
                        "database_feature_name": (
                            database_feature_name
                        ),
                        "match_status": "MATCHED",
                        "match_method": "SYNONYM_MATCH",
                        "confidence_score": 0.95
                    }

    # --------------------------------------------------
    # No safe match found
    # --------------------------------------------------

    print(
        f"[REVIEW REQUIRED] No schema match found "
        f"for: {original_name}"
    )

    return {
        **parameter,
        "canonical_feature_id": "",
        "canonical_feature_name": "",
        "database_feature_name": "",
        "match_status": "REVIEW_REQUIRED",
        "match_method": "REVIEW_REQUIRED",
        "confidence_score": 0
    }
    # --------------------------------------------------------
    # EXACT / CLINICAL NORMALIZED MATCH
    # --------------------------------------------------------

    for row in schema_records:

        values_to_check = []

        if canonical_name_col:

            value = str(
                row.get(
                    canonical_name_col,
                    ""
                )
            ).strip()

            if value:

                values_to_check.append(
                    value
                )

        if database_name_col:

            value = str(
                row.get(
                    database_name_col,
                    ""
                )
            ).strip()

            if value:

                values_to_check.append(
                    value
                )

        for value in values_to_check:

            normalized_schema_value = (
                get_clinical_normalized_name(
                    value
                )
            )

            if (
                normalized_schema_value
                == normalized_input
            ):

                return {

                    "canonical_feature_id":
                        row.get(
                            canonical_id_col,
                            ""
                        )
                        if canonical_id_col
                        else "",

                    "canonical_feature_name":
                        row.get(
                            canonical_name_col,
                            ""
                        )
                        if canonical_name_col
                        else "",

                    "database_feature_name":
                        row.get(
                            database_name_col,
                            ""
                        )
                        if database_name_col
                        else "",

                    "match_status":
                        "MATCHED",

                    "match_method":
                        "EXACT",

                    "confidence_score":
                        1.0
                }

    # --------------------------------------------------------
    # SYNONYM MATCH
    # --------------------------------------------------------

    if synonym_col:

        for row in schema_records:

            synonyms = str(
                row.get(
                    synonym_col,
                    ""
                )
            )

            synonym_list = re.split(
                r"[,;|/]",
                synonyms
            )

            for synonym in synonym_list:

                normalized_synonym = (
                    get_clinical_normalized_name(
                        synonym
                    )
                )

                if (
                    normalized_synonym
                    == normalized_input
                ):

                    return {

                        "canonical_feature_id":
                            row.get(
                                canonical_id_col,
                                ""
                            )
                            if canonical_id_col
                            else "",

                        "canonical_feature_name":
                            row.get(
                                canonical_name_col,
                                ""
                            )
                            if canonical_name_col
                            else "",

                        "database_feature_name":
                            row.get(
                                database_name_col,
                                ""
                            )
                            if database_name_col
                            else "",

                        "match_status":
                            "MATCHED",

                        "match_method":
                            "SYNONYM",

                        "confidence_score":
                            0.98
                    }

    # --------------------------------------------------------
    # REVIEW REQUIRED
    # --------------------------------------------------------

    return {

        "canonical_feature_id": "",
        "canonical_feature_name": "",
        "database_feature_name": "",

        "match_status":
            "REVIEW_REQUIRED",

        "match_method":
            "REVIEW_REQUIRED",

        "confidence_score":
            0.0
    }


# ============================================================
# COMPLETE LAB REPORT PIPELINE
# ============================================================

def process_lab_report(
    file_path: str
) -> dict:
    """
    Complete BiasGuard AI laboratory pipeline.
    """

    print(
        "\n"
        "============================================================"
    )

    print(
        "[BiasGuard AI] Starting lab report processing..."
    )

    print(
        "============================================================"
    )

    # --------------------------------------------------------
    # EXTRACT TEXT
    # --------------------------------------------------------

    extracted_text = extract_report_text(
        file_path
    )

    extracted_text = clean_extracted_text(
        extracted_text
    )

    if not extracted_text:

        raise ValueError(
            "No readable text could be extracted "
            "from the laboratory report."
        )

    print(
        f"[BiasGuard AI] Extracted "
        f"{len(extracted_text)} characters from report"
    )

    # --------------------------------------------------------
    # SHOW EXTRACTED / OCR TEXT PREVIEW
    # --------------------------------------------------------

    print(
        "\n[BiasGuard AI] OCR / EXTRACTED TEXT PREVIEW:"
    )

    print(
        "=" * 60
    )

    print(
        extracted_text[:3000]
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # CHUNK REPORT
    # --------------------------------------------------------

    chunks = chunk_text(
        extracted_text
    )

    print(
        f"[BiasGuard AI] Processing complete report: "
        f"{len(extracted_text)} characters in "
        f"{len(chunks)} chunks"
    )

    all_parameters = []

    failed_chunks = 0

    # --------------------------------------------------------
    # PROCESS EACH CHUNK
    # --------------------------------------------------------

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"\n[BiasGuard AI] Processing chunk "
            f"{index}/{len(chunks)} "
            f"({len(chunk)} characters)"
        )

        # Primary AI extraction

        parameters = (
            extract_parameters_with_ollama(
                chunk
            )
        )

        # Second OCR-focused extraction

        if not parameters:

            print(
                "[BiasGuard AI] No parameters found. "
                "Retrying with OCR-focused extraction prompt..."
            )

            parameters = (
                extract_parameters_from_ocr_text(
                    chunk
                )
            )

        # Rule-based fallback

        if not parameters:

            print(
                "[BiasGuard AI] AI extraction returned "
                "no parameters. Trying rule-based fallback..."
            )

            parameters = rule_based_extraction(
                chunk
            )

        if not parameters:

            failed_chunks += 1

            print(
                f"[BiasGuard AI] Chunk {index}: "
                "extracted 0 parameters"
            )

            continue

        print(
            f"[BiasGuard AI] Chunk {index}: "
            f"extracted {len(parameters)} parameters"
        )

        all_parameters.extend(
            parameters
        )

    # --------------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------------

    raw_count = len(
        all_parameters
    )

    unique_parameters = (
        remove_duplicate_parameters(
            all_parameters
        )
    )

    print(
        f"\n[BiasGuard AI] Total extraction complete: "
        f"{raw_count} raw parameters | "
        f"{len(unique_parameters)} unique parameters | "
        f"{failed_chunks} failed chunks"
    )

    if not unique_parameters:

        raise ValueError(
            "No clinical parameters could be extracted "
            "from the laboratory report."
        )

    # --------------------------------------------------------
    # LOAD MASTER SCHEMA
    # --------------------------------------------------------

    schema_records = load_master_schema()

    # --------------------------------------------------------
    # MATCH PARAMETERS
    # --------------------------------------------------------

    final_parameters = []

    unmatched_parameters = []

    matched_count = 0

    for parameter in unique_parameters:

        match_result = (
            match_parameter_to_schema(
                parameter,
                schema_records
            )
        )

        final_parameter = {

            "original_name":
                parameter.get(
                    "original_name",
                    ""
                ),

            "value":
                parameter.get(
                    "value",
                    ""
                ),

            "unit":
                parameter.get(
                    "unit",
                    ""
                ),

            "reference_range":
                parameter.get(
                    "reference_range",
                    ""
                ),

            **match_result
        }

        final_parameters.append(
            final_parameter
        )

        if (
            match_result[
                "match_status"
            ]
            == "MATCHED"
        ):

            matched_count += 1

        else:

            unmatched_parameters.append(
                parameter.get(
                    "original_name",
                    ""
                )
            )

    review_required_count = (
        len(unmatched_parameters)
    )

    # --------------------------------------------------------
    # SHOW UNMATCHED PARAMETERS
    # --------------------------------------------------------

    if unmatched_parameters:

        print(
            "\n[BiasGuard AI] Unmatched parameters:"
        )

        for parameter_name in unmatched_parameters:

            print(
                f"  - {parameter_name}"
            )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    print(
        "\n[BiasGuard AI] Processing complete: "
        f"{len(final_parameters)} extracted | "
        f"{matched_count} matched | "
        f"{review_required_count} review required"
    )

    print(
        "============================================================"
    )

    return {

        "success": True,

        "total_extracted":
            len(final_parameters),

        "matched_count":
            matched_count,

        "review_required_count":
            review_required_count,

        "failed_chunks":
            failed_chunks,

        "parameters":
            final_parameters,

        "unmatched_parameters":
            unmatched_parameters
    }


# ============================================================
# SAVE UPLOADED FILE
# ============================================================

def save_uploaded_file(
    file_content: bytes,
    original_filename: str
) -> str:
    """
    Save uploaded laboratory report.
    """

    extension = Path(
        original_filename
    ).suffix.lower()

    unique_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = (
        UPLOAD_DIR
        / unique_filename
    )

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            file_content
        )

    return str(
        file_path
    )