import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2
from io import BytesIO
from utils.prompts import get_prompt

# --- Configuration ---
load_dotenv()

# Initialize Gemini (with fallbacks)
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Try multiple model versions
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
    except:
        model = genai.GenerativeModel("gemini-1.0-pro")  # Fallback to stable version
        
except Exception as e:
    st.error(f" Gemini initialization failed: {str(e)}")
    st.stop()

# --- PDF Processing ---
def extract_text_from_pdf(uploaded_file):
    """Extracts text from PDF with robust error handling"""
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  # Skip empty pages
                text += f"{page_text}\n"
        return text.strip()
    except PyPDF2.PdfReadError:
        st.error("Invalid PDF file - please upload a readable PDF")
        return ""
    except Exception as e:
        st.error(f"PDF processing error: {str(e)}")
        return ""

# --- Streamlit UI ---
st.set_page_config(
    page_title="AI Interview Coach", 
    page_icon="💼",
    layout="wide"
)

# Sidebar for settings
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input(
        "Gemini API Key", 
        type="password",
        value=os.getenv("GEMINI_API_KEY", "")
    )
    if api_key:
        genai.configure(api_key=api_key)

# Main interface
st.title("💼 AI Interview Answer Generator")
st.caption("Upload your resume (PDF or text) and job description")

# Input columns
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    resume_text = st.text_area("Or paste resume text", height=200)

with col2:
    job_desc = st.text_area("Paste Job Description", height=200, placeholder="Paste the full job description here...")

# Question selection
question = st.selectbox(
    "Select interview question",
    options=[
        "Tell me about yourself",
        "Why should we hire you?",
        "What are your strengths?",
        "Describe a challenge you overcame",
        "Custom question"
    ],
    index=0
)

custom_question = st.text_input("Your custom question") if question == "Custom question" else ""

# Generation button
if st.button("Generate Answer", type="primary"):
    # Validate inputs
    if not (resume_text.strip() or uploaded_file):
        st.error("Please provide your resume")
        st.stop()
    
    if not job_desc.strip():
        st.error("Please provide the job description")
        st.stop()

    # Process PDF if uploaded
    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text.strip():
                st.error("No readable text found in PDF")
                st.stop()

    # Get final question
    final_question = custom_question if question == "Custom question" else question

    # Generate answer
    try:
        with st.spinner("Generating tailored answer..."):
            prompt = get_prompt(final_question, resume_text, job_desc)
            response = model.generate_content(prompt)
            
            # Display results
            st.success("🎯 Tailored Answer")
            st.write(response.text)
            
            # Add download option
            st.download_button(
                "Download Answer",
                data=response.text,
                file_name=f"interview_answer.txt",
                mime="text/plain"
            )
            
    except genai.types.BlockedPromptException:
        st.error("Content blocked by safety filters - try rephrasing")
    except Exception as e:
        st.error(f"Generation failed: {str(e)}")

# Footer with tips
st.divider()
st.caption("💡 Tip: For best results, include specific metrics (e.g. 'increased sales by 20%') in your resume")