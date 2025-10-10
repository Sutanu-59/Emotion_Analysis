# scripts/predict_with_probs_miniLM.py
import os
import joblib
import json
import numpy as np

# ===== Paths =====
MODEL_DIR = "models/minilm_emotion"
EMBEDDER_PATH = os.path.join(MODEL_DIR, "embedder.pkl")
LR_PATH = os.path.join(MODEL_DIR, "logistic_regression.pkl")
LABEL2ID_PATH = os.path.join(MODEL_DIR, "label2id.json")

# ===== Load models =====
print("⏳ Loading MiniLM embedder and Logistic Regression model...")
embedder = joblib.load(EMBEDDER_PATH)
lr_calibrated = joblib.load(LR_PATH)

with open(LABEL2ID_PATH, "r") as f:
    label2id = json.load(f)

id2label = {v: k for k, v in label2id.items()}
CLASSES = sorted(label2id.keys(), key=lambda x: label2id[x])

# ===== Prediction function =====
def predict_with_probs(text: str):
    """
    Returns:
        pred_label: str
        probs_dict: {class_name: probability_float_0_to_1}
        classes_list: list of class names
    """
    emb = embedder.encode([text])
    proba = lr_calibrated.predict_proba(emb)[0]
    pred_idx = int(np.argmax(proba))
    pred_label = id2label[pred_idx]

    probs_dict = {id2label[i]: float(p) for i, p in enumerate(proba)}

    return pred_label, probs_dict, CLASSES
