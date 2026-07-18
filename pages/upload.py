import streamlit as st
import base64
import time
import sys
import os
import pdfplumber
import docx

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from classifier.domain_classifier import classify_resume

st.set_page_config(page_title="ORBIT-I | Upload", page_icon="📂", layout="wide")

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li:first-child {display: none;}
        [data-testid="stSidebarNav"]::before {
            content: "ORBIT-I";
            display: block;
            font-size: 20px;
            font-weight: 700;
            color: #1a73e8;
            padding: 24px 16px 16px 16px;
            letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)

if "total_uploaded" not in st.session_state:
    st.session_state.total_uploaded = 0

if "pending" not in st.session_state:
    st.session_state.pending = 0

if "processed" not in st.session_state:
    st.session_state.processed = 0

if "last_uploaded" not in st.session_state:
    st.session_state.last_uploaded = None

st.title("📂 Upload Resume")
st.write("Upload your resume in PDF or DOCX format")

st.divider()

uploaded_file = st.file_uploader("Select your CV", type=["pdf", "docx"])

if uploaded_file is not None:

    if st.session_state.last_uploaded != uploaded_file.name:
        st.session_state.last_uploaded = uploaded_file.name
        st.session_state.total_uploaded += 1
        st.session_state.pending += 1

    with st.spinner("Processing your CV, please wait..."):

        # Step 1: Text extract karo
        extracted_text = ""

        if uploaded_file.name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            for cell in row:
                                if cell:
                                    extracted_text += cell + " "

        elif uploaded_file.name.endswith(".docx"):
            document = docx.Document(uploaded_file)
            for paragraph in document.paragraphs:
                extracted_text += paragraph.text + "\n"
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        extracted_text += cell.text + "\n"

        # Step 2: Classifier chalao
        if extracted_text.strip():
            result = classify_resume(extracted_text)

            if st.session_state.get("last_processed") != uploaded_file.name:
                st.session_state.last_processed = uploaded_file.name
                st.session_state.processed += 1
                if st.session_state.pending > 0:
                    st.session_state.pending -= 1

        time.sleep(1)

    st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

    st.divider()

    # Step 3: Result dikhao
    if extracted_text.strip() and 'result' in locals():
        st.subheader("🎯 Classification Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Domain", result.get("domain", "Unknown"))

        with col2:
            score = result.get("confidence_score", 0)
            st.metric("Confidence Score", f"{score}%")

        with col3:
            status = result.get("status", "Unknown")
            if status == "Manual Review":
                st.metric("Status", "⚠️ Manual Review")
            else:
                st.metric("Status", "✅ Auto Classified")

        if status == "Manual Review":
            st.warning("⚠️ Confidence score is below 75%. This CV has been flagged for manual review.")

    st.divider()

    if st.button("🏠 Back to Home"):
        st.switch_page("pages/home.py")
