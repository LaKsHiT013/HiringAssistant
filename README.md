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
```
