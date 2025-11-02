# app.py

import streamlit as st
import pandas as pd
import pickle

# -----------------------------
# Load trained model
# -----------------------------
with open("nsl_model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# App title
# -----------------------------
st.title("NSL-KDD Intrusion Detection App")
st.write("""
Predict whether a network connection is **Normal** or an **Attack** with confidence scores.
""")

# -----------------------------
# Initialize session state for demo values
# -----------------------------
for feature in ['duration', 'src_bytes', 'dst_bytes', 'count', 'srv_count']:
    if feature not in st.session_state:
        st.session_state[feature] = 0

# -----------------------------
# Sidebar for inputs and demo buttons
# -----------------------------
st.sidebar.header("Network Connection Features")

# Demo buttons
st.sidebar.header("Load Demo Example")
if st.sidebar.button("Normal Example"):
    st.session_state['duration'] = 0
    st.session_state['src_bytes'] = 491
    st.session_state['dst_bytes'] = 0
    st.session_state['count'] = 2
    st.session_state['srv_count'] = 2

if st.sidebar.button("Attack Example"):
    st.session_state['duration'] = 0
    st.session_state['src_bytes'] = 0
    st.session_state['dst_bytes'] = 0
    st.session_state['count'] = 100
    st.session_state['srv_count'] = 100

# Inputs bound to session state
duration = st.sidebar.number_input("duration", min_value=0, value=st.session_state['duration'], key='duration')
src_bytes = st.sidebar.number_input("src_bytes", min_value=0, value=st.session_state['src_bytes'], key='src_bytes')
dst_bytes = st.sidebar.number_input("dst_bytes", min_value=0, value=st.session_state['dst_bytes'], key='dst_bytes')
count = st.sidebar.number_input("count", min_value=0, value=st.session_state['count'], key='count')
srv_count = st.sidebar.number_input("srv_count", min_value=0, value=st.session_state['srv_count'], key='srv_count')

# -----------------------------
# Predict button with confidence
# -----------------------------
st.subheader("Prediction Result")
if st.button("Predict"):
    features = [[duration, src_bytes, dst_bytes, count, srv_count]]  # Add all 41 features in same order

    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]  # [prob_normal, prob_attack]

    # Colored prediction card
    if prediction == 0:
        st.markdown(
            f'<div style="background-color: #d4edda; padding: 10px; border-radius: 5px;"><b>✅ Normal connection</b></div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="background-color: #f8d7da; padding: 10px; border-radius: 5px;"><b>⚠️ Attack detected</b></div>', 
            unsafe_allow_html=True
        )

    # Confidence progress bars
    st.subheader("Prediction Confidence:")
    st.write(f"Normal: {proba[0]*100:.2f}%")
    st.progress(int(proba[0]*100))
    st.write(f"Attack: {proba[1]*100:.2f}%")
    st.progress(int(proba[1]*100))

# -----------------------------
# Optional: Show sample data
# -----------------------------
if st.checkbox("Show sample data"):
    df = pd.read_csv("KDDTest+.txt", header=None)  # or your test CSV
    st.dataframe(df.head(10))
