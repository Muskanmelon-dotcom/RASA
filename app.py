import streamlit as st
import os
from datetime import datetime as dt

# --- Streamlit Config ---
st.set_page_config(page_title="Period Health Voice Tracker", page_icon="🩸", layout="centered")

# --- Initialize Session State ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "profile" not in st.session_state:
    st.session_state.profile = {}

# --- Step 1: Welcome ---
if st.session_state.step == 1:
    st.title("🩸 Track Your Cycle, Understand Your Body")
    st.write("We help you easily log period dates, symptoms, and moods to reveal patterns and insights about your health.")
    if st.button("Get Started"):
        st.session_state.step = 2

# --- Step 2: Basic Info ---
elif st.session_state.step == 2:
    st.title("Tell us a little about yourself.")
    age = st.radio("How old are you?", ["18-24", "25-34", "35-44", "45-54", "55+", "Prefer not to say"])
    gender = st.radio("How do you identify?", ["Female", "Male", "Non-binary", "Prefer not to say", "Other"])
    if st.button("Next"):
        st.session_state.profile["age"] = age
        st.session_state.profile["gender"] = gender
        st.session_state.step = 3

# --- Step 3: Tracking Goals ---
elif st.session_state.step == 3:
    st.title("What are you hoping to track?")
    goals = st.multiselect(
        "Select all that apply:",
        ["Predicting my period", "Understanding symptoms", "Tracking irregularities", 
         "Fertility tracking", "General health awareness", "Something else"]
    )
    if st.button("Next"):
        st.session_state.profile["goals"] = goals
        st.session_state.step = 4

# --- Step 4: Last Period ---
elif st.session_state.step == 4:
    st.title("When did your last period start?")
    last_period = st.date_input("Select date (optional)")
    if st.button("Next"):
        st.session_state.profile["last_period"] = str(last_period)
        st.session_state.step = 5

# --- Step 5: Cycle Length ---
elif st.session_state.step == 5:
    st.title("What's your typical cycle length? (optional)")
    cycle_length = st.number_input("Enter in days (optional)", min_value=0, max_value=60, value=28)
    if st.button("Next"):
        st.session_state.profile["cycle_length"] = cycle_length
        st.session_state.step = 6

# --- Step 6: Period Duration ---
elif st.session_state.step == 6:
    st.title("How long does your period usually last? (optional)")
    duration = st.number_input("Enter in days (optional)", min_value=0, max_value=15, value=5)
    if st.button("Next"):
        st.session_state.profile["period_duration"] = duration
        st.session_state.step = 7

# --- Step 7: Privacy Notice ---
elif st.session_state.step == 7:
    st.title("Your Health Data is Private.")
    st.write("We are committed to protecting your personal health information.")
    share_data = st.checkbox("Help improve the app by sharing anonymous usage data", value=True)
    if st.button("Finish Setup"):
        st.session_state.profile["share_data"] = share_data
        st.session_state.step = 8

# --- Step 8: Voice Interaction ---
elif st.session_state.step == 8:
    st.title("🎙️ Voice-Based Period Health Tracker")
    st.write("Speak and submit below. Your voice and logs will be saved for review.")

    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
        save_dir = "recordings"
        os.makedirs(save_dir, exist_ok=True)
        file_path = f"{save_dir}/user_{timestamp}.wav"
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        st.success(f"Saved your voice as {file_path}")
        st.audio(audio_bytes, format="audio/wav")
        st.info("Simulated AI Response Played (replace with your backend)")

    st.write("You can record again any time without reloading the page.")
