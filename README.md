# TalentScout Hiring Assistant - ReadMe

## Introduction
TalentScout is an interview assistant application that was developed using Streamlit together with Google’s Generative AI. It is used for automatically specifying personalized interview questions and serves as a chatbot. The application is convenient as users can upload resumes in the PDF or DOCX format, provide candidate details, and have a conversation with the assistants who use and generate personalized technical role-based questions relying on resumes and the other details provided while also being able to upload the resume straight in the app.

## Functionalities

### Multi Language Support
The application supports several languages apart from English, including the following:
- Hindi
- Spanish
- French
- German

### Resume Upload and Extraction
Users are allowed to upload their resumes in both the PDF and DOCX formats, both of which the app is compatible with, in order to extract and generate other relevant details.

### Chat Interface
A conversational interface provides room to communicate with the TalentScout specific Assistant and engages in conversation regarding the users’ job application.

### Personalized Question Generation
With everything from the resume to what position the user would like to get, the app generates role-based questions in accordance with the given details.

### Sensitive Information Handling
In cases where questions with regard to salary, compensation, and others are asked, the assistant interacts with caution and care.

### Role-Specific Question Generation
Personalized questions are also generated based on the candidate's desired job position.

## Dependencies
The application requires the following Python libraries:
- `streamlit`: For building the web interface.
- `google-generativeai`: For interacting with Google's generative AI models.
- `pdfplumber`: For extracting text from PDF files.
- `python-docx`: For extracting text from Word (DOCX) files.
- `dotenv`: For managing environment variables.
- `os`: For interacting with the operating system (e.g., reading environment variables).

## Setup Instructions

### Prerequisites
- Python 3.7+
- A Google API Key for accessing the Google Generative AI model.

### Steps to Set Up the Application:
1. Clone or download the project folder.
2. Install the required dependencies by running the following:
   ```bash
   pip install -r requirements.txt
3. Set up the .env file in the project root with the following variable:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
4. Run the application using Streamlit
5. ```bash
   streamlit run app.py

## Application Flow and Logic

### Language Selection
- The user can choose the preferred language from the sidebar.
- The application maps the selected language to corresponding language codes (e.g., "en" for English, "hi" for Hindi).
- Language-specific UI text is loaded dynamically based on the selection.

### Candidate Details Form
The sidebar contains a form where the following candidate details can be input:
- Full Name
- Email Address
- Phone Number
- Years of Experience
- Desired Position
- Current Location
- Highest Qualification
- College/University Name
- Tech Stack

When the form is submitted, the candidate's details are stored in `session_state` for future interactions.

### Personalized Greeting
Upon submitting the form, the app provides a personalized greeting, addressing the user by name and acknowledging their qualification, location, and college/university. It also displays the extracted resume text (if available).

### Technical Question Generation
Based on the tech stack input by the user, the app generates 3-5 technical questions related to each technology listed. These questions are displayed on the main page.

### Resume-Based Personalized Question Generation
If a resume has been uploaded and text has been extracted, the app generates personalized questions based on the resume content. These questions explore the candidate's experience with projects, skills, and work history.

### Role-Specific Question Generation
If the user has specified a desired position, the app generates 5-7 interview questions tailored to that position.

### Chat Interface
The user can interact with the TalentScout Assistant using a simple text input. If the input contains any sensitive keywords (e.g., "salary", "compensation", "benefits"), the assistant responds with a predefined message. Otherwise, the assistant generates a response based on the user's input, considering candidate details such as name, location, qualification, and college.

### Chat History
The user's chat history is stored in `session_state` and displayed during the chat. This ensures that the user can review past interactions.

### End Conversation
The user can type 'exit' to end the conversation, at which point the assistant thanks the user for using the service.

## Code Details

### Environment Variables
The application requires an API key for the Google Generative AI model. This key should be placed in a `.env` file.

### Multi-Language Support
The app uses a dictionary (`ui_texts`) that contains translations of UI text for each supported language. The selected language code (`selected_language_code`) is used to fetch the appropriate translation.

### Extracting Resume Text
The `extract_resume_text` function handles the logic of extracting text from either PDF or DOCX files. The method uses `pdfplumber` for PDFs and `python-docx` for DOCX files, writing the content to a temporary file for processing.

### Generating Responses
The `generate_response_in_language` function constructs prompts for the generative AI model, incorporating language-specific instructions to ensure that the response is generated in the correct language.

### Session State
The `session_state` is used to track variables such as the selected language, user details, chat history, and whether the user has been greeted. This ensures that the state is preserved across different interactions within the session.

### Chat History
The chat history is stored and displayed in reverse order, showing the most recent question at the top. This allows users to review previous questions and answers during their conversation with the assistant.

## Conclusion
TalentScout Hiring Assistant is a powerful tool for recruiters and job candidates, providing personalized interview questions, a chat interface, and resume analysis in multiple languages. This application simplifies the hiring process by leveraging the capabilities of Google’s generative AI and enhancing the candidate experience through automated interactions.
