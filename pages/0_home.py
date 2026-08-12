import streamlit as st
import base64
import os

st.set_page_config(page_title="ORBIT-I | Home", page_icon="🚀", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "assets", "style.css"), encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid="stSidebarNav"] ul li:first-child {display: none;}
        [data-testid="stSidebarNav"]::before {
            content: "ORBIT-I";
            display: block;
            font-size: 20px;
            font-weight: 700;
            color: var(--lb-primary, #1a73e8);
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

with open(os.path.join(BASE_DIR, "assets", "logo.png"), "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()

# ── Title ──
st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 0px;">
        <img src="data:image/png;base64,{logo_data}" width="45">
        <div>
            <h1 style="margin: 0; padding: 0; line-height:1.1;">ORBIT-I</h1>
            <p style="margin:0; color: var(--lb-text-muted); font-size: 14px;">CV Intelligence &amp; Offer Automation Platform</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.divider()

# ── Stat cards ──
st.markdown(f"""
    <div class="stat-card-row">
        <div class="stat-card">
            <div class="stat-icon-circle">📄</div>
            <div>
                <div class="stat-label">Total CVs Uploaded</div>
                <div class="stat-value">{st.session_state.total_uploaded}</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon-circle success">✅</div>
            <div>
                <div class="stat-label">Processed</div>
                <div class="stat-value">{st.session_state.processed}</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon-circle warning">⏳</div>
            <div>
                <div class="stat-label">Pending</div>
                <div class="stat-value">{st.session_state.pending}</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Welcome / upload card ──
with st.container(border=True):
    st.markdown("### Welcome to ORBIT-I")
    st.markdown(
        "<p style='color: var(--lb-text-muted); margin-top:-8px;'>Upload CVs and generate offer letters automatically.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="orbit-dropzone-label">
            <div class="orbit-dropzone-icon">☁️⬆️</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        if st.button("Upload CV", use_container_width=True, type="primary"):
            st.switch_page("pages/upload.py")

    st.markdown(
        "<p style='text-align:center; color: var(--lb-text-muted); font-size:12px; margin-top:6px;'>"
        "Supports PDF, DOCX, TXT &nbsp;|&nbsp; Max file size 20MB</p>",
        unsafe_allow_html=True,
    )
