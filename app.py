import os
import streamlit as st
from deep_translator import GoogleTranslator
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="Farming Assistant", page_icon="🌾", layout="centered")

# ✅ Get API key only from Streamlit Secrets or Environment
OPENAI_API_KEY = (
    st.secrets.get("OPENAI_API_KEY", None)   # Streamlit Cloud Secrets UI
    or os.environ.get("OPENAI_API_KEY")      # Local env variable
)

st.title("🌾 Farming Assistant (English ↔ Malayalam)")

if not OPENAI_API_KEY:
    st.warning("⚠️ No OpenAI API key found. Please add it in Streamlit Cloud > Settings > Secrets.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.markdown("Ask farming-related questions in English or Malayalam. The app will translate as needed and return answers in both languages.")

with st.form("question_form"):
    user_question = st.text_input("Ask your farming question:")
    submit = st.form_submit_button("Get Answer")

if submit:
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        # Detect Malayalam roughly (Unicode block)
        is_malayalam = any('\u0d00' <= ch <= '\u0d7f' for ch in user_question)

        # Translate Malayalam -> English if needed
        if is_malayalam:
            try:
                question_en = GoogleTranslator(source='ml', target='en').translate(user_question)
            except Exception as e:
                st.error(f"Translation error: {e}")
                question_en = user_question
        else:
            question_en = user_question

        with st.spinner("Contacting AI..."):
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",  # adjust if needed
                    messages=[{"role": "user", "content": question_en}],
                    max_tokens=800
                )
                answer_en = resp.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"OpenAI request failed: {e}")
                answer_en = None

        if answer_en:
            if is_malayalam:
                # Translate back to Malayalam
                try:
                    answer_ml = GoogleTranslator(source='en', target='ml').translate(answer_en)
                except Exception as e:
                    st.error(f"Translation error: {e}")
                    answer_ml = answer_en
                st.success(answer_ml)
                st.markdown("---")
                st.info("English answer (original):\n\n" + answer_en)
            else:
                st.success(answer_en)
                # Also show Malayalam translation
                try:
                    answer_ml = GoogleTranslator(source='en', target='ml').translate(answer_en)
                except Exception:
                    answer_ml = "Translation failed."
                st.markdown("---")
            st.info("Malayalam translation:\n\n" + answer_ml)
