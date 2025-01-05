import streamlit as st
import google.generativeai as genai
import pdfplumber  # For extracting text from PDFs
import docx  # For extracting text from Word documents
import tempfile
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API Key not found. Please set the GOOGLE_API_KEY in your .env file.")
else:
    # Configure the generative model with API key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('models/gemini-1.0-pro')

    # Language Dictionaries for UI text
    ui_texts = {
        'en': {
            "title": "TalentScout Hiring Assistant",
            "sidebar_title": "Candidate Details",
            "upload_title": "Upload Resume (PDF/DOCX)",
            "greeting": "Welcome to TalentScout! How’s everything going in",
            "resume_extracted": "Resume Extracted Successfully!",
            "personalized_questions": "Personalized Questions from Resume:",
            "interview_questions": "Interview Questions for the Position",
            "chat_with": "Chat with TalentScout Assistant",
            "exit_message": "Type 'exit' to end the conversation.",
            "thank_you": "Thank you for using TalentScout. We wish you the best in your job search!"
        },
        'hi': {
            "title": "TalentScout हायरिंग असिस्टेंट",
            "sidebar_title": "उम्मीदवार विवरण",
            "upload_title": "रिज़्यूमे अपलोड करें (PDF/DOCX)",
            "greeting": "TalentScout में आपका स्वागत है! **{location}** में सब कुछ कैसे चल रहा है?",
            "resume_extracted": "रिज़्यूमे सफलतापूर्वक निकाला गया!",
            "personalized_questions": "रिज़्यूमे से व्यक्तिगत प्रश्न:",
            "interview_questions": "पद के लिए साक्षात्कार प्रश्न",
            "chat_with": "TalentScout सहायक से चैट करें",
            "exit_message": "चर्चा समाप्त करने के लिए 'exit' टाइप करें।",
            "thank_you": "TalentScout का उपयोग करने के लिए धन्यवाद। हम आपकी नौकरी खोज में शुभकामनाएं देते हैं!"
        },
        'es': {
            "title": "Asistente de Contratación TalentScout",
            "sidebar_title": "Detalles del Candidato",
            "upload_title": "Subir Currículum (PDF/DOCX)",
            "greeting": "¡Bienvenido a TalentScout! ¿Cómo va todo en **{location}**?",
            "resume_extracted": "¡Currículum extraído con éxito!",
            "personalized_questions": "Preguntas personalizadas del currículum:",
            "interview_questions": "Preguntas para la posición",
            "chat_with": "Chatea con el Asistente TalentScout",
            "exit_message": "Escribe 'exit' para terminar la conversación.",
            "thank_you": "¡Gracias por usar TalentScout! Te deseamos lo mejor en tu búsqueda de trabajo."
        },
        'fr': {
            "title": "Assistant de recrutement TalentScout",
            "sidebar_title": "Détails du candidat",
            "upload_title": "Télécharger le CV (PDF/DOCX)",
            "greeting": "Bienvenue sur TalentScout! Comment ça va à **{location}**?",
            "resume_extracted": "CV extrait avec succès!",
            "personalized_questions": "Questions personnalisées à partir du CV :",
            "interview_questions": "Questions pour le poste",
            "chat_with": "Discutez avec l'assistant TalentScout",
            "exit_message": "Tapez 'exit' pour terminer la conversation.",
            "thank_you": "Merci d'avoir utilisé TalentScout. Nous vous souhaitons bonne chance dans votre recherche d'emploi."
        },
        'de': {
            "title": "TalentScout Einstellungsassistent",
            "sidebar_title": "Kandidaten Details",
            "upload_title": "Lebenslauf hochladen (PDF/DOCX)",
            "greeting": "Willkommen bei TalentScout! Wie läuft es in **{location}**?",
            "resume_extracted": "Lebenslauf erfolgreich extrahiert!",
            "personalized_questions": "Personalisierte Fragen aus dem Lebenslauf:",
            "interview_questions": "Fragen für die Position",
            "chat_with": "Chatten Sie mit dem TalentScout Assistenten",
            "exit_message": "Geben Sie 'exit' ein, um das Gespräch zu beenden.",
            "thank_you": "Danke, dass Sie TalentScout verwenden. Wir wünschen Ihnen viel Erfolg bei Ihrer Jobsuche."
        }
    }

    # Initialize Streamlit app
    selected_language = st.sidebar.selectbox("Select Language", options=["English", "Hindi", "Spanish", "French", "German"])

    # Mapping language selection to the dictionary keys
    language_map = {"English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr", "German": "de"}
    selected_language_code = language_map[selected_language]

    # Store the language code in session_state to keep track of it
    if 'selected_language_code' not in st.session_state:
        st.session_state.selected_language_code = selected_language_code
    elif st.session_state.selected_language_code != selected_language_code:
        st.session_state.selected_language_code = selected_language_code
        # When language changes, we reset 'greeted' to False so it re-triggers greeting logic
        st.session_state.greeted = False

    # Title and sidebar content update based on the selected language
    st.title(ui_texts[st.session_state.selected_language_code]["title"])
    st.sidebar.title(ui_texts[st.session_state.selected_language_code]["sidebar_title"])

    # Resume Upload and Processing
    st.sidebar.subheader(ui_texts[st.session_state.selected_language_code]["upload_title"])
    uploaded_file = st.sidebar.file_uploader("Choose your resume", type=['pdf', 'docx'])

    # Extract text from the uploaded resume
    def extract_resume_text(uploaded_file):
        text = ""
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name

                # Extract text based on file type
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

    # Sidebar form to gather candidate information
    with st.sidebar.form("candidate_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")

        qualification = st.selectbox("Highest Qualification", ["Select", "Diploma", "Bachelor's Degree", "Master's Degree", "PhD"])
        college_name = st.text_input("College/University Name")
        tech_stack = st.text_area("Tech Stack (e.g., Python, Django, MySQL)")
        submit = st.form_submit_button("Submit")

    # Generate responses in selected language
    def generate_response_in_language(prompt, language_code):
        language_name = {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }.get(language_code, 'English')  # Default to English if not found
        language_instruction = f"Please provide your response in {language_name}."
        return model.generate_content(language_instruction + " " + prompt).text

    # Personalized Greeting and Intro
    if submit and not st.session_state.get("greeted", False):
        st.session_state.greeted = True
        st.write(f"**{name}! 👋**")
        st.write(f"{ui_texts[st.session_state.selected_language_code]['greeting']} **{location}**?")
        st.write(f"Your **{qualification}** from **{college_name}** sounds impressive! Let's get started. 😊")

        # Display resume text if available
        if resume_text:
            st.write(f"📄 **{ui_texts[st.session_state.selected_language_code]['resume_extracted']}**")
            st.write(resume_text[:300] + "...")  # Show preview of resume
        else:
            st.write("No resume uploaded or extracted. Proceeding with available details.")

        # Generate technical and personalized questions based on the resume and other information
        tech_stack_list = [tech.strip() for tech in tech_stack.split(',')]  # Split the stack into individual technologies

        # Generate Technical Questions from Tech Stack
        for tech in tech_stack_list:
            tech_prompt = f"Based on the candidate's experience and skills in {tech}, generate 3-5 technical questions."
            response_tech = generate_response_in_language(tech_prompt, st.session_state.selected_language_code)
            st.write(f"### Questions related to {tech}:")
            st.write(response_tech)

        # Generate Resume-Based Questions
        if resume_text:
            resume_prompt = f"Based on the resume of {name}, generate personalized questions that probe into the candidate's experience with projects, skills, and work history. Resume content: {resume_text}"
            response_resume = generate_response_in_language(resume_prompt, st.session_state.selected_language_code)
            st.write(f"### {ui_texts[st.session_state.selected_language_code]['personalized_questions']}")
            st.write(response_resume)

        # Add Role-Specific Question Generation
        if position:
            role_prompt = f"Based on the position {position} that the candidate, {name}, is applying for, generate 5-7 interview questions."
            response_role = generate_response_in_language(role_prompt, st.session_state.selected_language_code)

            st.write(f"### {ui_texts[st.session_state.selected_language_code]['interview_questions']} {position}")
            st.write(response_role)

    # Chatbot conversation logic
    st.subheader(ui_texts[st.session_state.selected_language_code]["chat_with"])
    chat_input = st.text_input("Your Message")

    if chat_input:
        sensitive_keywords = ["salary", "compensation", "benefits", "holiday", "leave", "pay", "bonus"]

        if any(word in chat_input.lower() for word in sensitive_keywords):
            response = f"I appreciate you bringing that up, {name}! 😊 However, compensation and related details are typically discussed after an offer is extended. If you’d like more insights, feel free to connect with HR directly."
        else:
            prompt = f"You are a helpful recruitment assistant. Respond to the following user input: {chat_input}. Use candidate details like name ({name}), location ({location}), qualification ({qualification}), and college ({college_name}) naturally during the response."
            response = generate_response_in_language(prompt, st.session_state.selected_language_code)

        # Prepend the new question and response to the chat history
        st.session_state.chat_history.insert(0, (chat_input, response))

        # Display full chat history (recent questions at the top)
        for chat, reply in st.session_state.chat_history:
            st.write(f"You: {chat}")
            st.write(f"Assistant: {reply}")

    # End conversation logic
    st.write("---")
    st.write(ui_texts[st.session_state.selected_language_code]["exit_message"])
    if chat_input.lower() == "exit":
        st.write(f"Dhanyavaad {name}! 🙏 {ui_texts[st.session_state.selected_language_code]['thank_you']}")
        st.stop()
