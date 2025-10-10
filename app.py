# app.py
import streamlit as st
import os
import json
import pandas as pd
import random
import requests, base64
import io

from questions import questions
from scripts.predict_lr import predict_with_probs  # MiniLM version

# ===== Paths =====
RESULTS_CSV = "data/session_results.csv"
os.makedirs("data", exist_ok=True)

# ===== GitHub Config =====
GITHUB_REPO = "Sutanu-59/Emotion_Analysis"
FILE_PATH = "data/session_results.csv"  # path inside repo
BRANCH = "main"
TOKEN = st.secrets["GITHUB_TOKEN"]  # add to .streamlit/secrets.toml

# ===== Functions =====
def update_csv_on_github(df_new):
    """Upload session_results.csv to GitHub safely, avoid duplicates"""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {TOKEN}"}

    # Check if file exists
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        sha = data["sha"]
        csv_content = base64.b64decode(data["content"]).decode()
        df_old = pd.read_csv(io.StringIO(csv_content))
        df_final = pd.concat([df_old, df_new], ignore_index=True)
        # Remove duplicate PatientID rows, keep the last submission
        df_final = df_final.drop_duplicates(subset=["PatientID"], keep="last")
    else:
        sha = None
        df_final = df_new

    # Convert to CSV
    csv_data = df_final.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()

    # Commit
    commit_data = {
        "message": "Update session results from Streamlit app",
        "content": encoded,
        "branch": BRANCH,
    }
    if sha:
        commit_data["sha"] = sha

    upload = requests.put(url, headers=headers, json=commit_data)

    if upload.status_code in [200, 201]:
        st.success("✅ Data successfully saved to GitHub!")
    else:
        st.error(f"❌ GitHub update failed: {upload.json()}")


# ===== Load Metrics =====
METRICS_PATH = "models/minilm_emotion/metrics.json"
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

# ===== Session State Initialization =====
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
    st.session_state.responses = []
    st.session_state.predictions = []
    st.session_state.probabilities = []
    st.session_state.questions_subset = random.sample(questions, 10)
    st.session_state.uploaded_to_github = False  # ✅ prevent repeated upload

# ===== Ask Random Questions =====
if st.session_state.q_index < len(st.session_state.questions_subset):
    question = st.session_state.questions_subset[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {question}")
    answer = st.text_area("Your response:", key=f"ans_{st.session_state.q_index}")

    if st.button("Next Question"):
        if answer.strip():
            pred, probs, _ = predict_with_probs(answer)
            st.session_state.responses.append(answer)
            st.session_state.predictions.append(pred)
            st.session_state.probabilities.append(probs)
            st.session_state.q_index += 1
            st.experimental_rerun()  # now safe since upload flag prevents duplicates
        else:
            st.warning("Please provide an answer before continuing.")

else:
    st.success("✅ Survey completed!")

    # ===== Aggregate Results =====
    prob_df = pd.DataFrame(st.session_state.probabilities)
    mean_probs = prob_df.mean().to_dict()
    mean_probs = {cls: round(mean_probs.get(cls, 0) * 100, 2) for cls in classes}

    session_result = {"PatientID": patient_id}
    session_result.update(mean_probs)
    new_df = pd.DataFrame([session_result])

    # ===== Save to GitHub once =====
    if not st.session_state.uploaded_to_github:
        update_csv_on_github(new_df)
        st.session_state.uploaded_to_github = True

    # ===== Show Results =====
    st.subheader("📊 Your Session Summary")
    st.write(session_result)
    st.bar_chart(pd.DataFrame([mean_probs]).T.rename(columns={0: "Probability %"}))
    st.info("Session saved successfully! You can now view it in GitHub / Power BI.")
