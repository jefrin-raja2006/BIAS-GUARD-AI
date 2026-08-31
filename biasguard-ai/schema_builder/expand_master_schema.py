import json
import re
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "master_schema.xlsx"
OUTPUT_FILE = BASE_DIR / "expanded_master_schema.xlsx"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"


# ------------------------------------------------------------
# CLINICAL LAB FEATURES TO ADD
# ------------------------------------------------------------

CLINICAL_FEATURES = [
    "Hemoglobin",
    "HbA1c",
    "Fetal Hemoglobin",
    "Blood Urea",
    "Serum Creatinine",
    "Uric Acid",
    "Serum Calcium",
    "Serum Phosphorus",
    "Alanine Aminotransferase",
    "Aspartate Aminotransferase",
    "Serum Sodium",
    "Serum Potassium",
    "Serum Chloride",
    "MCV",
    "MCH",
    "MCHC",
    "Red Blood Cell Count",
    "White Blood Cell Count",
    "Platelet Count"
]


def normalize_text(value):
    """Normalize a name for duplicate checking."""
    return re.sub(
        r"[^a-z0-9]+",
        "",
        str(value).lower()
    )


def extract_json(text):
    """Extract JSON safely from Ollama output."""

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON found in Ollama response")

    return json.loads(text[start:end + 1])


def ask_ollama(feature_name):
    """Ask Ollama to standardize one clinical feature."""

    prompt = f"""
You are a clinical terminology normalization engine.

Standardize this clinical laboratory parameter:

"{feature_name}"

Return ONLY valid JSON.

Use exactly this format:

{{
    "canonical_feature_name": "snake_case_standard_name",
    "synonyms": ["clinical synonym 1", "abbreviation"],
    "standard_unit": "unit or empty string",
    "clinical_category": "category"
}}

Rules:
- Use medically correct terminology.
- canonical_feature_name must be lowercase snake_case.
- Include common abbreviations and alternative names.
- Do not invent unrelated tests.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0
            }
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()
    text = result.get("response", "")

    return extract_json(text)


def main():

    print("=" * 60)
    print("BIASGUARD AI - MASTER SCHEMA EXPANSION")
    print("=" * 60)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Master schema not found: {INPUT_FILE}"
        )

    df = pd.read_excel(INPUT_FILE)

    print(f"Loaded {len(df)} existing schema records")

    existing_names = set(
        df["Canonical Feature Name"]
        .fillna("")
        .apply(normalize_text)
    )

    new_records = []

    next_id_number = 1

    existing_ids = df["Feature ID"].dropna().astype(str).tolist()

    numbers = []

    for feature_id in existing_ids:
        match = re.search(r"(\d+)$", feature_id)

        if match:
            numbers.append(int(match.group(1)))

    if numbers:
        next_id_number = max(numbers) + 1

    for index, feature in enumerate(
        CLINICAL_FEATURES,
        start=1
    ):

        normalized_feature = normalize_text(feature)

        print(
            f"\n[{index}/{len(CLINICAL_FEATURES)}] "
            f"Checking: {feature}"
        )

        if normalized_feature in existing_names:

            print(
                "  -> Already exists. Skipping."
            )

            continue

        try:

            result = ask_ollama(feature)

            canonical_name = str(
                result.get(
                    "canonical_feature_name",
                    ""
                )
            ).strip()

            synonyms = result.get(
                "synonyms",
                []
            )

            if not isinstance(synonyms, list):
                synonyms = []

            synonyms_text = ", ".join(
                str(item).strip()
                for item in synonyms
                if str(item).strip()
            )

            standard_unit = str(
                result.get(
                    "standard_unit",
                    ""
                )
            ).strip()

            clinical_category = str(
                result.get(
                    "clinical_category",
                    "laboratory"
                )
            ).strip()

            if not canonical_name:

                print(
                    "  -> Invalid AI result. Skipping."
                )

                continue

            if normalize_text(
                canonical_name
            ) in existing_names:

                print(
                    f"  -> Canonical feature "
                    f"already exists: {canonical_name}"
                )

                continue

            feature_id = (
                f"CLN_{next_id_number:04d}"
            )

            new_record = {
                "Feature ID": feature_id,
                "Canonical Feature Name": canonical_name,
                "Dataset Feature Name": feature,
                "Disease Model": "general_clinical",
                "Domain": "clinical_laboratory",
                "Synonyms": synonyms_text,
                "Standard Unit": standard_unit,
                "Clinical Category": clinical_category,
                "Status": "AI_ADDED",
                "Confidence Score": 0.90
            }

            new_records.append(
                new_record
            )

            existing_names.add(
                normalize_text(canonical_name)
            )

            next_id_number += 1

            print(
                f"  -> Added: "
                f"{canonical_name}"
            )

        except Exception as e:

            print(
                f"  -> Failed: {e}"
            )

    if new_records:

        new_df = pd.DataFrame(
            new_records
        )

        expanded_df = pd.concat(
            [df, new_df],
            ignore_index=True
        )

    else:

        expanded_df = df.copy()

    expanded_df.to_excel(
        OUTPUT_FILE,
        index=False,
        engine="openpyxl"
    )

    print("\n" + "=" * 60)
    print("MASTER SCHEMA EXPANSION COMPLETE")
    print("=" * 60)
    print(
        f"Existing records: {len(df)}"
    )
    print(
        f"New clinical features added: "
        f"{len(new_records)}"
    )
    print(
        f"Total records: "
        f"{len(expanded_df)}"
    )
    print(
        f"Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()