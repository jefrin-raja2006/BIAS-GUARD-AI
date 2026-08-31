import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "master_schema_final.xlsx"

OUTPUT_FILE = BASE_DIR / "master_schema_extended.xlsx"


# ============================================================
# NEW CLINICAL FEATURES
# ============================================================

NEW_FEATURES = [

    # --------------------------------------------------------
    # HEMATOLOGY
    # --------------------------------------------------------

    {
        "Canonical Feature Name": "hematocrit",
        "Dataset Feature Name": "Hematocrit",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "hct,packed_cell_volume,pcv",
        "Standard Unit": "%",
        "Clinical Category": "hematology"
    },

    {
        "Canonical Feature Name": "red_cell_distribution_width",
        "Dataset Feature Name": "RDW CV",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "rdw,rdw_cv,red_cell_distribution_width",
        "Standard Unit": "%",
        "Clinical Category": "hematology"
    },

    {
        "Canonical Feature Name": "neutrophils_percentage",
        "Dataset Feature Name": "Neutrophils %",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "neutrophils,neutrophil_percent,neutrophils_percentage",
        "Standard Unit": "%",
        "Clinical Category": "hematology"
    },

    {
        "Canonical Feature Name": "lymphocytes_percentage",
        "Dataset Feature Name": "Lymphocytes %",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "lymphocytes,lymphocyte_percent,lymphocytes_percentage",
        "Standard Unit": "%",
        "Clinical Category": "hematology"
    },

    {
        "Canonical Feature Name": "eosinophils_percentage",
        "Dataset Feature Name": "Eosinophils %",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "eosinophils,eosinophil_percent,eosinophils_percentage",
        "Standard Unit": "%",
        "Clinical Category": "hematology"
    },

    {
        "Canonical Feature Name": "monocytes_percentage",
        "Dataset Feature Name": "Monocytes %",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "monocytes,monocyte_percent,monocytes_percentage",
        "Standard Unit": "%",
        "Clinical Category": "hematology"
    },

    {
        "Canonical Feature Name": "mean_platelet_volume",
        "Dataset Feature Name": "MPV",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "mpv,mean_platelet_volume",
        "Standard Unit": "fL",
        "Clinical Category": "hematology"
    },


    # --------------------------------------------------------
    # LIPID PROFILE
    # --------------------------------------------------------

    {
        "Canonical Feature Name": "triglycerides",
        "Dataset Feature Name": "Triglyceride",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "triglyceride,tg,trigs",
        "Standard Unit": "mg/dL",
        "Clinical Category": "lipid_profile"
    },

    {
        "Canonical Feature Name": "hdl_cholesterol",
        "Dataset Feature Name": "HDL Cholesterol",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "hdl,hdl_cholesterol,high_density_lipoprotein",
        "Standard Unit": "mg/dL",
        "Clinical Category": "lipid_profile"
    },

    {
        "Canonical Feature Name": "ldl_cholesterol",
        "Dataset Feature Name": "Direct LDL",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "ldl,direct_ldl,ldl_cholesterol",
        "Standard Unit": "mg/dL",
        "Clinical Category": "lipid_profile"
    },

    {
        "Canonical Feature Name": "vldl_cholesterol",
        "Dataset Feature Name": "VLDL",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "vldl,vldl_cholesterol",
        "Standard Unit": "mg/dL",
        "Clinical Category": "lipid_profile"
    },

    {
        "Canonical Feature Name": "cholesterol_hdl_ratio",
        "Dataset Feature Name": "CHOL/HDL Ratio",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "chol_hdl_ratio,total_cholesterol_hdl_ratio",
        "Standard Unit": "ratio",
        "Clinical Category": "lipid_profile"
    },

    {
        "Canonical Feature Name": "ldl_hdl_ratio",
        "Dataset Feature Name": "LDL/HDL Ratio",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "ldl_hdl_ratio",
        "Standard Unit": "ratio",
        "Clinical Category": "lipid_profile"
    },


    # --------------------------------------------------------
    # PROTEINS / LIVER
    # --------------------------------------------------------

    {
        "Canonical Feature Name": "total_protein",
        "Dataset Feature Name": "Total Protein",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "total_protein,serum_total_protein",
        "Standard Unit": "g/dL",
        "Clinical Category": "protein_profile"
    },

    {
        "Canonical Feature Name": "albumin",
        "Dataset Feature Name": "Albumin",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "serum_albumin,albumin",
        "Standard Unit": "g/dL",
        "Clinical Category": "protein_profile"
    },

    {
        "Canonical Feature Name": "globulin",
        "Dataset Feature Name": "Globulin",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "serum_globulin,globulin",
        "Standard Unit": "g/dL",
        "Clinical Category": "protein_profile"
    },

    {
        "Canonical Feature Name": "albumin_globulin_ratio",
        "Dataset Feature Name": "A/G Ratio",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "ag_ratio,albumin_globulin_ratio,a_g_ratio",
        "Standard Unit": "ratio",
        "Clinical Category": "protein_profile"
    },


    # --------------------------------------------------------
    # IRON PROFILE
    # --------------------------------------------------------

    {
        "Canonical Feature Name": "serum_iron",
        "Dataset Feature Name": "Iron micro",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "iron,serum_iron",
        "Standard Unit": "ug/dL",
        "Clinical Category": "iron_profile"
    },

    {
        "Canonical Feature Name": "total_iron_binding_capacity",
        "Dataset Feature Name": "Total Iron Binding Capacity (TIBC)",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "tibc,total_iron_binding_capacity",
        "Standard Unit": "ug/dL",
        "Clinical Category": "iron_profile"
    },

    {
        "Canonical Feature Name": "transferrin_saturation",
        "Dataset Feature Name": "Transferrin Saturation",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "transferrin_saturation,iron_saturation",
        "Standard Unit": "%",
        "Clinical Category": "iron_profile"
    },


    # --------------------------------------------------------
    # OTHER CLINICAL TESTS
    # --------------------------------------------------------

    {
        "Canonical Feature Name": "homocysteine",
        "Dataset Feature Name": "Homocysteine, Serum",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "homocysteine,serum_homocysteine",
        "Standard Unit": "umol/L",
        "Clinical Category": "metabolic"
    },

    {
        "Canonical Feature Name": "vitamin_d",
        "Dataset Feature Name": "25(OH) Vitamin D",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "vitamin_d,25oh_vitamin_d,25_hydroxy_vitamin_d",
        "Standard Unit": "ng/mL",
        "Clinical Category": "vitamin_profile"
    },

    {
        "Canonical Feature Name": "vitamin_b12",
        "Dataset Feature Name": "Vitamin B12",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "vitamin_b12,b12,cobalamin",
        "Standard Unit": "pg/mL",
        "Clinical Category": "vitamin_profile"
    },

    {
        "Canonical Feature Name": "immunoglobulin_e",
        "Dataset Feature Name": "IgE",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "ige,immunoglobulin_e,total_ige",
        "Standard Unit": "IU/mL",
        "Clinical Category": "immunology"
    },


    # --------------------------------------------------------
    # HEMOGLOBIN FRACTIONS
    # --------------------------------------------------------

    {
        "Canonical Feature Name": "hemoglobin_a",
        "Dataset Feature Name": "Hb A L %",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "hba,hb_a,hemoglobin_a",
        "Standard Unit": "%",
        "Clinical Category": "hemoglobin_fraction"
    },

    {
        "Canonical Feature Name": "hemoglobin_a2",
        "Dataset Feature Name": "Hb A2 %",
        "Disease Model": "general_lab",
        "Domain": "clinical_laboratory",
        "Synonyms": "hba2,hb_a2,hemoglobin_a2",
        "Standard Unit": "%",
        "Clinical Category": "hemoglobin_fraction"
    }
]


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("BIASGUARD AI - EXTENDING MASTER CLINICAL SCHEMA")
    print("=" * 60)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    df = pd.read_excel(INPUT_FILE)

    print(f"Existing records: {len(df)}")

    # Find highest existing numeric feature ID
    existing_ids = df["Feature ID"].astype(str).tolist()

    numbers = []

    for feature_id in existing_ids:

        if feature_id.startswith("CLN_"):

            try:
                numbers.append(
                    int(feature_id.replace("CLN_", ""))
                )
            except ValueError:
                pass

    next_number = max(numbers) + 1 if numbers else 1

    new_rows = []

    for feature in NEW_FEATURES:

        row = {
            "Feature ID": (
                f"CLN_{next_number:04d}"
            ),
            "Canonical Feature Name":
                feature["Canonical Feature Name"],

            "Dataset Feature Name":
                feature["Dataset Feature Name"],

            "Disease Model":
                feature["Disease Model"],

            "Domain":
                feature["Domain"],

            "Synonyms":
                feature["Synonyms"],

            "Standard Unit":
                feature["Standard Unit"],

            "Clinical Category":
                feature["Clinical Category"],

            "Status":
                "MATCHED",

            "Confidence Score":
                1.0
        }

        new_rows.append(row)

        print(
            f"Added {row['Feature ID']} → "
            f"{row['Canonical Feature Name']}"
        )

        next_number += 1

    new_df = pd.DataFrame(
        new_rows
    )

    final_df = pd.concat(
        [df, new_df],
        ignore_index=True
    )

    final_df.to_excel(
        OUTPUT_FILE,
        index=False,
        engine="openpyxl"
    )

    print()
    print("=" * 60)
    print("MASTER SCHEMA EXTENDED SUCCESSFULLY")
    print("=" * 60)
    print(f"Old records: {len(df)}")
    print(f"New features: {len(new_rows)}")
    print(f"Total records: {len(final_df)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()