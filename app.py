import streamlit as st
import os
import sys
import time
import subprocess
from googletrans import Translator

TRANSLATED_TEXT_PATH = "./_connector/translated_text.txt"
OUTPUT_AUDIO_PATH = "./_connector/generated_output.wav"

def generate_sound(text):
    st.write("**Translated Text:**")
    translator = Translator()
    translated_text = translator.translate(text, src="auto", dest="ja").text
    st.write(translated_text)
    with open(TRANSLATED_TEXT_PATH, "w", encoding="utf-8") as f:
        f.write(translated_text)
    
    st.write("**Generating Audio...**")
    
    loading_placeholder = st.empty()
    loading_placeholder.write("⏳ Starting audio generation...")
    
    if os.path.exists(OUTPUT_AUDIO_PATH): os.remove(OUTPUT_AUDIO_PATH)
    subprocess.run([f"{sys.executable}", "_inference_only,py", text])
    
    st.write("**Audio:**")
    
    max_wait = 120
    waiting_time = 0
    
    while waiting_time < max_wait:
        if os.path.exists(OUTPUT_AUDIO_PATH):
            time.sleep(1)
            st.audio(OUTPUT_AUDIO_PATH, format='audio/wav')
            break
        time.sleep(1)
        waiting_time += 1
        loading_placeholder.write(f"⏳ Processing... ({waiting_time}s)")

st.title("Indonesian Folk Story Storytelling in Japanese Language with Text-to-speech (TTS)")

story_choice = st.selectbox(
    'Story Choices:',
    ('Danau Toba', 'Kisah Putri Ular', 'Malin Kundang'),
    key='story_selector'
)

if st.button('Tell me the story! (preset story)'):
    if story_choice == 'Danau Toba':
        st.write("Danau Toba")
        st.audio("./story_data/jp/danau_toba.wav", format='audio/wav')
    elif story_choice == 'Kisah Putri Ular':
        st.write("Kisah Putri Ular")
        st.audio("./story_data/jp/kisah_putri_ular.wav", format='audio/wav')
    elif story_choice == 'Malin Kundang':
        st.write("Malin Kundang")
        st.audio("./story_data/jp/malin_kundang.wav", format='audio/wav')
    elif story_choice == 'Generate New Story from Text':
        st.write("Enter your story text below and click 'Generate Sound'")

user_input = st.text_area("Enter your story text here:", key="story_text")
if st.button("Generate Sound", key="generate_btn"):
    if user_input:
        st.write("Your custom story will be processed...")
        generate_sound(user_input)
    else:
        st.warning("Please enter some text first!")
