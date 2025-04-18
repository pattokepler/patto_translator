# main.py
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from faster_whisper import WhisperModel  # [!code ++]
import os 
from groq_translation import groq_translate 
from gtts import gTTS

# Set page config
st.set_page_config(page_title='Patto Translator', page_icon='🎤')

# Set page title
st.title('Patto Translator')

languages = {
   "Portuguese": "pt",
   "Spanish": "es",
   "German": "de",
   "French": "fr",
   "Italian": "it",
   "Dutch": "nl",
   "Russian": "ru",
   "Japanese": "ja",
   "Chinese": "zh",
   "Korean": "ko",
   "Kinyarwanda": "rw"
}

# Language selection
option = st.selectbox(
   "Language to translate to:",
   languages,
   index=None,
   placeholder="Select language...",
)


# Load whisper model
model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=int(os.cpu_count() / 2)) # [!code ++]

# Speech to text
def speech_to_text(audio_chunk): # [!code ++]
    segments, info = model.transcribe(audio_chunk, beam_size=5) # [!code ++]
    speech_text = " ".join([segment.text for segment in segments]) # [!code ++]
    return speech_text # [!code ++]


# Text to speech
def text_to_speech(translated_text, language): # [!code ++]
    file_name = "speech.mp3" # [!code ++]
    my_obj = gTTS(text=translated_text, lang=language) # [!code ++]
    my_obj.save(file_name) # [!code ++]
    return file_name

# Record audio
audio_bytes = audio_recorder()
if audio_bytes and option:
    # Display audio player
    st.audio(audio_bytes, format="audio/wav")

    # Save audio to file
    with open('audio.wav', mode='wb') as f:
        f.write(audio_bytes)
    
    # Speech to text
    st.divider() 
    with st.spinner('Transcribing...'): 
        text = speech_to_text('audio.wav') 
    st.subheader('Transcribed Text') 
    st.write(text) 
    
    # Groq translation
    st.divider() 
    with st.spinner('Translating...'): 
        translation = groq_translate(text, 'en', option) 
    st.subheader('Translated Text to ' + option) 
    st.write(translation.text)

    # Text to speech
    audio_file = text_to_speech(translation.text, languages[option]) 
    st.audio(audio_file, format="audio/mp3") 