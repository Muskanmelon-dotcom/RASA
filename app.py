import streamlit as st
import sqlite3
import datetime
import openai

# --- Streamlit Page Config ---
st.set_page_config(page_title="Voice Health Tracker", page_icon="🎙️", layout="centered")

# --- Optional Styles ---
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

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
            st.session_state.step = 8

# --- Step 8: Conversational AI Companion ---
elif st.session_state.step == 8:
    st.title("Your AI Support Companion")
    st.write("Start typing your thoughts or concerns below.")

    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        openai.api_key = api_key

        if "messages" not in st.session_state:
            st.session_state.messages = [{
                "role": "system",
                "content": "You are a supportive and empathetic mental health companion named Ash."
            }]

        user_msg = st.text_input("You:")
        if st.button("Send") and user_msg.strip():
            st.session_state.messages.append({"role": "user", "content": user_msg})
            with st.spinner("Ash is thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content.strip()
                st.session_state.messages.append({"role": "assistant", "content": reply})

        for msg in st.session_state.messages[1:]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Ash:** {msg['content']}")

        if st.button("Reset Conversation"):
            st.session_state.pop("messages")
