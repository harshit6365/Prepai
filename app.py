# PrepAI — AI Internship Coach
# Vision7Lab — Version 2 with RoadmapBot

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=API_KEY)

st.set_page_config(
    page_title="PrepAI",
    page_icon="🚀",
    layout="centered"
)

st.sidebar.title("🚀 PrepAI")
st.sidebar.caption("by Vision7Lab")
page = st.sidebar.radio("Navigate", [
    "💬 Chat Coach",
    "🗺 RoadmapBot"
])

if page == "💬 Chat Coach":
    st.title("💬 PrepAI Chat Coach")
    st.caption("Ask me anything about internships")
    st.divider()

    SYSTEM_PROMPT = """
    You are PrepAI, an AI internship coach for Indian engineering students.
    Help students with skills, projects, interviews, and resumes.
    Be friendly, specific, and practical.
    Always give advice relevant to the Indian tech job market.
    """

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

elif page == "🗺 RoadmapBot":
    st.title("🗺 RoadmapBot")
    st.caption("Get your personalised week-by-week internship roadmap")
    st.divider()

    with st.form("roadmap_form"):
        name = st.text_input("Your Name")
        
        current_skills = st.multiselect(
            "Your current skills",
            ["Python basics", "HTML/CSS", "JavaScript", "React",
             "Machine Learning", "Data Analysis", "SQL",
             "Git/GitHub", "Java", "C++", "None yet"]
        )
        
        target_role = st.selectbox(
            "Target internship role",
            ["AI/ML Engineer", "Python Developer", "Web Developer",
             "Data Analyst", "Full Stack Developer", "Product Manager"]
        )
        
        hours_per_day = st.slider(
            "Hours available per day", 1, 8, 3
        )
        
        weeks_available = st.slider(
            "Weeks available to prepare", 2, 12, 6
        )
        
        submitted = st.form_submit_button("Generate My Roadmap 🚀")

    if submitted:
        if not name or not current_skills:
            st.error("Please fill in your name and select at least one skill!")
        else:
            prompt = f"""
            Create a detailed week-by-week internship preparation roadmap for:
            
            Name: {name}
            Current Skills: {', '.join(current_skills)}
            Target Role: {target_role}
            Hours per day: {hours_per_day}
            Weeks available: {weeks_available}
            
            Format the roadmap clearly with:
            - Week number and title
            - What to learn that week
            - What to build that week
            - Resources to use (free only)
            - Goal for the week
            
            Make it specific, actionable, and realistic for an Indian engineering student.
            Focus on getting them internship-ready within {weeks_available} weeks.
            """

            with st.spinner("Building your personalised roadmap..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                roadmap = response.choices[0].message.content

            st.success(f"✅ Your personalised roadmap is ready, {name}!")
            st.divider()
            st.markdown(roadmap)
            
            st.divider()
            st.download_button(
                label="📥 Download Roadmap",
                data=roadmap,
                file_name=f"{name}_internship_roadmap.txt",
                mime="text/plain"
            )