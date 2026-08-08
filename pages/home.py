import streamlit as st
import base64

st.set_page_config(page_title="ORBIT-I | Home", page_icon="🚀", layout="wide")

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

if "processed" not in st.session_state:
    st.session_state.processed = 0

if "pending" not in st.session_state:
    st.session_state.pending = 0

with open("assets/logo.png", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()

st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0px;">
        <img src="data:image/png;base64,{logo_data}" width="45">
        <h1 style="margin: 0; padding: 0;">ORBIT-I</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("CV Intelligence & Offer Automation Platform")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total CVs Uploaded", value=st.session_state.total_uploaded)

with col2:
    st.metric(label="Processed", value=st.session_state.processed)

with col3:
    st.metric(label="Pending", value=st.session_state.pending)

st.divider()

st.write("Welcome to ORBIT-I. Upload CVs and generate offer letters automatically.")

if st.button("📂 Upload CV"):
    st.switch_page("pages/upload.py")