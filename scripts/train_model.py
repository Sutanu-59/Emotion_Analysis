import os
import json
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, classification_report
from sentence_transformers import SentenceTransformer
from preprocessing import clean_text

# ===== Paths =====
DATA_PATH = "data/final_data_reduced_check.csv"
MODEL_DIR = "models/minilm_emotion"
os.makedirs(MODEL_DIR, exist_ok=True)

EMBEDDER_PATH = os.path.join(MODEL_DIR, "embedder.pkl")
LR_PATH = os.path.join(MODEL_DIR, "logistic_regression.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")
LABEL2ID_PATH = os.path.join(MODEL_DIR, "label2id.json")

# Cache paths for embeddings
TRAIN_EMB_PATH = "data/embeddings_train.npy"
TEST_EMB_PATH = "data/embeddings_test.npy"

# ===== Load dataset =====
print("📂 Loading dataset...")
df = pd.read_csv(DATA_PATH, encoding="latin1")

# Clean text
df["clean_text"] = df["Text"].apply(clean_text)
texts = df["clean_text"]
labels = df["Label"]

# ===== Create label2id mapping =====
unique_labels = sorted(labels.unique())
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}
labels_id = labels.map(label2id)

# ===== Train-test split =====
print("🧪 Splitting dataset...")
X_train_text, X_test_text, y_train, y_test = train_test_split(
    texts, labels_id, test_size=0.2, random_state=42, stratify=labels_id
)

# ===== Embedding =====
print("🔹 Loading MiniLM embedder...")
embedder = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

if os.path.exists(TRAIN_EMB_PATH) and os.path.exists(TEST_EMB_PATH):
    print("⚡ Using cached embeddings...")
    X_train = np.load(TRAIN_EMB_PATH)
    X_test = np.load(TEST_EMB_PATH)
else:
    print("⏳ Computing embeddings (once only)...")
    X_train = embedder.encode(X_train_text.tolist(), batch_size=64, show_progress_bar=True)
    X_test = embedder.encode(X_test_text.tolist(), batch_size=64, show_progress_bar=True)
    np.save(TRAIN_EMB_PATH, X_train)
    np.save(TEST_EMB_PATH, X_test)

# ===== Train Logistic Regression =====
print("🧠 Training Logistic Regression model...")
lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
lr_calibrated = CalibratedClassifierCV(lr, method="isotonic", cv=3)
lr_calibrated.fit(X_train, y_train)

# ===== Evaluation =====
print("📈 Evaluating model...")
y_pred = lr_calibrated.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(
    y_test, y_pred, labels=list(range(len(unique_labels))), target_names=unique_labels, digits=4
)

print(f"✅ Training Complete | Accuracy: {acc*100:.2f}%")
print("📊 Classification Report:")
print(report)

# ===== Save models =====
joblib.dump(embedder, EMBEDDER_PATH)
joblib.dump(lr_calibrated, LR_PATH)

# ===== Save metrics =====
with open(METRICS_PATH, "w") as f:
    json.dump({"accuracy": acc, "report": report, "classes": unique_labels}, f, indent=4)

# ===== Save label2id mapping =====
with open(LABEL2ID_PATH, "w") as f:
    json.dump(label2id, f, indent=4)

print(f"✅ Models and metrics saved in {MODEL_DIR}")
