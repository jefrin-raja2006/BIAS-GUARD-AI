import os
import sys
import json
import re
from collections import defaultdict

import pandas as pd
import requests

# Allow importing disease_config.py from the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from disease_config import DISEASE_CONFIG


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"

OUTPUT_FILE = os.path.join(PROJECT_ROOT, "master_schema.xlsx")


def clean_json(text):
    """Extract JSON safely from Ollama output."""

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # Find JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        return None


def ask_ollama(feature_name, disease, related_features):
    """Ask Ollama to identify the clinical meaning of one feature."""

    prompt = f"""
You are a clinical terminology normalization assistant.

Identify the meaning of this healthcare dataset feature.

FEATURE NAME:
{feature_name}

DISEASE / DATASET CONTEXT:
{disease}

OTHER FEATURES IN THE SAME DATASET:
{", ".join(related_features)}

Rules:
1. Determine the most appropriate canonical clinical feature name.
2. Understand abbreviations and synonyms.
3. Do NOT invent medical meaning if the feature is ambiguous.
4. If uncertain, use REVIEW_REQUIRED.
5. Give confidence between 0 and 1.
6. Suggest common synonyms.
7. Suggest a standard unit only if reasonably known from the feature/context.
8. Return ONLY valid JSON.
9. All JSON keys and string values must use double quotes.

Required format:
{{
  "canonical_feature_name": "",
  "clinical_category": "",
  "synonyms": [],
  "standard_unit": "",
  "status": "MATCHED",
  "confidence_score": 0.0
}}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        data = response.json()
        result = clean_json(data.get("response", ""))

        if result is None:
            return {
                "canonical_feature_name": feature_name,
                "clinical_category": "",
                "synonyms": [],
                "standard_unit": "",
                "status": "REVIEW_REQUIRED",
                "confidence_score": 0.0
            }

        return result

    except Exception as e:
        print(f"\nOllama error for {feature_name}: {e}")

        return {
            "canonical_feature_name": feature_name,
            "clinical_category": "",
            "synonyms": [],
            "standard_unit": "",
            "status": "REVIEW_REQUIRED",
            "confidence_score": 0.0
        }


def normalize_name(name):
    """Normalize names for deterministic grouping."""

    name = str(name).lower()
    name = name.replace("_", " ")
    name = re.sub(r"[^a-z0-9\s]", "", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name


def main():

    print("=" * 60)
    print("BiasGuard AI - Automatic Clinical Master Schema Generator")
    print("=" * 60)

    records = []

    # ---------------------------------------------------------
    # STEP 1: Collect all real features from DISEASE_CONFIG
    # ---------------------------------------------------------

    print("\nReading features from DISEASE_CONFIG...\n")

    for disease, config in DISEASE_CONFIG.items():

        feature_cols = config.get("feature_cols", [])

        print(f"{disease}: {len(feature_cols)} features")

        for feature in feature_cols:

            records.append({
                "disease": disease,
                "domain": config.get("domain", ""),
                "dataset_feature_name": feature,
                "all_features": feature_cols
            })

    print(f"\nTotal dataset feature entries: {len(records)}")

    # ---------------------------------------------------------
    # STEP 2: Group identical feature names before AI calls
    # ---------------------------------------------------------

    unique_features = {}

    for record in records:

        key = normalize_name(record["dataset_feature_name"])

        if key not in unique_features:
            unique_features[key] = record

    print(f"Unique normalized features: {len(unique_features)}")

    # ---------------------------------------------------------
    # STEP 3: Ask Ollama to understand clinical terms
    # ---------------------------------------------------------

    ai_results = {}

    print("\nStarting AI clinical terminology analysis...\n")

    for index, (key, record) in enumerate(unique_features.items(), start=1):

        feature = record["dataset_feature_name"]

        print(
            f"[{index}/{len(unique_features)}] "
            f"Analyzing: {feature} "
            f"({record['disease']})"
        )

        result = ask_ollama(
            feature_name=feature,
            disease=record["disease"],
            related_features=record["all_features"]
        )

        ai_results[key] = result

        print(
            f"  -> {result.get('canonical_feature_name')} "
            f"| {result.get('status')} "
            f"| confidence={result.get('confidence_score')}"
        )

    # ---------------------------------------------------------
    # STEP 4: Build schema rows
    # ---------------------------------------------------------

    schema_rows = []

    canonical_to_id = {}
    feature_counter = 1

    for record in records:

        dataset_feature = record["dataset_feature_name"]
        key = normalize_name(dataset_feature)

        ai = ai_results[key]

        canonical_name = (
            ai.get("canonical_feature_name")
            or dataset_feature
        )

        canonical_key = normalize_name(canonical_name)

        # Give same Feature ID to same canonical feature
        if canonical_key not in canonical_to_id:

            canonical_to_id[canonical_key] = (
                f"CLN_{feature_counter:04d}"
            )

            feature_counter += 1

        feature_id = canonical_to_id[canonical_key]

        synonyms = ai.get("synonyms", [])

        if not isinstance(synonyms, list):
            synonyms = [str(synonyms)]

        schema_rows.append({
            "Feature ID": feature_id,
            "Canonical Feature Name": canonical_name,
            "Dataset Feature Name": dataset_feature,
            "Disease Model": record["disease"],
            "Domain": record["domain"],
            "Synonyms": ", ".join(map(str, synonyms)),
            "Standard Unit": ai.get("standard_unit", ""),
            "Clinical Category": ai.get(
                "clinical_category", ""
            ),
            "Status": ai.get(
                "status", "REVIEW_REQUIRED"
            ),
            "Confidence Score": ai.get(
                "confidence_score", 0.0
            )
        })

    # ---------------------------------------------------------
    # STEP 5: Create Excel file
    # ---------------------------------------------------------

    df = pd.DataFrame(schema_rows)

    df = df.sort_values(
        by=["Feature ID", "Disease Model"]
    ).reset_index(drop=True)

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            sheet_name="Master Clinical Schema",
            index=False
        )

        # Create separate review sheet
        review_df = df[
            (df["Status"] == "REVIEW_REQUIRED")
            | (df["Confidence Score"] < 0.80)
        ]

        review_df.to_excel(
            writer,
            sheet_name="Review Required",
            index=False
        )

        # Create feature summary
        summary_df = (
            df.groupby(
                ["Feature ID", "Canonical Feature Name"],
                dropna=False
            )
            .agg({
                "Dataset Feature Name":
                    lambda x: ", ".join(sorted(set(x))),
                "Disease Model":
                    lambda x: ", ".join(sorted(set(x))),
                "Status":
                    lambda x: ", ".join(sorted(set(x)))
            })
            .reset_index()
        )

        summary_df.to_excel(
            writer,
            sheet_name="Canonical Features",
            index=False
        )

    print("\n" + "=" * 60)
    print("MASTER SCHEMA GENERATED SUCCESSFULLY")
    print("=" * 60)

    print(f"\nOutput file:\n{OUTPUT_FILE}")

    print(f"\nTotal mappings: {len(df)}")
    print(
        f"Unique canonical features: "
        f"{df['Feature ID'].nunique()}"
    )

    review_count = len(
        df[
            (df["Status"] == "REVIEW_REQUIRED")
            | (df["Confidence Score"] < 0.80)
        ]
    )

    print(f"Review required: {review_count}")


if __name__ == "__main__":
    main()