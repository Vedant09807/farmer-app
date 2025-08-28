import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator

# Initialize OpenAI
client = OpenAI(api_key="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")
  # replace with your API key

st.title("🌾 Farming Assistant (English ↔ Malayalam)")

# Input
user_question = st.text_input("Ask your farming question:")

if st.button("Get Answer"):
    if user_question:
        # Detect language (simple check: Malayalam unicode range)
        is_malayalam = any('\u0d00' <= ch <= '\u0d7f' for ch in user_question)

        if is_malayalam:
            # Translate Malayalam → English
            question_en = GoogleTranslator(source='ml', target='en').translate(user_question)
        else:
            question_en = user_question

        # Get AI answer in English
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question_en}]
        )
        answer_en = response.choices[0].message.content

        # Translate back if needed
        if is_malayalam:
            answer_ml = GoogleTranslator(source='en', target='ml').translate(answer_en)
            st.success(answer_ml)
            st.markdown("---")
            st.info("English Answer:\n\n" + answer_en)
        else:
            st.success(answer_en)
            answer_ml = GoogleTranslator(source='en', target='ml').translate(answer_en)
            st.markdown("---")
            st.info("Malayalam Answer:\n\n" + answer_ml)
    else:
        st.warning("Please enter a question.")

