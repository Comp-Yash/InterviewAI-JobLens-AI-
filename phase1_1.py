import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pygame
import google.generativeai as genai
import fitz
import os
import tempfile
import time
from io import BytesIO

# Configure Gemini AI
genai.configure(api_key="AIzaSyBNDP4ixG27c9zblIBYeXzajhXV5vu1_mk")
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize pygame mixer
pygame.mixer.init()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'recorded_answer' not in st.session_state:
    st.session_state.recorded_answer = ""

def extract_resume_info(pdf_path):
    """Extract text from PDF resume"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting resume: {str(e)}"

def text_to_speech(text):
    """Convert text to speech and play it"""
    try:
        tts = gTTS(text=text, lang='en')
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(audio_buffer.read())
            tmp_file_path = tmp_file.name
        
        pygame.mixer.music.load(tmp_file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        try:
            pygame.mixer.music.unload()
            time.sleep(0.1)
            os.unlink(tmp_file_path)
        except:
            pass
    except Exception as e:
        pass

def record_audio():
    """Record audio when button is clicked"""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 8.0  # Wait 8 seconds of silence before stopping
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Recording started... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Record audio - will stop after 8 seconds of silence or 2 minutes max
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=120)
        
        st.info("🔄 Processing your answer...")
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def generate_question(name, title, job_description, resume_info, level, previous_questions, question_num):
    """Generate interview question using Gemini AI"""
    
    previous_q_text = ""
    if previous_questions:
        for i, q in enumerate(previous_questions):
            previous_q_text += f"Q{i+1}) {q}\n"
    
    prompt = f"""You are a professional interviewer.

Candidate name: {name}
Job title: {title}
Job description: {job_description}
Resume info: {resume_info}
Previous questions: {previous_q_text}
Question level: {level}

Generate one clear interview question related to the job description.
Only return the question text, nothing else. Note using gTTS so construct quetion such that it is easy to read and dont break flow of the question.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating question: {str(e)}"

# PAGE 1: User Input
def page_1():
    st.title("🎯 AI Interview Assistant")
    st.subheader("Please provide your details to start the interview")
    
    with st.form("interview_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            candidate_name = st.text_input("👤 Candidate Name", placeholder="Enter your full name")
            job_title = st.text_input("💼 Job Title", placeholder="e.g., Software Engineer")
            level = st.selectbox("📊 Experience Level", 
                               ["Entry Level", "Mid Level", "Senior Level", "Lead/Principal"])
        
        with col2:
            uploaded_file = st.file_uploader("📄 Upload Resume", type=['pdf'])
        
        job_description = st.text_area("📋 Job Description & Required Skills", 
                                     placeholder="Describe the job role, responsibilities, and required skills...",
                                     height=150)
        
        submit_button = st.form_submit_button("🚀 Start Interview", use_container_width=True)
        
        if submit_button:
            if not all([candidate_name, job_title, level, job_description, uploaded_file]):
                st.error("❌ Please fill all fields and upload your resume!")
                return
            
            # Save form data to session state
            st.session_state.candidate_name = candidate_name
            st.session_state.job_title = job_title
            st.session_state.level = level
            st.session_state.job_description = job_description
            
            # Process resume
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            resume_info = extract_resume_info(tmp_file_path)
            st.session_state.resume_info = resume_info
            os.unlink(tmp_file_path)
            
            # Generate first question
            first_question = generate_question(
                candidate_name, job_title, job_description, 
                resume_info, level, [], 1
            )
            st.session_state.questions = [first_question]
            st.session_state.current_question_index = 0
            
            st.session_state.page = 2
            st.rerun()
            
    st.subheader("Please Note")
    st.write("1. The interview will be conducted in a single session.")
    st.write("2. The interview will be conducted in English.")
    st.write("3. Answer Autoplayed after 3 seconds.")
    st.write("4. To sumbit Answer just be silent for 8 seconds")
    st.write("5. Can repeat the question by clicking on the repeat button.")
    st.write("6. If any issue occurs during recording, please click the 'Record' button again and restart your answer from the beginning.")
    st.write("7. Can write NA at job description if you want to skip.")
    
    



# PAGE 2: Interview Process
def page_2():
    # Header
    st.markdown(f"""
    <div style="background-color: #1e3a8a; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2>🎤 Interview in Progress</h2>
        <p><strong>👤 Candidate:</strong> {st.session_state.candidate_name}</p>
        <p><strong>💼 Role:</strong> {st.session_state.job_title}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    progress = (st.session_state.current_question_index + 1) / 10
    st.progress(progress)
    st.write(f"Question {st.session_state.current_question_index + 1} of 10")
    
    # Current question
    if st.session_state.current_question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.current_question_index]
        
        st.markdown("### 📝 Question:")
        st.markdown(f"**{current_question}**")
        
        # Auto-play question
        if f'played_q_{st.session_state.current_question_index}' not in st.session_state:
            text_to_speech(current_question)
            st.session_state[f'played_q_{st.session_state.current_question_index}'] = True
        
        st.markdown("---")
        
        # Buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🎤 Record Answer", use_container_width=True):
                # Start recording immediately when button is clicked
                answer = record_audio()
                
                if answer:
                    st.session_state.answers.append(answer)
                    st.success(f"✅ Answer recorded: {answer[:100]}...")
                    
                    # Move to next question or finish
                    if st.session_state.current_question_index < 9:
                        # Generate next question
                        next_question = generate_question(
                            st.session_state.candidate_name,
                            st.session_state.job_title,
                            st.session_state.job_description,
                            st.session_state.resume_info,
                            st.session_state.level,
                            st.session_state.questions,
                            st.session_state.current_question_index + 2
                        )
                        st.session_state.questions.append(next_question)
                        st.session_state.current_question_index += 1
                        st.rerun()
                    else:
                        # Interview complete
                        st.session_state.page = 3
                        st.rerun()
                else:
                    st.warning("⚠️ No audio detected. Please try again.")
        
        with col2:
            if st.button("🔁 Repeat Question", use_container_width=True):
                text_to_speech(current_question)
                st.info("🔊 Question repeated!")
        
        with col3:
            st.write("")  # Empty space

# PAGE 3: Results
def page_3():
    st.title("🎉 Interview Completed!")
    st.success(f"Congratulations {st.session_state.candidate_name}! You have successfully completed the interview.")
    
    # Display all Q&A
    st.subheader("📋 Interview Summary")
    
    qa_content = f"Interview Summary for {st.session_state.candidate_name}\n"
    qa_content += f"Job Title: {st.session_state.job_title}\n"
    qa_content += f"Level: {st.session_state.level}\n"
    qa_content += f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
        st.markdown(f"**Question {i+1}:** {question}")
        st.markdown(f"**Answer:** {answer}")
        st.markdown("---")
        
        qa_content += f"Question {i+1}: {question}\n"
        qa_content += f"Answer: {answer}\n\n"
    
    # Download button
    st.download_button(
        label="📥 Download Interview Summary",
        data=qa_content,
        file_name=f"interview_summary_{st.session_state.candidate_name}_{time.strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    # Restart button
    if st.button("🔄 Start New Interview", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = 1
        st.rerun()

# Main App
def main():
    st.set_page_config(
        page_title="AI Interview Assistant", 
        page_icon="🎯",
        layout="wide"
    )
    
    if st.session_state.page == 1:
        page_1()
    elif st.session_state.page == 2:
        page_2()
    elif st.session_state.page == 3:
        page_3()

if __name__ == "__main__":
    main()
