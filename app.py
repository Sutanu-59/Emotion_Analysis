# app.py
import streamlit as st
import joblib
import os
import json
import pandas as pd
import random
import requests
import base64
import io

from questions import questions
from scripts.predict_lr import predict_with_probs  # 🔹 MiniLM prediction

# ===== Paths =====
RESULTS_CSV = "data/session_results.csv"
os.makedirs("data", exist_ok=True)

# ===== GitHub Config =====
GITHUB_REPO = "Sutanu-59/Emotion_Analysis"   # 🔹 change this
FILE_PATH = "data/session_results.csv"       # path inside repo
BRANCH = "main"
TOKEN = st.secrets["GITHUB_TOKEN"]          # add to .streamlit/secrets.toml

# ===== Helper: GitHub Upload =====
def update_csv_on_github(df_new, patient_id_col="PatientID"):
    """
    Safely upload session_results.csv to GitHub:
    - Removes duplicates by PatientID
    - Handles SHA conflicts
    """
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}"}

    for attempt in range(3):
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            sha = data["sha"]
            csv_content = base64.b64decode(data["content"]).decode()
            df_old = pd.read_csv(io.StringIO(csv_content))

            # Remove existing entry for same PatientID
            df_old = df_old[df_old[patient_id_col] != df_new[patient_id_col].values[0]]
            df_final = pd.concat([df_old, df_new], ignore_index=True)
        else:
            sha = None
            df_final = df_new

        # Convert to CSV and encode
        csv_data = df_final.to_csv(index=False)
        encoded = base64.b64encode(csv_data.encode()).decode()

        commit_data = {
            "message": f"Update session results for {df_new[patient_id_col].values[0]}",
            "content": encoded,
            "branch": BRANCH,
        }
        if sha:
            commit_data["sha"] = sha

        upload = requests.put(url, headers=headers, json=commit_data)
        if upload.status_code in [200, 201]:
            st.success("✅ Data successfully saved to GitHub!")
            return
        else:
            sha = None  # Retry if SHA conflict

    st.error(f"❌ GitHub update failed: {upload.json()}")

# ===== Load Metrics =====
METRICS_PATH = "models/minilm_emotion/metrics.json"  # 🔹 updated path
with open(METRICS_PATH, "r") as f:
    metrics = json.load(f)

classes = metrics["classes"]

# ===== Streamlit Config =====
st.set_page_config(page_title="Depression Counselling Survey", layout="centered")
st.title("🧠 Interactive Emotion Counselling")

# ===== Patient Info =====
patient_id = st.text_input("Enter Patient ID:", "")
if not patient_id:
    st.warning("Please enter a Patient ID to start.")
    st.stop()

# ===== Session State =====
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.responses = []
    st.session_state.predictions = []
    st.session_state.probabilities = []
    st.session_state.questions_subset = random.sample(questions, 10)

# ===== Ask Random Questions =====
if st.session_state.q_index < len(st.session_state.questions_subset):
    question = st.session_state.questions_subset[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {question}")
    answer = st.text_area("Your response:", key=f"ans_{st.session_state.q_index}")

    if st.button("Next Question"):
        if answer.strip():
            pred, probs, _ = predict_with_probs(answer)  # MiniLM prediction
            st.session_state.responses.append(answer)
            st.session_state.predictions.append(pred)
            st.session_state.probabilities.append(probs)
            st.session_state.q_index += 1

        else:
            st.warning("Please provide an answer before continuing.")

else:
    st.success("✅ Survey completed!")

    # ===== Aggregate Results =====
    prob_df = pd.DataFrame(st.session_state.probabilities)
    mean_probs = prob_df.mean().to_dict()
    mean_probs = {cls: round(mean_probs.get(cls, 0) * 100, 2) for cls in classes}

    # Prepare session result
    session_result = {"PatientID": patient_id}
    session_result.update(mean_probs)
    new_df = pd.DataFrame([session_result])

    # ===== Upload to GitHub =====
    update_csv_on_github(new_df)

    # ===== Show Results =====
    st.subheader("📊 Your Session Summary")
    st.write(session_result)

    st.bar_chart(pd.DataFrame([mean_probs]).T.rename(columns={0: "Probability %"}))
    st.info("Session saved successfully! You can now view it in GitHub / Power BI.")

