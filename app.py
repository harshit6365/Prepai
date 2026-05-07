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
    "🗺 RoadmapBot",
    "🛠 ProjectBot",
    "🎤 InterviewBot"
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

        hours_per_day = st.slider("Hours available per day", 1, 8, 3)
        weeks_available = st.slider("Weeks available to prepare", 2, 12, 6)

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

            Format with:
            - Week number and title
            - What to learn
            - What to build
            - Free resources
            - Weekly goal

            Make it specific and realistic for an Indian engineering student.
            """

            with st.spinner("Building your personalised roadmap..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                roadmap = response.choices[0].message.content

            st.success(f"✅ Your roadmap is ready, {name}!")
            st.divider()
            st.markdown(roadmap)
            st.divider()
            st.download_button(
                label="📥 Download Roadmap",
                data=roadmap,
                file_name=f"{name}_roadmap.txt",
                mime="text/plain"
            )

elif page == "🛠 ProjectBot":
    st.title("🛠 ProjectBot")
    st.caption("Get 3 perfect project ideas for your portfolio")
    st.divider()

    with st.form("project_form"):
        skill_level = st.selectbox(
            "Your skill level",
            ["Complete Beginner", "Basic Python known",
             "Intermediate - know APIs", "Advanced"]
        )

        target_role = st.selectbox(
            "Target internship role",
            ["AI/ML Engineer", "Python Developer", "Web Developer",
             "Data Analyst", "Full Stack Developer"]
        )

        time_available = st.selectbox(
            "Time to build project",
            ["1 week", "2 weeks", "1 month"]
        )

        interests = st.multiselect(
            "Your interests",
            ["Education", "Healthcare", "Finance", "Music",
             "Sports", "Social Media", "E-commerce", "Gaming",
             "Environment", "Travel"]
        )

        submitted2 = st.form_submit_button("Get My Project Ideas 🛠")

    if submitted2:
        if not interests:
            st.error("Please select at least one interest!")
        else:
            prompt = f"""
            Suggest 3 perfect projects for an internship portfolio:
            Skill Level: {skill_level}
            Target Role: {target_role}
            Time Available: {time_available}
            Interests: {', '.join(interests)}

            For each project:
            1. Project name and description
            2. Problem it solves
            3. Tech stack
            4. Step by step how to build
            5. GitHub README tips
            6. How to explain in interview
            7. Time to complete

            Make it realistic for Indian tech internships.
            """

            with st.spinner("Finding perfect projects for you..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                projects = response.choices[0].message.content

            st.success("✅ Here are your 3 perfect projects!")
            st.divider()
            st.markdown(projects)
            st.divider()
            st.download_button(
                label="📥 Download Project Ideas",
                data=projects,
                file_name="project_ideas.txt",
                mime="text/plain"
            )

elif page == "🎤 InterviewBot":
    st.title("🎤 InterviewBot")
    st.caption("Practice mock interviews and get instant feedback")
    st.divider()

    if "interview_messages" not in st.session_state:
        st.session_state.interview_messages = []
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    if not st.session_state.interview_started:
        role = st.selectbox(
            "Select interview type",
            ["AI/ML Engineer", "Python Developer",
             "Web Developer", "Data Analyst"]
        )

        if st.button("Start Interview 🎤"):
            st.session_state.interview_started = True
            st.session_state.interview_role = role
            st.session_state.question_count = 0
            st.session_state.interview_messages = []

            first_prompt = f"""
            You are a technical interviewer at a top Indian tech company.
            You are interviewing a student for a {role} internship.
            Rules:
            - Ask exactly 5 questions one by one
            - Wait for student to answer before next question
            - After each answer give brief feedback
            - After 5 questions give final score out of 10 and detailed feedback
            - Start by introducing yourself and asking question 1
            """

            with st.spinner("Starting your interview..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": first_prompt}]
                )
                first_question = response.choices[0].message.content

            st.session_state.interview_messages.append({
                "role": "assistant",
                "content": first_question
            })
            st.rerun()

    else:
        st.info(f"🎤 Mock Interview — {st.session_state.interview_role} Internship")

        if st.button("❌ End Interview"):
            st.session_state.interview_started = False
            st.session_state.interview_messages = []
            st.session_state.question_count = 0
            st.rerun()

        for msg in st.session_state.interview_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_answer = st.chat_input("Type your answer...")

        if user_answer:
            with st.chat_message("user"):
                st.write(user_answer)

            st.session_state.interview_messages.append({
                "role": "user",
                "content": user_answer
            })
            st.session_state.question_count += 1

            with st.spinner("Interviewer is responding..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a technical interviewer for {st.session_state.interview_role} internship. Ask 5 questions total. Question count so far: {st.session_state.question_count}. After 5 answers give final score out of 10."
                        },
                        *st.session_state.interview_messages
                    ]
                )
                interviewer_reply = response.choices[0].message.content

            with st.chat_message("assistant"):
                st.write(interviewer_reply)

            st.session_state.interview_messages.append({
                "role": "assistant",
                "content": interviewer_reply
            })
            st.rerun()