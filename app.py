# PrepAI — AI Internship Coach
# Vision7Lab — Powered by Groq (Free & Fast)

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from groq import Groq

# Paste your Groq API key here
import os
API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """
You are PrepAI, an AI internship coach for Indian engineering students.
You help students with:
- What skills to learn for their target internship
- What projects to build for their portfolio
- How to crack interviews
- How to write resumes and cover letters

Be friendly, specific, and practical.
Always give advice relevant to the Indian tech job market.
Keep responses clear and actionable.
"""

st.set_page_config(
    page_title="PrepAI",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 PrepAI")
st.caption("AI Internship Coach for Indian Students — by Vision7Lab")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    st.info("👋 Hi! I'm PrepAI. Tell me your current skills and target internship — I'll give you a personalised plan!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask me anything about internships...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("PrepAI is thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *st.session_state.messages
            ]
        )
        ai_reply = response.choices[0].message.content

    with st.chat_message("assistant"):
        st.write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })