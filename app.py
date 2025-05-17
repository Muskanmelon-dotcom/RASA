import streamlit as st
import os
import sqlite3
from datetime import datetime

# --- Streamlit Config ---
st.set_page_config(page_title="Period Health Voice Tracker", page_icon="🩸", layout="centered")

# --- Database Setup ---
conn = sqlite3.connect('user_profiles.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
        timestamp TEXT,
        name TEXT,
        age_range TEXT,
        gender TEXT,
        tracking_goals TEXT,
        last_period_date TEXT,
        cycle_length TEXT,
        period_duration TEXT,
        share_data TEXT
    )
''')
conn.commit()

# --- Session State Setup ---
if "step" not in st.session_state:
    st.session_state.step = 1

# --- Onboarding Screens ---
if st.session_state.step == 1:
    st.title("🩸 Track Your Cycle, Understand Your Body.")
    st.write("We help you easily log period dates, symptoms, and moods to reveal patterns and insights about your health.")
    if st.button("Get Started"):
        st.session_state.step = 2

elif st.session_state.step == 2:
    st.title("Tell us a little about yourself.")
    st.session_state.name = st.text_input("What's your name?")
    st.session_state.age_range = st.radio("How old are you?", ["18-24", "25-34", "35-44", "45-54", "55+", "Prefer not to say"])
    st.session_state.gender = st.radio("How do you identify?", ["Female", "Non-binary", "Prefer not to say", "Other"])
    if st.button("Next"):
        st.session_state.step = 3

elif st.session_state.step == 3:
    st.title("What are you hoping to track?")
    tracking_options = [
        "Predicting my period", "Understanding symptoms", "Tracking irregularities",
        "Trying to conceive", "General health awareness", "Something else"
    ]
    st.session_state.tracking_goals = st.multiselect("Select all that apply:", tracking_options)
    if st.button("Next"):
        st.session_state.step = 4

elif st.session_state.step == 4:
    st.title("When did your last period start?")
    st.session_state.last_period_date = st.date_input("Select the date or skip if you're unsure.")
    if st.button("Next"):
        st.session_state.step = 5

elif st.session_state.step == 5:
    st.title("What's your typical cycle length?")
    st.session_state.cycle_length = st.number_input("Average number of days (e.g., 28)", min_value=0, step=1)
    if st.button("Next"):
        st.session_state.step = 6

elif st.session_state.step == 6:
    st.title("How long does your period usually last?")
    st.session_state.period_duration = st.number_input("Number of days (e.g., 5)", min_value=0, step=1)
    if st.button("Next"):
        st.session_state.step = 7

elif st.session_state.step == 7:
    st.title("Your Health Data is Private.")
    st.write("We are committed to protecting your personal health information.")
    st.session_state.share_data = st.checkbox("Help improve the app by sharing anonymous usage data", value=True)
    if st.button("Finish Setup"):
        c.execute('''
            INSERT INTO user_profiles (
                timestamp, name, age_range, gender, tracking_goals,
                last_period_date, cycle_length, period_duration, share_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            st.session_state.name,
            st.session_state.age_range,
            st.session_state.gender,
            ", ".join(st.session_state.tracking_goals),
            str(st.session_state.last_period_date),
            str(st.session_state.cycle_length),
            str(st.session_state.period_duration),
            "Yes" if st.session_state.share_data else "No"
        ))
        conn.commit()
        st.session_state.step = 8

# --- Voice-Based Tracker ---
elif st.session_state.step == 8:
    st.title("🎙️ Voice-Based Period Health Tracker")
    st.write("Speak and submit below. Your voice and logs will be saved for review.")

    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        os.makedirs("recordings", exist_ok=True)
        file_name = f"recordings/{st.session_state.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(file_name, "wb") as f:
            f.write(audio_bytes)
        st.success(f"Saved your voice as {file_name}")
        st.audio(audio_bytes, format="audio/wav")
        st.info("Simulated AI Response Played (replace this with your backend output)")

    st.write("You can record again any time without reloading the page.")
