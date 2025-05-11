import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {
    "Content-Type": "application/json"
}

def get_predictions(text, count=3):
    payload = {
        "contents": [{
            "parts": [{"text": text}]
        }]
    }

    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if "candidates" in data:
            return [item['content']['parts'][0]['text'] for item in data['candidates']][:count]
        else:
            return ["No result."]
    except requests.exceptions.RequestException as e:
        return [f"Error: {str(e)}"]

st.set_page_config(page_title="Sentence Prediction", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)

st.title(" Sentence Prediction Tool")
st.write("Enter a sentence and get possible next sentence suggestions using the Gemini API.")

text = st.text_area("Input Text", height=150)
count = st.slider("Number of Predictions", 1, 3, 2)

if st.button("Generate Predictions"):
    if text.strip():
        with st.spinner("Generating..."):
            results = get_predictions(text, count)
            st.subheader("Results:")
            for i, result in enumerate(results):
                st.write(f"{i + 1}. {result}")
    else:
        st.warning("Please enter a sentence first.")

st.markdown("</div>", unsafe_allow_html=True)
