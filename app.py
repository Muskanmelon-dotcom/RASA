import streamlit as st
import sqlite3
import datetime
import os
from datetime import datetime as dt

# --- Page Config ---
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
        ethnicity TEXT,
        primary_concern TEXT
    )
''')
conn.commit()

# --- Session State ---
if "step" not in st.session_state:
    st.session_state.step = 1

# --- Step 1: Welcome ---
if st.session_state.step == 1:
    st.title("🩸 Period Health Voice Tracker")
    st.write("You're in the right place to track your cycle, symptoms, and feelings with your voice.")
    if st.button("Continue"):
        st.session_state.step = 2

# --- Step 2: Name ---
elif st.session_state.step == 2:
    st.title("Step 1: What's your name?")
    name = st.text_input("Enter your name")
    if st.button("Next"):
        if not name.strip():
            st.error("Please enter your name.")
        else:
            st.session_state.name = name
            st.session_state.step = 3

# --- Step 3: Age Range ---
elif st.session_state.step == 3:
    st.title("Step 2: Select your age range")
    age_range = st.radio("Choose one", ["18-24", "25-34", "35-44", "45-54", "55+", "Prefer not to say"])
    if st.button("Next"):
        st.session_state.age_range = age_range
        st.session_state.step = 4

# --- Step 4: Ethnicity ---
elif st.session_state.step == 4:
    st.title("Step 3: Your ethnicity")
    ethnicity = st.radio("Select one", [
        "Asian / South Asian", "White / Caucasian", "Black / African American",
        "Hispanic / Latino", "Native Hawaiian / Pacific Islander",
        "American Indian / Alaska Native", "Prefer not to say", "Other"
    ])
    if st.button("Next"):
        st.session_state.ethnicity = ethnicity
        st.session_state.step = 5

# --- Step 5: Primary Concern ---
elif st.session_state.step == 5:
    st.title("Step 4: What do you need the most support with?")
    concern = st.radio("Select one", ["Cycle Tracking", "Mood Tracking", "Symptom Tracking", "Something Else"])
    if st.button("Continue to Voice Tracker"):
        st.session_state.primary_concern = concern
        timestamp = dt.now().isoformat()
        c.execute('''
            INSERT INTO user_profiles (timestamp, name, age_range, gender, ethnicity, primary_concern)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, st.session_state.name, st.session_state.age_range, "Female", st.session_state.ethnicity, concern))
        conn.commit()
        st.session_state.step = 6

# --- Step 6: Voice-Based Tracker ---
elif st.session_state.step == 6:
    st.title("🎙️ Voice-Based Period Health Tracker")
    st.write("Speak and submit below. Your voice and logs will be saved for review.")

    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
        save_dir = "recordings"
        os.makedirs(save_dir, exist_ok=True)
        file_path = f"{save_dir}/{st.session_state.name}_{timestamp}.wav"
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        st.success(f"Saved your voice as {file_path}")
        st.audio(audio_bytes, format="audio/wav")
        st.info("Simulated AI Response Played (replace this with your backend output)")

    st.write("You can record again any time without reloading the page.")
