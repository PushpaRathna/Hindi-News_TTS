# app.py

import streamlit as st
from summarizer import process_company_news

st.set_page_config(page_title="📰 Hindi News Summarizer", layout="centered")

st.title("📰 Hindi News Summarizer & Sentiment Analyzer")
st.markdown("Enter a company name to fetch recent news in Hindi, summarize the content, analyze sentiment, and listen to a Hindi TTS report.")

# 👉 Input box
company = st.text_input("🔍 Enter Company Name (in English or Hindi):", placeholder="e.g., LIC")

# 👉 Button to trigger processing
if st.button("Generate Report"):
    if not company.strip():
        st.warning("⚠️ Please enter a valid company name.")
    else:
        with st.spinner("⏳ Fetching and processing news..."):
            result, audio_path = process_company_news(company)

            # Error case
            if isinstance(result, str) and result.startswith("❌"):
                st.error(result)
            else:
                # Show articles
                st.success("✅ Report Ready!")
                for i, article in enumerate(result, 1):
                    st.subheader(f"📰 Article {i}")
                    st.write(f"**Title:** {article['Title']}")
                    st.write(f"**Summary:** {article['Summary']}")
                    st.write(f"**Sentiment:** {article['Sentiment']}")

                # Play audio
                if audio_path:
                    st.audio(audio_path, format="audio/mp3")
