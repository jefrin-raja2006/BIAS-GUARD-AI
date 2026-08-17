import joblib
import os
import pandas as pd
import numpy as np

from disease_config import DISEASE_CONFIG, get_domain_diseases


def _load_model_artifacts(cfg: dict):
    """Same loading logic as bias_service._load_artifacts, kept local here
    so predict_service has no import-order dependency on bias_service."""
    model_path = os.path.join(cfg["model_dir"], cfg["model_file"])
    model = joblib.load(model_path)

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

    label_encoders = None
    if cfg.get("encode_cols") and cfg.get("encoder_file"):
        enc_path = os.path.join(cfg["model_dir"], cfg["encoder_file"])
        if os.path.exists(enc_path):
            label_encoders = joblib.load(enc_path)

    return model, scaler, label_encoders


def _build_feature_row(cfg: dict, patient_data: dict) -> pd.DataFrame:
    """Builds a single-row DataFrame in the exact column order the model expects,
    using only what's present in patient_data. Raises if fields are missing."""
    feature_cols = cfg["feature_cols"]
    missing = [c for c in feature_cols if c not in patient_data]
    if missing:
        raise ValueError(f"Missing fields: {missing}")

    row = {c: patient_data[c] for c in feature_cols}
    df = pd.DataFrame([row], columns=feature_cols)
    return df


def _predict_single_disease(disease: str, patient_data: dict) -> dict:
    cfg = DISEASE_CONFIG[disease]

    X = _build_feature_row(cfg, patient_data)

    model, scaler, label_encoders = _load_model_artifacts(cfg)

    if label_encoders and cfg.get("encode_cols"):
        for col in cfg["encode_cols"]:
            if col in X.columns and col in label_encoders:
                le = label_encoders[col]
                X[col] = le.transform(X[col].astype(str))

    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    if scaler is not None:
        try:
            X_scaled = scaler.transform(X)
        except Exception:
            X_scaled = X.values
    else:
        X_scaled = X.values

    pred_raw = model.predict(X_scaled)
    pred = int(np.array(pred_raw).flatten()[0])

    confidence = None
    if hasattr(model, "predict_proba"):
        try:
            proba = model.predict_proba(X_scaled)
            confidence = round(float(np.max(proba[0])), 4)
        except Exception:
            confidence = None

    return {
        "disease": disease,
        "prediction": pred,
        "confidence": confidence,
        "risk_flag": bool(pred == 1) if confidence is None else bool(pred == 1),
    }


def predict_domain(domain: str, patient_data: dict) -> dict:
    """Runs every disease model in the domain against this one patient's data.
    Diseases whose required fields aren't present in patient_data are skipped
    and reported separately, rather than silently ignored."""
    diseases = get_domain_diseases(domain)
    if not diseases:
        raise ValueError(f"No diseases registered for domain '{domain}'")

    results = []
    skipped = []

    for disease in diseases:
        cfg = DISEASE_CONFIG[disease]
        missing = [c for c in cfg["feature_cols"] if c not in patient_data]
        if missing:
            skipped.append({"disease": disease, "missing_fields": missing})
            continue
        try:
            result = _predict_single_disease(disease, patient_data)
            results.append(result)
        except Exception as e:
            skipped.append({"disease": disease, "error": str(e)})

    results.sort(key=lambda r: (r["confidence"] or 0), reverse=True)

    return {
        "domain": domain,
        "results": results,
        "skipped": skipped,
    }