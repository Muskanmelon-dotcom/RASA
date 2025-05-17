import streamlit as st
import sqlite3
import datetime

# --- Streamlit Page Config ---
st.set_page_config(page_title="Voice Health Tracker", page_icon="🎙️", layout="centered")

# --- Optional Styles ---
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass  # Continue without styles if not present

# --- Database Setup ---
conn = sqlite3.connect('health_logs.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS health_metrics (
        date TEXT,
        user_name TEXT,
        user_age TEXT,
        reason TEXT,
        metric_name TEXT,
        metric_value TEXT,
        raw_input_text TEXT
    )
''')
conn.commit()

# --- Initialize Session State ---
if "step" not in st.session_state:
    st.session_state.step = 1

# --- Step 1: Collect Name ---
if st.session_state.step == 1:
    st.title("Step 1: Your Name")
    name = st.text_input("What is your name?")
    if st.button("Next"):
        if name.strip() == "":
            st.error("Please enter your name to continue.")
        else:
            st.session_state.name = name
            st.session_state.step = 2

# --- Step 2: Collect Age ---
elif st.session_state.step == 2:
    st.title("Step 2: Your Age")
    age = st.text_input("How old are you?")
    if st.button("Next"):
        if age.strip() == "":
            st.error("Please enter your age to continue.")
        else:
            st.session_state.age = age
            st.session_state.step = 3

# --- Step 3: Reason for Visiting ---
elif st.session_state.step == 3:
    st.title("Step 3: What Brings You Here?")
    reason = st.text_input("e.g., stress, anxiety, period tracking")
    if st.button("Next"):
        st.session_state.reason = reason
        st.session_state.step = 4

# --- Step 4: Health Description + Audio Recorder ---
elif st.session_state.step == 4:
    st.title("Step 4: Describe Your Health Today")
    user_input = st.text_area("Speak or type your update")

    # --- Optional Voice Recorder ---
    st.subheader("Record Your Voice")
    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        # You could save 'audio_bytes' to storage or process it further here.

    if st.button("Submit"):
        if user_input.strip() == "":
            st.error("Please describe your health to continue.")
        else:
            today_date = datetime.date.today().isoformat()
            metrics = []

            # Simulated metric extraction
            text_lower = user_input.lower()
            if "period" in text_lower:
                metrics.append(("period_start", "yes"))
            if "spotting" in text_lower:
                metrics.append(("spotting", "yes"))
            if "headache" in text_lower:
                metrics.append(("symptoms", "headache"))
            if "cramps" in text_lower:
                metrics.append(("symptoms", "cramps"))
            if "low" in text_lower or "sad" in text_lower:
                metrics.append(("mood", "low"))

            for metric_name, metric_value in metrics:
                c.execute('''
                    INSERT INTO health_metrics (date, user_name, user_age, reason, metric_name, metric_value, raw_input_text)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (today_date, st.session_state.name, st.session_state.age, st.session_state.reason,
                      metric_name, metric_value, user_input))
                conn.commit()

            st.success(f"Logged: {', '.join([m[0] for m in metrics])} for today.")
            st.balloons()
            st.session_state.step = 1  # Restart for next user
