import streamlit as st
from reco import record_audio, recognize_speech, save_audio
import matplotlib.pyplot as plt
import numpy as np
import wave

# Page configuration
st.set_page_config(
    page_title="SayItNow",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced custom styles
st.markdown(
    """
    <style>
    /* Main container styling */
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Header styling */
    .title-container {
        background: linear-gradient(90deg, #2c3e50, #3498db);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #2c3e50, #3498db);
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.5rem 0;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }

    /* Download button styling */
    .download-button {
        background-color: #27ae60 !important;
    }

    /* Success message styling */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }

    /* Card styling */
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom container for title
st.markdown(
    """
    <div class='title-container'>
        <h1 style='font-size: 3rem;'>🎙️ SayItNow</h1>
        <h2 style='font-size: 3rem;'> Instant Voice-to-Text Magic!</h2>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Transform your voice into text with advanced speech recognition</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Create two columns for main content
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Recording Status")
    status_placeholder = st.empty()  # Placeholder to show recording status
    progress_bar = st.progress(0)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🎮 Controls")

    # Check if a recording session is active
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False

    if not st.session_state.is_recording:
        if st.button("🎤 Start Recording", key="record_button"):
            st.session_state.is_recording = True
            status_placeholder.markdown("🔴 Recording in progress...")

            # Record audio
            audio = record_audio()

            # Simulate progress during recording
            for i in range(100):
                progress_bar.progress(i + 1)
                if i == 99:
                    status_placeholder.markdown("✅ Recording complete!")
                    save_audio(audio)  # Save the audio only after completion
            st.session_state.is_recording = False

            # Recognition
            text = recognize_speech(audio)

            # Update session state
            st.session_state.recorded_text = text
            st.session_state.has_recording = True
    else:
        # If recording is active, show stop button and progress
        if st.button("⏹️ Stop Recording", key="stop_record_button"):
            st.session_state.is_recording = False
            status_placeholder.markdown("✅ Recording stopped manually.")
            save_audio(audio)

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Recognition Results")

    if 'has_recording' in st.session_state and st.session_state.has_recording:
        st.markdown(
            f"""
            <div class='success-message'>
                <h3>Recognized Text:</h3>
                <p style='font-size: 1.2rem;'>{st.session_state.recorded_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Waveform visualization
        st.subheader("📈 Audio Waveform")
        with wave.open("recorded.wav", "rb") as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            signal = np.frombuffer(frames, dtype=np.int16)
            framerate = wav_file.getframerate()
            time = np.linspace(0, len(signal) / framerate, num=len(signal))

            fig, ax = plt.subplots(figsize=(12, 4))
            ax.plot(time, signal, color="#3498db", alpha=0.7)
            ax.fill_between(time, signal, alpha=0.1, color="#3498db")
            ax.set_title("Audio Waveform Visualization", pad=20)
            ax.set_xlabel("Time (seconds)")
            ax.set_ylabel("Amplitude")
            ax.grid(True, alpha=0.3)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Set background color
            fig.patch.set_facecolor('#ffffff')
            ax.set_facecolor('#ffffff')

            st.pyplot(fig)

        # Download section
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("💾 Download Options")
        col3, col4 = st.columns(2)

        with col3:
            with open("recorded.wav", "rb") as f:
                st.download_button(
                    label="⬇️ Download Audio",
                    data=f,
                    file_name="recorded.wav",
                    mime="audio/wav",
                    key="download-audio",
                )

        with col4:
            # Add text download option
            st.download_button(
                label="📄 Download Text",
                data=st.session_state.recorded_text,
                file_name="transcript.txt",
                mime="text/plain",
                key="download-text",
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Click 'Start Recording' to begin capturing audio.")
    st.markdown("</div>", unsafe_allow_html=True)