import streamlit as st
import requests
from io import BytesIO
from fpdf import FPDF
import fitz  # PyMuPDF for reading PDFs

# --- Helper Function to Generate PDF for Download ---
def generate_pdf(text, title="StudyBudy Output"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, title + "\n\n" + text)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return BytesIO(pdf_output)

# --- Base URL for Backend ---
API_BASE_URL = "http://localhost:8000"

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="StudyBudy - Educational Assistant", layout="wide")

# --- Sidebar Theme Switcher ---
theme_option = st.sidebar.selectbox(
    "Choose App Theme",
    ["Light Mode", "Dark Mode"],
    index=0  # Default to Light Mode
)

# --- Apply Theme Based on Selection ---
if theme_option == "Light Mode":
    primaryColor = "#1976D2"
    backgroundColor = "#FAFAFA"
    secondaryBackgroundColor = "#BEBEBE"
    textColor = "#212121"
elif theme_option == "Dark Mode":
    primaryColor = "#BB86FC"
    backgroundColor = "#121212"
    secondaryBackgroundColor = "#1F1F1F"
    textColor = "#FFFFFF"

# --- Custom Dynamic Styling ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {backgroundColor};
        color: {textColor};
    }}
    section[data-testid="stSidebar"] > div:first-child {{
        background-color: {secondaryBackgroundColor};
    }}
    textarea, input {{
        background-color: {backgroundColor} !important;
        color: {textColor} !important;
    }}
    textarea {{
        border: 1px solid {primaryColor};
        border-radius: 0.5rem;
        padding: 10px;
    }}
    button[kind="primary"] {{
        background-color: {primaryColor};
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {primaryColor};
    }}
    label, .stSelectbox label {{
        color: {textColor};
    }}
    </style>
""", unsafe_allow_html=True)

# --- Page Title ---
st.markdown(f"<h1 style='text-align: center; color: {primaryColor};'>📚 StudyBudy: Your AI-Powered Lecture Companion</h1>", unsafe_allow_html=True)

# --- Sidebar Upload and Action Options ---
st.sidebar.title("Upload & Interact")
uploaded_pdf = st.sidebar.file_uploader("Upload Lecture/Transcript PDF", type=["pdf"])

# --- Extract Text from Uploaded PDF (if any) ---
pdf_text = ""
if uploaded_pdf is not None:
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    for page in doc:
        pdf_text += page.get_text()

# --- Main Interaction: Text Area (prefilled with PDF text if uploaded) ---
transcript_text = st.text_area(
    "Paste Lecture Transcript (or upload a PDF)", 
    value=pdf_text,
    height=300
)

# --- Sidebar Action Choices ---
option = st.sidebar.selectbox("Choose Action", [
    "Summarize Lecture",
    "Extract Key Concepts",
    "Generate Quiz",
    "Ask a Question",
])

# --- Action Buttons and API Calls ---
if option != "Ask a Question":
    if st.button("Run"):
        if not transcript_text.strip():
            st.error("Please paste a lecture transcript or upload a PDF.")
        else:
            endpoint_map = {
                "Summarize Lecture": "/summarize",
                "Extract Key Concepts": "/key_concepts",
                "Generate Quiz": "/generate_quiz"
            }
            endpoint = endpoint_map[option]
            response = requests.post(API_BASE_URL + endpoint, json={"content": transcript_text})
            if response.status_code == 200:
                result = list(response.json().values())[0]
                st.text_area(f"{option} Output", result, height=300)
                
                # --- PDF Download Button ---
                pdf_file = generate_pdf(result, title=f"{option} Output")
                st.download_button(
                    label="📄 Download Output as PDF",
                    data=pdf_file,
                    file_name="studybudy_output.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("API Error: " + response.text)
else:
    question_text = st.text_input("Ask a question about the lecture")
    if st.button("Get Answer"):
        if not transcript_text.strip() or not question_text.strip():
            st.error("Please provide both transcript and question.")
        else:
            response = requests.post(API_BASE_URL + "/ask", json={
                "question": question_text,
                "transcript": transcript_text
            })
            if response.status_code == 200:
                answer = response.json()['answer']
                st.success("Answer:")
                st.write(answer)
                
                # --- PDF Download for Answer ---
                pdf_file = generate_pdf(answer, title="Answer Output")
                st.download_button(
                    label="📄 Download Answer as PDF",
                    data=pdf_file,
                    file_name="studybudy_answer.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("API Error: " + response.text)
