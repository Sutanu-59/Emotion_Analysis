# app.py
import streamlit as st
import joblib
import os
import json
import pandas as pd
import random

from questions import questions
from scripts.predict_lr import predict_with_probs

# ===== Paths =====
RESULTS_CSV = "data/session_results.csv"
os.makedirs("data", exist_ok=True)

# ===== Load Metrics =====
METRICS_PATH = "models/metrics.json"
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
    st.session_state.probabilities = []  # store probability dicts
    # Shuffle and select 10 random questions from the list
    st.session_state.questions_subset = random.sample(questions, 10)

# ===== Ask Random Questions =====
if st.session_state.q_index < len(st.session_state.questions_subset):
    question = st.session_state.questions_subset[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}: {question}")
    answer = st.text_area("Your response:", key=f"ans_{st.session_state.q_index}")

    if st.button("Next Question"):
        if answer.strip():
            pred, probs, _ = predict_with_probs(answer)  # <-- use new function
            st.session_state.responses.append(answer)
            st.session_state.predictions.append(pred)
            st.session_state.probabilities.append(probs)
            st.session_state.q_index += 1
            st.rerun()
        else:
            st.warning("Please provide an answer before continuing.")
else:
    st.success("✅ Survey completed!")

    # ===== Aggregate Results =====
    # Average probabilities across all responses (per session)
    prob_df = pd.DataFrame(st.session_state.probabilities)
    mean_probs = prob_df.mean().to_dict()
    mean_probs = {cls: round(mean_probs.get(cls, 0) * 100, 2) for cls in classes}

    session_result = {"PatientID": patient_id}
    session_result.update(mean_probs)

    # ===== Save to CSV =====
    if os.path.exists(RESULTS_CSV):
        results_df = pd.read_csv(RESULTS_CSV)
    else:
        results_df = pd.DataFrame(columns=["PatientID"] + classes)

    results_df = pd.concat([results_df, pd.DataFrame([session_result])], ignore_index=True)
    results_df.to_csv(RESULTS_CSV, index=False)

    # ===== Show Results =====
    st.subheader("📊 Your Session Summary")
    st.write(session_result)

    st.bar_chart(pd.DataFrame([mean_probs]).T.rename(columns={0: "Probability %"}))

    st.info("Session saved successfully! This data can now be analyzed in Power BI.")