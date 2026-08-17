import os
import joblib
import pandas as pd
import numpy as np
from fairlearn.metrics import demographic_parity_difference, equalized_odds_difference

from disease_config import DISEASE_CONFIG


def _load_artifacts(cfg: dict):
    """Load model and scaler. For obesity, also load LabelEncoders from encoder_file."""
    model_path = os.path.join(cfg["model_dir"], cfg["model_file"])
    model = joblib.load(model_path)

    # Unwrap dict-wrapped models
    if isinstance(model, dict):
        for key in ["model", "estimator", "classifier", "clf"]:
            if key in model and hasattr(model[key], "predict"):
                model = model[key]
                break
        else:
            for v in model.values():
                if hasattr(v, "predict"):
                    model = v
                    break

    scaler = None
    if cfg.get("scaler_file"):
        scaler_path = os.path.join(cfg["model_dir"], cfg["scaler_file"])
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)

    # Load label encoders (obesity uses encoder_file = model.joblib dict of LabelEncoders)
    label_encoders = None
    if cfg.get("encode_cols") and cfg.get("encoder_file"):
        enc_path = os.path.join(cfg["model_dir"], cfg["encoder_file"])
        if os.path.exists(enc_path):
            label_encoders = joblib.load(enc_path)

    return model, scaler, label_encoders


def _load_data(cfg: dict) -> pd.DataFrame:
    data_path = cfg["data_file"]
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at: {data_path}")
    if data_path.endswith(".data"):
        col_names = cfg["feature_cols"] + [cfg["target_col"]]
        return pd.read_csv(data_path, header=None, sep=r"\s+", names=col_names)
    df = pd.read_csv(data_path, sep=None, engine="python")
    df.columns = df.columns.str.strip()
    return df


def _resolve_columns(df: pd.DataFrame, cfg: dict):
    target_col = cfg["target_col"].strip()
    sensitive_col = cfg["sensitive_col"].strip()

    if cfg["feature_cols"] is not None:
        feature_cols = [c.strip() for c in cfg["feature_cols"]]
        return feature_cols, target_col, sensitive_col

    # Auto-detect: numeric cols only, exclude target and sensitive
    exclude = {target_col, sensitive_col}
    feature_cols = [c for c in df.columns if c not in exclude and pd.api.types.is_numeric_dtype(df[c])]
    return feature_cols, target_col, sensitive_col


def _make_age_groups(df: pd.DataFrame) -> pd.Series:
    age_col = next((c for c in df.columns if c.lower() in ["age", "age (yrs)"]), None)
    if age_col is None:
        raise ValueError("No 'age' column found for age_group binning.")
    return pd.cut(
        pd.to_numeric(df[age_col], errors="coerce"),
        bins=[0, 18, 35, 50, 65, 120],
        labels=["0-18", "19-35", "36-50", "51-65", "65+"]
    ).astype(str)


def _binarize_labels(y: pd.Series) -> pd.Series:
    unique = y.dropna().unique()
    if set(unique).issubset({0, 1}):
        return y.astype(int)
    if pd.api.types.is_numeric_dtype(y):
        return (y != 0).astype(int)
    most_frequent = y.value_counts().idxmax()
    return (y != most_frequent).astype(int)


def _bin_numeric_sensitive(s: pd.Series, n_bins: int = 5) -> pd.Series:
    if not isinstance(s, pd.Series):
        s = pd.Series(np.array(s).flatten())
    s = s.reset_index(drop=True)
    try:
        return pd.qcut(s, q=n_bins, duplicates="drop").astype(str)
    except Exception:
        return s.astype(str)

def check_bias(disease: str) -> dict:
    if disease not in DISEASE_CONFIG:
        raise ValueError(f"Unknown disease '{disease}'. Supported: {list(DISEASE_CONFIG.keys())}")

    cfg = DISEASE_CONFIG[disease]
    model, scaler, label_encoders = _load_artifacts(cfg)
    df = _load_data(cfg)

    feature_cols, target_col, sensitive_col = _resolve_columns(df, cfg)

    missing = [c for c in feature_cols + [target_col] if c not in df.columns]
    if missing:
        raise ValueError(f"Columns missing in dataset: {missing}")

    X = df[feature_cols].copy()
    y_true = df[target_col].copy()
# For glucose: derive binary target from HR median
    if cfg.get("derive_target"):
        median_val = y_true.median()
        y_true = (y_true > median_val).astype(int)
    # Apply LabelEncoders for obesity string columns
    if label_encoders and cfg.get("encode_cols"):
        for col in cfg["encode_cols"]:
            if col in X.columns and col in label_encoders:
                le = label_encoders[col]
                X[col] = le.transform(X[col].astype(str))

    # Coerce all X to numeric (fixes PCOS object cols like AMH, II beta-HCG)
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    # Handle sensitive attribute
    if sensitive_col == "age_group":
        sensitive = _make_age_groups(df)
    elif sensitive_col not in df.columns:
        raise ValueError(f"Sensitive column '{sensitive_col}' not found in dataset.")
    else:
        s = df[sensitive_col].squeeze()
        if pd.api.types.is_numeric_dtype(s):
            sensitive = _bin_numeric_sensitive(s)
        else:
            sensitive = s.astype(str)

    # Scale
    if scaler is not None:
        try:
            X_scaled = scaler.transform(X)
        except Exception:
            X_scaled = X.values
    else:
        X_scaled = X.values

    y_pred_raw = model.predict(X_scaled)
    y_pred = pd.Series(np.array(y_pred_raw).flatten())

    y_true = pd.Series(np.array(y_true).flatten())
    y_true_bin = _binarize_labels(y_true)
    y_pred_bin = _binarize_labels(y_pred)

    dpd = demographic_parity_difference(y_true_bin, y_pred_bin, sensitive_features=sensitive)
    eod = equalized_odds_difference(y_true_bin, y_pred_bin, sensitive_features=sensitive)

    bias_detected = bool(abs(dpd) > 0.1 or abs(eod) > 0.1)

    df_tmp = df.copy()
    df_tmp["_pred"] = y_pred_bin.values
    df_tmp["_sensitive"] = sensitive.values
    group_rates = (
        df_tmp.groupby("_sensitive")["_pred"]
        .mean()
        .round(4)
        .to_dict()
    )

    return {
        "disease": disease,
        "sensitive_attribute": sensitive_col,
        "bias_detected": bias_detected,
        "demographic_parity_difference": round(float(dpd), 4),
        "equalized_odds_difference": round(float(eod), 4),
        "group_prediction_rates": group_rates,
        "alert": (
            f"⚠️ Bias detected in '{disease}' predictions across {sensitive_col} groups. "
            "Doctor should review carefully."
            if bias_detected else
            f"✅ No significant bias detected in '{disease}' predictions."
        ),
    }