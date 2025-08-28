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

# ✅ This was broken in your copy — fixed now
with st.form("question_form"):
    user_question = st.text_input("Ask your farming question:")
    submit = st.form_submit_button("Get Answer")

if submit:
    if not user_question or user_question.strip() == "":
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
                    model="gpt-4o-mini",  # adjust model if needed
                    messages=[{"role": "user", "content": question_en}],
                    max_tokens=800
                )
                answer_en = resp.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"OpenAI request failed: {e}")
                answer_en = None

        if answer_en:
            if is_malayalam:
                # translate back to Malayalam
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
                # also show Malayalam translation
                try:
                    answer_ml = GoogleTranslator(source='en', target='ml').translate(answer_en)
                except Exception:
                    answer_ml = "Translation failed."
                st.markdown("---")
               st.info("Malayalam translation:\n\n" + answer_ml)


