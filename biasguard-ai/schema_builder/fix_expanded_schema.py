import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "expanded_master_schema.xlsx"
OUTPUT_FILE = BASE_DIR / "master_schema_final.xlsx"


def to_snake_case(value):
    value = str(value).strip().lower()
    value = value.replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^a-z0-9_]+", "", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def main():

    print("=" * 60)
    print("BIASGUARD AI - FIXING EXPANDED MASTER SCHEMA")
    print("=" * 60)

    df = pd.read_excel(INPUT_FILE)

    # Make canonical names consistent
    df["Canonical Feature Name"] = (
        df["Canonical Feature Name"]
        .fillna("")
        .apply(to_snake_case)
    )

    # Correct clinically important terms
    corrections = {
        "mean_cytoplasmic_volume": "mean_corpuscular_volume",
        "serum_potassium": "serum_potassium",
        "platelet_count": "platelet_count",
    }

    df["Canonical Feature Name"] = (
        df["Canonical Feature Name"]
        .replace(corrections)
    )

    # Add corrected MCV terminology to synonyms
    mask = df["Dataset Feature Name"].astype(str).str.upper() == "MCV"

    df.loc[mask, "Synonyms"] = (
        "MCV, mean corpuscular volume, mean cell volume"
    )

    # Add useful synonyms for known abbreviations
    synonym_updates = {
        "hemoglobin": "Hb, Hgb, Haemoglobin, Hemoglobin",
        "hba1c": "HbA1c, Hemoglobin A1c, Glycated Hemoglobin",
        "blood_urea": "Urea, Blood Urea, Serum Urea",
        "serum_creatinine": "Creatinine, Serum Creatinine, Creat",
        "uric_acid": "Uric Acid, Serum Uric Acid",
        "alanine_aminotransferase": "ALT, SGPT, Alanine Aminotransferase",
        "aspartate_aminotransferase": "AST, SGOT, Aspartate Aminotransferase",
        "serum_sodium": "Sodium, Na, Na+",
        "serum_potassium": "Potassium, K, K+",
        "serum_chloride": "Chloride, Cl, Cl-",
        "mch": "MCH, Mean Corpuscular Hemoglobin",
        "mchc": "MCHC, Mean Corpuscular Hemoglobin Concentration",
        "red_blood_cell_count": "RBC, Red Blood Cell Count, Erythrocyte Count",
        "white_blood_cell_count": "WBC, White Blood Cell Count, Leukocyte Count",
        "platelet_count": "Platelet Count, Platelets, PLT",
    }

    for canonical_name, synonyms in synonym_updates.items():

        mask = (
            df["Canonical Feature Name"] == canonical_name
        )

        if mask.any():
            df.loc[mask, "Synonyms"] = synonyms

    # Remove exact duplicate records
    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "Feature ID",
            "Disease Model"
        ],
        keep="first"
    )

    df.to_excel(
        OUTPUT_FILE,
        index=False,
        engine="openpyxl"
    )

    print(f"Input records: {before}")
    print(f"Final records: {len(df)}")
    print(f"Output created:")
    print(OUTPUT_FILE)

    print("=" * 60)
    print("SCHEMA READY FOR LAB REPORT MATCHING")
    print("=" * 60)


if __name__ == "__main__":
    main()