import streamlit as st
import google.generativeai as genai
import pdfplumber
import docx
import tempfile
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API Key not found. Please set the GOOGLE_API_KEY in your .env file.")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-1.0-pro')

    # Initialize Streamlit app
    st.title("TalentScout Hiring Assistant")
    st.sidebar.title("Candidate Details")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "greeted" not in st.session_state:
        st.session_state.greeted = False

    st.sidebar.subheader("Upload Resume (PDF/DOCX)")
    uploaded_file = st.sidebar.file_uploader("Choose your resume", type=['pdf', 'docx'])

    def extract_resume_text(uploaded_file):
        text = ""
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

                if uploaded_file.name.endswith(".pdf"):
                    with pdfplumber.open(temp_path) as pdf:
                        for page in pdf.pages:
                            text += page.extract_text() or ""
                elif uploaded_file.name.endswith(".docx"):
                    doc = docx.Document(temp_path)
                    for para in doc.paragraphs:
                        text += para.text + "\n"
        return text.strip()

    resume_text = extract_resume_text(uploaded_file)

    with st.sidebar.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")

        qualification = st.selectbox(
            "Highest Qualification",
            ["Select", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD"]
        )
        college_name = st.text_input("College/University Name")

        tech_stack = st.text_area("Tech Stack (e.g., Python, Django, MySQL)")
        submit = st.form_submit_button("Submit")

    if submit and not st.session_state.greeted:
        st.session_state.greeted = True
        st.write(f"**Namaste {name}! 👋**")
        st.write(f"Welcome to TalentScout! How’s everything going in **{location}**?")
        st.write(f"Your **{qualification}** from **{college_name}** sounds impressive! Let's get started. 😊")

        if resume_text:
            st.write("📄 **Resume Extracted Successfully!**")
            st.write(resume_text[:300] + "...")
        else:
            st.write("No resume uploaded or extracted. Proceeding with available details.")

        tech_stack_list = [tech.strip() for tech in tech_stack.split(',')]

        for tech in tech_stack_list:
            tech_prompt = f"""
            Based on the candidate's experience and skills in {tech}, generate 3-5 technical questions.
            Questions should test proficiency, practical experience, and problem-solving skills for {tech}.
            """
            response_tech = model.generate_content(tech_prompt)
            st.write(f"### Questions related to {tech}:")
            st.write(response_tech.text)

        if resume_text:
            resume_prompt = f"""
            Based on the resume of {name}, generate personalized questions that probe into the candidate's experience with projects, skills, and work history.
            The candidate has experience in the following tech stack: {tech_stack}.
            Resume content:
            {resume_text}
            """
            response_resume = model.generate_content(resume_prompt)
            st.write(f"### Personalized Questions from Resume:")
            st.write(response_resume.text)

        if position:
            role_prompt = f"""
            Based on the position {position} that the candidate, {name}, is applying for, generate 5-7 interview questions.
            These questions should test the candidate's understanding of the core responsibilities and skills required for the {position} role.
            """
            response_role = model.generate_content(role_prompt)

            st.write(f"### Interview Questions for the Position: {position}")
            st.write(response_role.text)

    st.subheader("Chat with TalentScout Assistant")
    chat_input = st.text_input("Your Message")

    if chat_input:
        sensitive_keywords = ["salary", "compensation", "benefits", "holiday", "leave", "pay", "bonus"]

        if any(word in chat_input.lower() for word in sensitive_keywords):
            response = f"""
            I appreciate you bringing that up, {name}! 😊
            However, compensation, benefits, and related details are typically discussed after an offer is extended. 
            If you’d like more insights, feel free to connect with HR directly. 
            For now, let’s focus on preparing you for the technical rounds. I believe your {qualification} from {college_name} will definitely stand out!
            """
        else:
            prompt = f"""
            You are a helpful recruitment assistant. Respond to the following user input: {chat_input}.
            Use candidate details like name ({name}), location ({location}), qualification ({qualification}),
            and college ({college_name}) naturally during the response.
            """
            response = model.generate_content(prompt).text

        st.session_state.chat_history.insert(0, (chat_input, response))

        for chat, reply in st.session_state.chat_history:
            st.write(f"You: {chat}")
            st.write(f"Assistant: {reply}")

    st.write("---")
    st.write("Type 'exit' to end the conversation.")
    if chat_input.lower() == "exit":
        st.write(f"Dhanyavaad {name}! 🙏 Thank you for using TalentScout. We wish you the best in your job search!")
        st.stop()
