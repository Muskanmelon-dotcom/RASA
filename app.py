import streamlit as st
import sqlite3
import datetime

# Page Configuration
st.set_page_config(page_title="Voice Health Tracker", page_icon="🎙️", layout="centered")

# Optional Styles
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Database Setup
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

# Define Pages
pages = [
    {"title": "Welcome to Ash", "text": "You're in the right place.", "button": "Continue"},
    {"title": "How old are you?", "options": ["18 – 24", "25 – 34", "35 – 44", "45 – 54", "55 – 64", "65+", "Prefer not to say"]},
    {"title": "How do you identify?", "options": ["Female", "Male", "Non-binary", "Prefer not to say", "Other"]},
    {"title": "What best describes your race/ethnicity?", "options": ["White / Caucasian", "Black / African American", "Hispanic / Latino", "Asian / South Asian / East Asian", "Native Hawaiian / Pacific Islander", "American Indian / Alaska Native", "Prefer not to say", "Other"]},
    {"title": "What are you most looking for support with?", "options": ["Depression", "Anxiety", "Relationships", "Something else"]},
    {"title": "Our Commitment to You", "text": "Your mental health is personal and private.", "button": "Continue"},
]

# Initialize Session State
if "page" not in st.session_state:
    st.session_state.page = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}

# Progress Indicator
progress_percentage = int((st.session_state.page / (len(pages) + 1)) * 100)
st.progress(progress_percentage, f"Progress: {progress_percentage}%")

# Render Current Page
if st.session_state.page < len(pages):
    current = pages[st.session_state.page]
    st.title(current["title"])

    # Text-only page
    if "text" in current:
        st.markdown(current["text"])
        if st.button(current.get("button", "Next")):
            st.session_state.page += 1

    # Option-selection page
    elif "options" in current:
        choice = st.radio("Select an option:", current["options"], key=f"page_{st.session_state.page}")
        if st.button("Next"):
            st.session_state.responses[current["title"]] = choice
            st.session_state.page += 1

# Final Health Check-in Page
elif st.session_state.page == len(pages):
    st.title("Describe Your Health Today")
    user_input = st.text_area("Speak or type your update")

    # Optional Voice Recorder
    st.subheader("Record Your Voice (Optional)")
    audio_bytes = st.audio_input("Record your voice")

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.success("Audio recorded successfully!")

    if st.button("Submit"):
        if not user_input.strip():
            st.error("Please describe your health to continue.")
        else:
            today_date = datetime.date.today().isoformat()
            c.execute('''
                INSERT INTO health_metrics (date, user_name, user_age, reason, metric_name, metric_value, raw_input_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                today_date,
                st.session_state.responses.get("How do you identify?", "Unknown"),
                st.session_state.responses.get("How old are you?", "Unknown"),
                st.session_state.responses.get("What are you most looking for support with?", "Unknown"),
                "self_reported",
                "submitted",
                user_input
            ))
            conn.commit()
            st.success("Your response has been saved. Thank you!")
            st.balloons()
            # Reset for next user
            st.session_state.page = 0
            st.session_state.responses = {}
