import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from openai import OpenAI
import fitz
import os
import folium
from streamlit_folium import st_folium
from gtts import gTTS
from PIL import Image
from pathlib import Path
from pydub import AudioSegment

def app():
    
    st.markdown(
    """
    <style>
    /* Change text color inside the selectbox */
    div[data-baseweb="select"] > div {
        color: white;  /* Change this to your preferred color */
    }

    /* Change background color of the selectbox dropdown options */
    div[data-baseweb="select"] > div > div {
        background-color: transparent; /* Background color for the dropdown */
        color: white; /* Text color for the options */
    }

    <style>
    /* Style for selectbox text color (selected option) */
    div[data-baseweb="select"] > div {
        color: white;  /* Text color for selected option */
        background-color: transparent;  /* Background color of the selectbox */
        border-radius: 5px;
        padding: 8px;
    }

    /* Style for text_input */
    input[type="text"] {
        background-color: transparent;  /* Input background color */
        color: #FFFFFF;  /* Input text color */
        border: 1px solid #2b6cb0;  /* Optional: Input border color */
        border-radius: 5px;  /* Optional: Rounding the corners */
        padding: 8px;  /* Padding inside the input box */
    }
     

    /* Style for the placeholder "Choose an option" in the multiselect */
    div[data-baseweb="select"] .css-14jk2my {
        color: white;  /* Placeholder text color */
    }

    /* Style the st.write output boxes */
    .streamlit-expander {
        background-color: #e0f7fa;  /* Light cyan background */
        border-radius: 5px;
        padding: 10px;
        color: white;  /* Dark teal text color */
        font-weight: bold;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Optional box shadow */
    }

    /* Style other generic st.write containers */
    .css-1n76uvr {
        background-color: #e0f7fa; /* Background color */
        color: white; /* Text color */
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


    # Initialize the OpenAI client
    # Do not change this
    client = OpenAI(api_key=st.secrets["MY_API_KEY"])



    # ChatGPT help
    pdf_path = "PDF.pdf"
    def extract_text_from_pdf(pdf_path):    
        if not os.path.isfile(pdf_path):
            print("Error: File not found!")
        else:
            try:
                # Function to extract text from PDF
                def extract_text_from_pdf(pdf_path):
                    text = ""
                    with fitz.open(pdf_path) as pdf:
                        for page_num, page in enumerate(pdf, start=1):
                            text += f"--- Page {page_num} ---\n"
                            text += page.get_text()
                    return text
            except Exception as e:
                print(f"An error occurred: {e}")
    pdf_text = extract_text_from_pdf(pdf_path)
    def get_guided_instructions(pdf_content,prompt,model="gpt-3.5-turbo"):
        completion = client.chat.completions.create(
            model = model,
            messages = [{"role":"system", 
                        "content": "You are a water lines expert. Guide the user step-by-step how to check for leakage using this content: {pdf_content}. Feel free to replace any terms and make it easy to follow for students."},
                        {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content

    def display_image(image_name):
         file_path = Path(__file__).parent / 'images' / image_name
    
        # Load and display the image
         if file_path.is_file():
          img = Image.open(file_path)
          st.image(img, caption='Displayed Image')
         else:
          st.write("Image not found. Please check the file path or name.")

    # Title of the app
    st.title("DIY Water Quality Testing Guide")
    language = "English"  # Only English is supported
    lang_code = 'en'
    st.write("Water is our most precious resource. Climate change and drought can put it at significant risk. Conservation is key to protecting our water supplies. The information contained in the following instructions is based on Valley Water and its contractor’s general experience inspecting homes for water leaks. However, your situation may be unique. Please seek professional advice if you are unsure how to conduct the inspections or install the items.")
    st.write("To get started, gather tools and find your meter box and follow the instructions below to perform the pin test. This test will help you determine if you have a leak in your house line. All other tests will help identify sources of leaks in your home.")
    # Dropdown menu for selecting the test type
    test_options = [
        "Select a test",
        "Pin Test",
        "House Line Test",
        "Toilet Leak Test",
        "Flow Rate Measurement"
    ]
    selected_test = st.selectbox("Choose a water quality test to get started:", test_options)

    # Display information based on the selected test
    if selected_test == "House Line Test":
        st.subheader("House Line Test")
        display_image("house1.png")
        

# Translate the English text to Spanish
        english_text = "Follow these steps to perform the House Line Test"
       
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform house line test that's easy to follow for someone who has never done this test before. Add some information that can encourage users to perform this test. Include clearly separated steps.", model="gpt-3.5-turbo")
        
         # Text-to-speech conversion
        steps = guided_instructions.split('\n')  # Assuming each step is on a new line
    
        st.write("Follow these steps to perform the House Line Test:")
        if "guided_instructions" not in st.session_state:
            st.session_state.guided_instructions = guided_instructions
            st.session_state.steps = guided_instructions.split('\n')
            st.session_state.checked_steps = [False] * len(st.session_state.steps)

    # Check and adjust the list length to match the steps if needed
        if len(st.session_state.checked_steps) != len(st.session_state.steps):
            st.session_state.checked_steps = [False] * len(st.session_state.steps)

    # Display each step with a checkbox
        for idx, step in enumerate(st.session_state.steps):
            if step.strip():  # Ensure step is not empty
                st.session_state.checked_steps[idx] = st.checkbox(
                    f"{step}",
                    value=st.session_state.checked_steps[idx],
                    key=f"step_{idx}"
                )
        
    # Debugging: Show the current state of checkboxes (optional)
    
        
        tts = gTTS(text=guided_instructions, lang=lang_code)
        tts.save("guided_instructions.mp3")
        audio = AudioSegment.from_mp3("guided_instructions.mp3")
        audio.export("guided_instructions.ogg", format="ogg")

        # Display audio player in Streamlit
        if st.button("Play Audio"):
            audio_file = open("guided_instructions.ogg", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/ogg")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    elif selected_test == "Pin Test":
        st.subheader("Pin Test")
        display_image("pin2.png")
        display_image("pin3.png")
        display_image("pin4.png")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform the pin test that's easy to follow for someone who has never done this test before. Add some information that can encourage users to perform this test. Include clearly separated steps.",model="gpt-3.5-turbo")
        steps = guided_instructions.split('\n')  # Assuming each step is on a new line
    
        st.write("Follow these steps to perform the Pin Test:")
        if "pin_test_instructions" not in st.session_state:
            st.session_state.pin_test_instructions = guided_instructions
            st.session_state.pin_test_steps = guided_instructions.split('\n')
            st.session_state.pin_test_checked = [False] * len(st.session_state.pin_test_steps)

    # Check and adjust the list length to match the steps if needed
        if len(st.session_state.pin_test_checked) != len(st.session_state.pin_test_steps):
            st.session_state.pin_test_checked= [False] * len(st.session_state.pin_test_steps)

    # Display each step with a checkbox
        for idx, step in enumerate(st.session_state.pin_test_steps):
            if step.strip():  # Ensure step is not empty
                st.session_state.pin_test_checked[idx] = st.checkbox(
                    f"{step}",
                    value=st.session_state.pin_test_checked[idx],
                    key=f"pin_step_{idx}"
                )
        # Text-to-speech conversion
        tts = gTTS(text=guided_instructions, lang= lang_code)
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    elif selected_test == "Toilet Leak Test":
        st.subheader("Toilet Leak Test")
        display_image("toilet3.png")
        display_image("toilet4.png")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform the toilet leak test that's easy to follow for someone who has never done this test before. Add some information that can encourage users to perform this test. Include clearly separated steps. ",model="gpt-3.5-turbo")
        steps = guided_instructions.split('\n')  # Assuming each step is on a new line
    
        st.write("Follow these steps to perform the Toilet Leak Test:")
        if "toilet_leak_instructions" not in st.session_state:
            st.session_state.toilet_leak_instructions = guided_instructions
            st.session_state.toilet_leak_steps = guided_instructions.split('\n')
            st.session_state.toilet_leak_checked = [False] * len(st.session_state.toilet_leak_steps)

    # Check and adjust the list length to match the steps if needed
        if len(st.session_state.toilet_leak_checked) != len(st.session_state.toilet_leak_steps):
            st.session_state.toilet_leak_checked = [False] * len(st.session_state.toilet_leak_steps)

    # Display each step with a checkbox
        for idx, step in enumerate(st.session_state.toilet_leak_steps):
            if step.strip():  # Ensure step is not empty
                st.session_state.toilet_leak_checked[idx] = st.checkbox(
                    f"{step}",
                    value=st.session_state.toilet_leak_checked[idx],
                    key=f"toilet_step_{idx}"
                )
        # Text-to-speech conversion
        tts = gTTS(text=guided_instructions, lang= lang_code)
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    elif selected_test == "Flow Rate Measurement":
        st.subheader("Flow Rate Measurement")
        guided_instructions = get_guided_instructions(pdf_text, "Instruct user to perform flow rate measurement that's easy to follow for someone who has never done this test before. Add some information that can encourage users to perform this test. Include clearly separated steps. ",model="gpt-3.5-turbo")
        steps = guided_instructions.split('\n')  # Assuming each step is on a new line
    
        st.write("Follow these steps to perform the Flow Rate Measurment Test:")
        if "flow_rate_instructions" not in st.session_state:
            st.session_state.flow_rate_instructions = guided_instructions
            st.session_state.flow_rate_steps = guided_instructions.split('\n')
            st.session_state.flow_rate_checked = [False] * len(st.session_state.flow_rate_steps)

    # Check and adjust the list length to match the steps if needed
        if len(st.session_state.flow_rate_checked) != len(st.session_state.flow_rate_steps):
            st.session_state.flow_rate_checked = [False] * len(st.session_state.flow_rate_steps)

    # Display each step with a checkbox
        for idx, step in enumerate(st.session_state.flow_rate_steps):
            if step.strip():  # Ensure step is not empty
                st.session_state.flow_rate_checked[idx] = st.checkbox(
                    f"{step}",
                    value=st.session_state.flow_rate_checked[idx],
                    key=f"flow_step_{idx}"
                )
        tts = gTTS(text=guided_instructions, lang= lang_code)
        tts.save("guided_instructions.mp3")

        # Display audio player in Streamlit
        audio_file = open("guided_instructions.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

        # Clean up audio file after use
        audio_file.close()
        os.remove("guided_instructions.mp3")
    else:
        st.write("Please select a test to see the instructions.")





