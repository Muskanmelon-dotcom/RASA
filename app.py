import streamlit as st
import sqlite3
import datetime
import os

# --- Streamlit Page Config ---
st.set_page_config(page_title="Voice Health Tracker", page_icon="🎙️", layout="centered")

# --- Optional Styles ---
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- Ensure Audio Save Directory ---
os.makedirs("recordings", exist_ok=True)

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

# --- Step 1: Welcome ---
if st.session_state.step == 1:
    st.title("Welcome to Ash")
    st.write("You're in the right place.")
    if st.button("Continue"):
        st.session_state.step = 2

# --- Step 2: Age ---
elif st.session_state.step == 2:
    st.title("How old are you?")
    age = st.radio("Select an age range:", ["18 – 24", "25 – 34", "35 – 44", "45 – 54", "55 – 64", "65+", "Prefer not to say"])
    if st.button("Next"):
        st.session_state.age = age
        st.session_state.step = 3

# --- Step 3: Gender ---
elif st.session_state.step == 3:
    st.title("How do you identify?")
    gender = st.radio("Select one:", ["Female", "Male", "Non-binary", "Prefer not to say", "Other"])
    if st.button("Next"):
        st.session_state.gender = gender
        st.session_state.step = 4

# --- Step 4: Ethnicity ---
elif st.session_state.step == 4:
    st.title("What best describes your race/ethnicity?")
    ethnicity = st.radio("Select one:", [
        "White / Caucasian", "Black / African American", "Hispanic / Latino",
        "Asian / South Asian / East Asian", "Native Hawaiian / Pacific Islander",
        "American Indian / Alaska Native", "Prefer not to say", "Other"
    ])
    if st.button("Next"):
        st.session_state.ethnicity = ethnicity
        st.session_state.step = 5

# --- Step 5: Reason for Support ---
elif st.session_state.step == 5:
    st.title("What are you most looking for support with?")
    reason = st.radio("Choose your primary concern:", ["Depression", "Anxiety", "Relationships", "Something else"])
    if st.button("Next"):
        st.session_state.reason = reason
        st.session_state.step = 6

# --- Step 6: Commitment Page ---
elif st.session_state.step == 6:
    st.title("Our Commitment to You")
    st.write("Your mental health is personal and private.")
    if st.button("Continue"):
        st.session_state.step = 7

# --- Step 7: Health Description + Audio Recorder ---
elif st.session_state.step == 7:
    st.title("Describe Your Health Today")
    user_input = st.text_area("Speak or type your update")

    st.subheader("Record Your Voice")
    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        # Save audio to file
        filename = f"recordings/{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(filename, "wb") as f:
            f.write(audio_bytes.getvalue())
        st.success(f"Saved your recording to {filename}")

    if st.button("Submit"):
        if user_input.strip() == "":
            st.error("Please describe your health to continue.")
        else:
            today_date = datetime.date.today().isoformat()
            metrics = []
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
                ''', (today_date, st.session_state.get("name", ""), st.session_state.age, st.session_state.reason,
                      metric_name, metric_value, user_input))
                conn.commit()

            st.success(f"Logged: {', '.join([m[0] for m in metrics])} for today.")
            st.session_state.step = 1  # Restart for next user
