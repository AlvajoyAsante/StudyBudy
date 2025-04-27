import streamlit as st
import requests

# Set the base URL for the FastAPI backend
API_BASE_URL = "http://localhost:8000"

# Streamlit configuration
st.set_page_config(page_title="StudyBudy - Educational Assistant", layout="wide")

# --- Sidebar Theme Switcher ---
theme_option = st.sidebar.selectbox(
    "Choose App Theme",
    ["Light Mode", "Dark Mode"],
    index=0  # Default to Corporate
)

# --- Apply Theme Based on Choice ---
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

# --- Dynamic CSS Styling ---
# --- Custom Dynamic Styling ---
st.markdown(f"""
    <style>
    /* Entire App Background */
    .stApp {{
        background-color: {backgroundColor};
        color: {textColor};
    }}

    /* Sidebar background */
    section[data-testid="stSidebar"] > div:first-child {{
        background-color: {secondaryBackgroundColor};
    }}

    /* Text input and text area background */
    textarea, input {{
        background-color: {backgroundColor} !important;
        color: {textColor} !important;
    }}

    /* Text area border and padding */
    textarea {{
        border: 1px solid {primaryColor};
        border-radius: 0.5rem;
        padding: 10px;
    }}

    /* Button styling */
    button[kind="primary"] {{
        background-color: {primaryColor};
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }}

    /* Heading colors */
    h1, h2, h3, h4, h5, h6 {{
        color: {primaryColor};
    }}

    /* Label Text (Choose App Theme, etc.) */
    label, .stSelectbox label {{
        color: {textColor};
    }}
    </style>
""", unsafe_allow_html=True)


# --- Page Title ---
st.markdown(f"<h1 style='text-align: center; color: {primaryColor};'>📚 StudyBudy: Your AI-Powered Lecture Companion</h1>", unsafe_allow_html=True)

# --- Sidebar Options ---
st.sidebar.title("Upload & Interact")
option = st.sidebar.selectbox("Choose Action", [
    "Summarize Lecture",
    "Extract Key Concepts",
    "Generate Quiz",
    "Ask a Question",
])

# --- Main Interaction ---
transcript_text = st.text_area("Paste Lecture Transcript", height=300)

if option != "Ask a Question":
    if st.button("Run"):
        if not transcript_text.strip():
            st.error("Please paste a lecture transcript.")
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
            else:
                st.error("API Error: " + response.text)
