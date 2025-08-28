# app.py
import os
import streamlit as st
from deep_translator import GoogleTranslator
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="Farming Assistant", page_icon="🌾", layout="centered")

# Get API key: priority -> Streamlit secrets -> env var -> direct input field (for quick testing)
OPENAI_API_KEY = (
    st.secrets.get("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", None)  # if deployed to Streamlit Cloud with secrets
    or os.environ.get("OPENAI_API_KEY")     # or environment variable
)

st.title("🌾 Farming Assistant (English ↔ Malayalam)")

if not OPENAI_API_KEY:
    st.warning("No OpenAI API key found. You can paste it below for this session (not saved).")
    key_input = st.text_input("Paste OpenAI API key (sk-...)", type="password")
    if key_input:
        OPENAI_API_KEY = key_input

if not OPENAI_API_KEY:
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.markdown("Ask farming-related questions in English or Malayalam. The app will translate as needed and return answers in both languages.")

with st.form("q
