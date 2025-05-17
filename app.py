import streamlit as st
import os
from datetime import datetime

# --- Streamlit Config ---
st.set_page_config(page_title="Voice Period Health Tracker", page_icon="🩸", layout="centered")

# --- Initialize States ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- Step 1: Welcome ---
if st.session_state.step == 1:
    st.title("🩸 Track Your Cycle, Understand Your Body")
    st.write("We help you easily log period dates, symptoms, and moods to reveal patterns and insights about your health.")
    if st.button("Get Started"):
        st.session_state.step = 2

# --- Step 2: Basic Info ---
elif st.session_state.step == 2:
    st.title("👤 Tell us a little about yourself")
    name = st.text_input("What's your name?")
    age_range = st.radio("How old are you?", ["18-24", "25-34", "35-44", "45-54", "55+", "Prefer not to say"])
    gender = st.radio("How do you identify?", ["Female", "Male", "Non-binary", "Other", "Prefer not to say"])
    if st.button("Next"):
        st.session_state.user_profile.update({"name": name, "age_range": age_range, "gender": gender})
        st.session_state.step = 3

# --- Step 3: Tracking Goals ---
elif st.session_state.step == 3:
    st.title("🎯 What are you hoping to track?")
    goals = st.multiselect(
        "Select all that apply",
        ["Predicting my period", "Understanding symptoms", "Tracking irregularities",
         "Trying to conceive", "General health awareness", "Something else"]
    )
    if st.button("Next"):
        st.session_state.user_profile["goals"] = goals
        st.session_state.step = 4

# --- Step 4: Last Period ---
elif st.session_state.step == 4:
    st.title("🩸 When did your last period start?")
    last_period_date = st.date_input("Pick the start date of your last period")
    if st.button("Next"):
        st.session_state.user_profile["last_period"] = str(last_period_date)
        st.session_state.step = 5

# --- Step 5: Cycle Length ---
elif st.session_state.step == 5:
    st.title("🔄 What's your typical cycle length?")
    cycle_length = st.number_input("Enter the number of days", min_value=21, max_value=35, step=1)
    if st.button("Next"):
        st.session_state.user_profile["cycle_length"] = cycle_length
        st.session_state.step = 6

# --- Step 6: Period Duration ---
elif st.session_state.step == 6:
    st.title("🩸 How long does your period usually last?")
    period_duration = st.number_input("Enter the number of days", min_value=1, max_value=10, step=1)
    if st.button("Next"):
        st.session_state.user_profile["period_duration"] = period_duration
        st.session_state.step = 7

# --- Step 7: Privacy ---
elif st.session_state.step == 7:
    st.title("🔒 Your Health Data is Private")
    share_data = st.checkbox("Help improve the app by sharing anonymous usage data", value=False)
    st.session_state.user_profile["share_data"] = share_data
    if st.button("Finish Setup"):
        st.session_state.step = 8

# --- Step 8: Voice Tracker ---
elif st.session_state.step == 8:
    st.title("🎙️ Voice-Based Period Health Tracker")
    st.write("Record updates about your health below. Your voice and conversation will be saved.")

    audio_bytes = st.audio_input("Press record and speak your update")

    if audio_bytes:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("recordings", exist_ok=True)
        file_path = f"recordings/{st.session_state.user_profile.get('name', 'user')}_{timestamp}.wav"
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        # Simulated Transcription and Response
        transcription = "Simulated transcription of your voice input."
        ai_response = "Simulated AI response based on your input."

        # Display and Log
        st.markdown(f"**You said:** {transcription}")
        st.markdown(f"**AI replied:** {ai_response}")
        st.audio(audio_bytes, format="audio/wav")

        st.session_state.conversation.append({
            "audio_file": file_path,
            "transcription": transcription,
            "response": ai_response
        })

    if st.session_state.conversation:
        st.markdown("### 📝 Conversation History")
        for idx, entry in enumerate(st.session_state.conversation, start=1):
            st.markdown(f"**Turn {idx}:**")
            st.markdown(f"- Audio File: `{entry['audio_file']}`")
            st.markdown(f"- Transcription: {entry['transcription']}")
            st.markdown(f"- AI Response: {entry['response']}")
            st.markdown("---")

    st.write("Feel free to record again any time without reloading the page.")
