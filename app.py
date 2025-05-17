import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Voice Chat Prototype", page_icon="🎙️")

st.title("🎙️ Voice-Based Conversational AI (Prototype)")

# Create folder to save audio files
SAVE_DIR = "recordings"
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize session state
if "conversation_round" not in st.session_state:
    st.session_state.conversation_round = 1

st.header(f"Round {st.session_state.conversation_round}: Your Turn")
audio_bytes = st.audio_input("Record your voice and click Submit")

if audio_bytes:
    # Save user audio correctly by reading bytes
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user_filename = f"{SAVE_DIR}/user_round_{st.session_state.conversation_round}_{timestamp}.wav"
    with open(user_filename, "wb") as f:
        f.write(audio_bytes.read())
    st.success(f"Saved your voice as {user_filename}")

    # Simulated AI response (replace with real backend-generated audio)
    dummy_response_path = "dummy_response.wav"  # Replace with real backend response
    if os.path.exists(dummy_response_path):
        st.audio(dummy_response_path, format="audio/wav")
    else:
        st.info("AI Response would play here (simulate with your backend)")

    if st.button("Next Round"):
        st.session_state.conversation_round += 1
        st.experimental_rerun()
