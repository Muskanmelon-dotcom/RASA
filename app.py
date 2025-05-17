import streamlit as st
import os
import datetime
import uuid

# --- Streamlit Config ---
st.set_page_config(page_title="Voice Health Companion", page_icon="🎙️", layout="centered")

# --- Styles ---
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- Session State ---
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎙️ Voice Health Companion")

st.write("Talk to your companion by recording your voice below. You’ll hear a voice response in return.")

# --- Voice Input ---
audio_bytes = st.audio_input("Press to Record and Speak")

if audio_bytes:
    # --- Save Audio ---
    save_folder = "saved_audio"
    os.makedirs(save_folder, exist_ok=True)
    filename = f"{st.session_state.conversation_id}_{len(st.session_state.history)}.wav"
    filepath = os.path.join(save_folder, filename)
    with open(filepath, "wb") as f:
        f.write(audio_bytes)
    st.success(f"Saved your voice as {filename}")

    # --- Append to History ---
    st.session_state.history.append({"user_audio": filepath})

    # --- Placeholder for Backend Response ---
    st.info("Sending audio to backend for processing...")
    
    # Simulate voice response file (replace this with your backend logic)
    # Here you can fetch `response_audio_file` from your backend processing
    response_audio_file = filepath  # Dummy: Echoing back the same file

    st.session_state.history[-1]["assistant_audio"] = response_audio_file

# --- Playback Conversation History ---
for i, entry in enumerate(st.session_state.history, 1):
    st.markdown(f"**You (Turn {i}):**")
    st.audio(open(entry["user_audio"], "rb").read(), format="audio/wav")

    st.markdown(f"**Assistant (Turn {i}):**")
    st.audio(open(entry["assistant_audio"], "rb").read(), format="audio/wav")

# --- Reset Conversation ---
if st.button("🔄 Reset Conversation"):
    st.session_state.conversation_id = str(uuid.uuid4())
    st.session_state.history = []
    st.experimental_rerun()
