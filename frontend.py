import streamlit as st
import requests

# Set the base URL for the FastAPI backend
API_BASE_URL = "http://localhost:8000"

# Streamlit configuration
st.set_page_config(page_title="Edu Assistant Agent", layout="wide")
st.title("📚 Educational Assistant Agent")

st.sidebar.title("Upload & Interact")
option = st.sidebar.selectbox("Choose Action", [
    "Summarize Lecture",
    "Extract Key Concepts",
    "Generate Quiz",
    "Ask a Question"
])

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

