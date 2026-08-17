import os
from dotenv import load_dotenv

load_dotenv()

ENDO_DIR = os.getenv("ENDO_DIR", r"C:\Users\hp\Downloads\Endocrinology")

DISEASE_CONFIG = {

    "thyroid": {
        "model_dir":     os.path.join(ENDO_DIR, "E00_E07_Thyroid", "saved_model"),
        "model_file":    "model.joblib",
        "scaler_file":   None,
        "encoder_file":  None,
        "data_file":     os.path.join(ENDO_DIR, "E00_E07_Thyroid", "data", "ann-train.data"),
        "target_col":    "class",
        "sensitive_col": "sex",
        "feature_cols":  [
            "age", "sex", "on_thyroxine", "query_on_thyroxine",
            "on_antithyroid_medication", "sick", "pregnant", "thyroid_surgery",
            "I131_treatment", "query_hypothyroid", "query_hyperthyroid",
            "lithium", "goitre", "tumor", "hypopituitary", "psych",
            "TSH", "T3", "TT4", "T4U", "FTI"
        ],
    },

    "diabetes": {
        "model_dir":     os.path.join(ENDO_DIR, "E08_E13_Diabetes", "saved_model"),
        "model_file":    "model.joblib",
        "scaler_file":   "scaler.joblib",
        "encoder_file":  None,
        "data_file":     os.path.join(ENDO_DIR, "E08_E13_Diabetes", "data", "diabetes.csv"),
        "target_col":    "Outcome",
        "sensitive_col": "age_group",
        "feature_cols":  [
            "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
        ],
    },

    # Only GlucoseCGM is numeric non-target — model expects 2 features
    # HR is target, ts/PtID/Database are non-numeric
    # Use GlucoseCGM as feature; sensitive fallback to GlucoseCGM bins
    "glucose": {
    "model_dir":     os.path.join(ENDO_DIR, "E15_E16_Glucose_Disorders", "saved_model"),
    "model_file":    "model.joblib",
    "scaler_file":   "scaler.joblib",
    "encoder_file":  None,
    "data_file":     os.path.join(ENDO_DIR, "E15_E16_Glucose_Disorders", "data", "glucose.csv"),
    "target_col":    "HR",
    "sensitive_col": "GlucoseCGM",
    "feature_cols":  ["GlucoseCGM", "HR"],
    "derive_target": True,   # HR will be binarized in bias_service
},

    # 42 features exactly matching model (stripped column names)
    "pcos": {
        "model_dir":     os.path.join(ENDO_DIR, "E20_E35_Endocrine_Disorders", "E28_PCOS", "saved_model"),
        "model_file":    "model.joblib",
        "scaler_file":   "scaler.joblib",
        "encoder_file":  None,
        "data_file":     os.path.join(ENDO_DIR, "E20_E35_Endocrine_Disorders", "E28_PCOS", "data", "pcos.csv"),
        "target_col":    "PCOS (Y/N)",
        "sensitive_col": "age_group",
        "feature_cols":  [
            "Patient File No.", "Age (yrs)", "Weight (Kg)", "Height(Cm)", "BMI",
            "Blood Group", "Pulse rate(bpm)", "RR (breaths/min)", "Hb(g/dl)",
            "Cycle(R/I)", "Cycle length(days)", "Marraige Status (Yrs)", "Pregnant(Y/N)",
            "No. of aborptions", "I   beta-HCG(mIU/mL)", "II    beta-HCG(mIU/mL)",
            "FSH(mIU/mL)", "LH(mIU/mL)", "FSH/LH", "Hip(inch)", "Waist(inch)",
            "Waist:Hip Ratio", "TSH (mIU/L)", "AMH(ng/mL)", "PRL(ng/mL)",
            "Vit D3 (ng/mL)", "PRG(ng/mL)", "RBS(mg/dl)", "Weight gain(Y/N)",
            "hair growth(Y/N)", "Skin darkening (Y/N)", "Hair loss(Y/N)",
            "Pimples(Y/N)", "Fast food (Y/N)", "Reg.Exercise(Y/N)",
            "BP _Systolic (mmHg)", "BP _Diastolic (mmHg)", "Follicle No. (L)",
            "Follicle No. (R)", "Avg. F size (L) (mm)", "Avg. F size (R) (mm)",
            "Endometrium (mm)"
        ],
    },

    "malnutrition": {
        "model_dir":     os.path.join(ENDO_DIR, "E40_E46_Malnutrition", "saved_model"),
        "model_file":    "model.joblib",
        "scaler_file":   "scaler.joblib",
        "encoder_file":  None,
        "data_file":     os.path.join(ENDO_DIR, "E40_E46_Malnutrition", "data", "malnutrition.csv"),
        "target_col":    "nutrition_status",
        "sensitive_col": "age_months",
        "feature_cols":  ["age_months", "weight_kg", "height_cm", "muac_cm", "bmi"],
    },

    "vitamin_d": {
        "model_dir":     os.path.join(ENDO_DIR, "E50_E64_Nutritional_Deficiency", "E55_Vitamin_D_Deficiency", "saved_model"),
        "model_file":    "model.joblib",
        "scaler_file":   "scaler.joblib",
        "encoder_file":  "label_encoder.joblib",
        "data_file":     os.path.join(ENDO_DIR, "E50_E64_Nutritional_Deficiency", "E55_Vitamin_D_Deficiency", "data", "vitamin_d.csv"),
        "target_col":    "Deficiency_Status",
        "sensitive_col": "age_group",
        "feature_cols":  [
            "Age", "BMI", "Sun_Exposure_Hours_Per_Week",
            "Physical_Activity_Level", "Vitamin_D_Intake_mcg_Per_Day",
            "Latitude", "Risk_Score"
        ],
    },

    # Obesity: string cols encoded via LabelEncoder before scaling
    "obesity": {
        "model_dir":     os.path.join(ENDO_DIR, "E65_E68_Obesity", "E66_Obesity", "saved_model"),
        "model_file":    "obesity_model.joblib",
        "scaler_file":   "scaler.joblib",
        "encoder_file":  "model.joblib",       # contains LabelEncoders per column
        "data_file":     os.path.join(ENDO_DIR, "E65_E68_Obesity", "E66_Obesity", "data", "obesity.csv"),
        "target_col":    "NObeyesdad",
        "sensitive_col": "age_group",          # Age col exists → binned
        "encode_cols":   ["Gender", "family_history_with_overweight", "FAVC",
                          "CAEC", "SMOKE", "SCC", "CALC", "MTRANS"],
        "feature_cols":  [
            "Gender", "Age", "Height", "Weight", "family_history_with_overweight",
            "FAVC", "FCVC", "NCP", "CAEC", "SMOKE", "CH2O", "SCC",
            "FAF", "TUE", "CALC", "MTRANS"
        ],
    },

    "metabolic": {
        "model_dir":     os.path.join(ENDO_DIR, "E70_E88_Metabolic_Disorders", "E78_Dyslipidemia", "saved_model"),
        "model_file":    "model.joblib",
        "scaler_file":   "scaler.joblib",
        "encoder_file":  None,
        "data_file":     os.path.join(ENDO_DIR, "E70_E88_Metabolic_Disorders", "E78_Dyslipidemia", "data", "heart.csv"),
        "target_col":    "target",
        "sensitive_col": "gender",
        "feature_cols":  [
            "age", "gender", "chestpain", "restingBP", "serumcholestrol",
            "fastingbloodsugar", "restingrelectro", "maxheartrate",
            "exerciseangia", "oldpeak", "slope", "noofmajorvessels"
        ],
    },
}

SUPPORTED_DISEASES = list(DISEASE_CONFIG.keys())