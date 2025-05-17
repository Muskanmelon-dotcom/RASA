import streamlit as st
import os
import datetime
import io

# --- Streamlit Page Config ---
st.set_page_config(page_title="Voice-Only ChatGPT Prototype", page_icon="🎙️", layout="centered")
st.title("🎙️ Voice-Only ChatGPT (Prototype)")

# --- Create Recordings Folder ---
os.makedirs("recordings", exist_ok=True)

# --- Voice Interaction Section ---
st.subheader("Speak and Submit Below (Simulated AI Will Reply)")

audio_bytes = st.audio_input("Record your voice")

if audio_bytes:
    # Save the uploaded audio
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recordings/user_{timestamp}.wav"
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    st.success(f"🎧 Saved your voice as {filename}")

    # Simulated AI voice response (replace with your backend integration later)
    st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav", format="audio/wav", start_time=0)
    st.info("Simulated AI Response Played (replace this with your backend output)")

st.write("You can record again any time without reloading the page.")
