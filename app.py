
# Mamba AI Maintenance Hub - Streamlit App (MVP + Logs & Charts)
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import os

# Load or create log data
LOG_FILE = "mamba_logs.csv"
if os.path.exists(LOG_FILE):
    logs_df = pd.read_csv(LOG_FILE)
else:
    logs_df = pd.DataFrame(columns=["Date", "Shift", "Machine", "Operator ID", "Runtime (hrs)", "Downtime (mins)", "OEE (%)", "Issue", "Fix"])

# Title and login
st.title("🛠️ Mamba AI Maintenance Hub")
st.markdown("**AI-powered maintenance log and prediction system for IMA I20 CORAZZA machines.**")

# Simulate operator login
operator_id = st.text_input("Enter Operator ID (e.g., PNG1080)", max_chars=10)
if not operator_id:
    st.stop()

# Machine selector
press_ids = list(range(40, 90, 2))
selected_press = st.selectbox("Select Press Machine", press_ids)
selected_wrapper = selected_press + 1
machine_name = f"Press {selected_press} & Wrapper {selected_wrapper}"

# Shift info
shift = st.selectbox("Shift", [1, 2, 3])
date = st.date_input("Date", datetime.date.today())
runtime = st.slider("Runtime (hrs)", 0.0, 8.0, 7.5, 0.1)
downtime = st.slider("Downtime (mins)", 0, 120, 10)
oee = round(100 - (downtime / (runtime * 60 + downtime)) * 100, 2)

# Issue and Fix
issues = ["Cube crash on bridge", "Line 1/2 missing wrapping", "Exit belt cut", "None"]
issue = st.selectbox("Issue Encountered", issues)

fixes = {
    "Cube crash on bridge": ["Blow powder with airgun", "Realign bridge and remove cubes"],
    "Line 1/2 missing wrapping": ["Blow naked cube with airgun", "Check wrapping knife or replace paper reel"],
    "Exit belt cut": ["Replace exit belt"],
    "None": ["None"]
}
fix = st.selectbox("Fix Applied", fixes[issue])

# Submit log
if st.button("Submit Log"):
    new_log = pd.DataFrame([[date, shift, machine_name, operator_id, runtime, downtime, oee, issue, fix]],
                           columns=logs_df.columns)
    logs_df = pd.concat([logs_df, new_log], ignore_index=True)
    logs_df.to_csv(LOG_FILE, index=False)
    st.success(f"✅ Log submitted by {operator_id} for {machine_name} on {date} (Shift {shift})")
    st.info(f"Runtime: {runtime} hrs | Downtime: {downtime} mins | OEE: {oee}%")
    st.info(f"Issue: {issue} | Fix: {fix}")

# Prediction placeholder
if st.button("🔮 Predict Next Issue & Run Hours"):
    pred_issue = random.choice(issues[:-1])
    pred_runtime = round(random.uniform(6.0, 7.9), 2)
    st.subheader("🔧 AI Prediction")
    st.write(f"**Most Likely Next Issue**: {pred_issue}")
    st.write(f"**Expected Run Time Before Issue**: {pred_runtime} hrs")

# Logs Viewer
st.markdown("---")
st.subheader("📋 Log History Viewer")
if logs_df.empty:
    st.info("No logs submitted yet.")
else:
    filter_machine = st.selectbox("Filter by Machine", ["All"] + sorted(logs_df["Machine"].unique().tolist()))
    filtered_df = logs_df if filter_machine == "All" else logs_df[logs_df["Machine"] == filter_machine]
    st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True)

# Charts
if not logs_df.empty:
    st.subheader("📊 OEE & Downtime Trends")
    chart_data = logs_df.copy()
    chart_data["Date"] = pd.to_datetime(chart_data["Date"])
    st.line_chart(chart_data.groupby("Date")["OEE (%)"].mean(), use_container_width=True)
    st.bar_chart(chart_data.groupby("Issue")["Downtime (mins)"].sum(), use_container_width=True)
    st.subheader("🧮 Issue Frequency")
    st.dataframe(chart_data["Issue"].value_counts().reset_index().rename(columns={"index": "Issue", "Issue": "Count"}))

# Footer
st.markdown("---")
st.caption("Built by Mamba & ChatGPT for AI Challenge 2025")
