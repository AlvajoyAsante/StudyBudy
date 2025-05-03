# 📚 StudyBudy

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  ![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

An AI-powered educational assistant that helps students by:

- 📖 Summarizing lecture transcripts  
- 🎯 Extracting key concepts and definitions  
- 📝 Generating quiz questions  
- ❓ Answering questions based on lecture content  

Built with a FastAPI backend, Streamlit frontend, and powered by Groq LLMs!

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/AlvajoyAsante/StudyBudy.git
cd StudyBudy
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Frontend (Streamlit)

```bash
streamlit run app.py
```

The app will open automatically at: http://localhost:8000

### ⚙️ Technologies Used

- 🛠 Python  
- ⚡ FastAPI (Backend API)  
- 🎨 Streamlit (Frontend UI)  
- 🧠 Groq API (LLM Engine)  
- 🔥 OpenAI Python SDK (Connected to Groq)  

### 📂 Project Structure

```plaintext
StudyBudy/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
```

### 💡 Future Improvements

- Allow users to upload lecture audio/video and auto-transcribe  
- Save user transcripts and question history in a database  
- Add login and user authentication system  
- Enhance the UI with custom themes and better styling  

### ✨ Demo 
https://my-ai-study-buddy.streamlit.app/