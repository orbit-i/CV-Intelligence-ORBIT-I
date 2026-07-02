import streamlit as st
import base64
import time

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
        time.sleep(2)

    st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

    st.divider()

    if st.button("🏠 Back to Home"):
        st.switch_page("pages/home.py")