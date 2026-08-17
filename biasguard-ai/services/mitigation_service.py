import os
import joblib
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE


from disease_config import DISEASE_CONFIG
from services.bias_service import _load_data, _resolve_columns, _make_age_groups


def _prepare_X(df: pd.DataFrame, feature_cols: list, cfg: dict):
    """
    Prepare feature matrix — encode string cols, coerce to numeric.
    Uses LabelEncoders from cfg if available (obesity).
    """
    X = df[feature_cols].copy()

    # Apply LabelEncoders for obesity
    label_encoders = None
    if cfg.get("encode_cols") and cfg.get("encoder_file"):
        enc_path = os.path.join(cfg["model_dir"], cfg["encoder_file"])
        if os.path.exists(enc_path):
            label_encoders = joblib.load(enc_path)

    if label_encoders and cfg.get("encode_cols"):
        for col in cfg["encode_cols"]:
            if col in X.columns and col in label_encoders:
                le = label_encoders[col]
                X[col] = le.transform(X[col].astype(str))

    # Coerce all remaining object cols to numeric (fixes PCOS AMH, II beta-HCG etc.)
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)
    return X


def run_smote(disease: str) -> dict:
    """
    Apply SMOTE to balance the dataset for the given disease.
    Returns before/after class distribution and number of samples added.
    """
    if disease not in DISEASE_CONFIG:
        raise ValueError(f"Unknown disease '{disease}'. Supported: {list(DISEASE_CONFIG.keys())}")

    cfg = DISEASE_CONFIG[disease]
    df = _load_data(cfg)
    feature_cols, target_col, sensitive_col = _resolve_columns(df, cfg)

    missing = [c for c in feature_cols + [target_col] if c not in df.columns]
    if missing:
        raise ValueError(f"Columns missing in dataset: {missing}")

    X = _prepare_X(df, feature_cols, cfg)
    y = df[target_col].copy()

    # Flatten y
    y = pd.Series(np.array(y).flatten())

    before_dist = y.value_counts().to_dict()
    before_dist = {str(k): int(v) for k, v in before_dist.items()}

    # Determine SMOTE k_neighbors safely
    min_class_count = y.value_counts().min()
    k = min(5, min_class_count - 1)
    if k < 1:
        return {
            "disease": disease,
            "status": "skipped",
            "reason": f"Minority class has only {min_class_count} sample(s). Need at least 2 for SMOTE.",
            "before_distribution": before_dist,
        }

    smote = SMOTE(random_state=42, k_neighbors=k)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    after_dist = pd.Series(y_resampled).value_counts().to_dict()
    after_dist = {str(k): int(v) for k, v in after_dist.items()}

    added = sum(after_dist.values()) - sum(before_dist.values())

    return {
        "disease": disease,
        "status": "success",
        "sensitive_attribute": sensitive_col,
        "before_distribution": before_dist,
        "after_distribution": after_dist,
        "samples_added": added,
        "message": (
            f"SMOTE balanced the '{disease}' dataset. "
            f"Added {added} synthetic samples. "
            "Recommend retraining the model with this balanced data."
        ),
    }


def run_synthetic(disease: str, num_rows: int = 200) -> dict:
    if disease not in DISEASE_CONFIG:
        raise ValueError(f"Unknown disease '{disease}'. Supported: {list(DISEASE_CONFIG.keys())}")

    cfg = DISEASE_CONFIG[disease]
    df = _load_data(cfg)
    feature_cols, target_col, sensitive_col = _resolve_columns(df, cfg)

    cols_to_use = list(set(feature_cols + [target_col]))
    if sensitive_col in df.columns and sensitive_col not in cols_to_use:
        cols_to_use.append(sensitive_col)
    df_subset = df[cols_to_use].dropna().copy()

    # Cast columns
    for col in df_subset.columns:
        try:
            df_subset[col] = pd.to_numeric(df_subset[col], errors="raise").astype(float)
        except (ValueError, TypeError):
            df_subset[col] = df_subset[col].astype(str)

    # Always treat target as categorical
    df_subset[target_col] = df_subset[target_col].astype(str)

    # Always treat target and sensitive as categorical
    df_subset[target_col] = df_subset[target_col].astype(str)
    if sensitive_col in df_subset.columns:
        df_subset[sensitive_col] = df_subset[sensitive_col].astype(str)

    # Round float columns that should be integers (age, count-like cols)
    for col in df_subset.select_dtypes(include="float").columns:
        if df_subset[col].dropna().apply(lambda x: x == int(x)).all():
            df_subset[col] = df_subset[col].astype(int)
                
    synthetic_rows = {}
    for col in df_subset.columns:
        if pd.api.types.is_float_dtype(df_subset[col]):
            mean = df_subset[col].mean()
            std = df_subset[col].std()
            synthetic_rows[col] = np.random.normal(loc=mean, scale=std if std > 0 else 1, size=num_rows)
        else:
            # Sample from existing category distribution
            probs = df_subset[col].value_counts(normalize=True)
            synthetic_rows[col] = np.random.choice(probs.index.tolist(), size=num_rows, p=probs.values.tolist())

    synthetic_df = pd.DataFrame(synthetic_rows)

    if sensitive_col in synthetic_df.columns:
        group_counts = synthetic_df[sensitive_col].astype(str).value_counts().to_dict()
    else:
        group_counts = {}

    target_dist = synthetic_df[target_col].value_counts().to_dict()
    target_dist = {str(k): int(v) for k, v in target_dist.items()}

    return {
        "disease": disease,
        "status": "success",
        "sensitive_attribute": sensitive_col,
        "synthetic_rows_generated": num_rows,
        "synthetic_group_distribution": {str(k): int(v) for k, v in group_counts.items()},
        "synthetic_target_distribution": target_dist,
        "sample_preview": synthetic_df.head(5).to_dict(orient="records"),
        "message": (
            f"Generated {num_rows} synthetic '{disease}' patient records. "
            "Use these to augment underrepresented groups before retraining."
        ),
    }