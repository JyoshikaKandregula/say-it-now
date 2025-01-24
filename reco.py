import speech_recognition as sr

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def recognize_speech(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def save_audio(audio, filename="recorded.wav"):
    with open(filename, "wb") as f:
        f.write(audio.get_wav_data())
