import base64
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
from hr.validation import validate_email, validate_salary, validate_required

script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, os.pardir, "icon", "Screenshot 2026-07-20 140604.png")

logo_data = None
if os.path.exists(logo_path):
    with open(logo_path, "rb") as logo_file:
        logo_data = base64.b64encode(logo_file.read()).decode()

logo_html = ""
if logo_data:
    logo_html = f'<span class="orbit-icon"><img src="data:image/png;base64,{logo_data}" alt="ORBIT-I logo"></span>'
else:
    logo_html = '<span class="orbit-icon"></span>'

st.set_page_config(page_title="ORBIT-I | Manual Override", page_icon="✏️", layout="wide")

hero_html = """
    <style>
        :root {
            --orbit-bg: #051523;
            --orbit-card: rgba(255, 255, 255, 0.08);
            --orbit-border: rgba(255, 255, 255, 0.14);
            --orbit-accent: #ffc94d;
            --orbit-text: #e8edf4;
            --orbit-muted: #a8bcd4;
        }

        .stApp {
            background: radial-gradient(circle at top left, rgba(255, 201, 77, 0.12), transparent 24%),
                        radial-gradient(circle at bottom right, rgba(80, 180, 255, 0.14), transparent 20%),
                        linear-gradient(160deg, #081223 0%, #0b1f3f 40%, #071025 100%);
            color: var(--orbit-text);
            font-family: 'Inter', sans-serif;
        }

        .hero-banner {
            padding: 2rem 2rem 1.8rem;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.14);
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.18);
            overflow: hidden;
            position: relative;
            margin-bottom: 2rem;
        }

        .hero-banner::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, rgba(255, 201, 77, 0.18), rgba(78, 182, 255, 0.16));
            opacity: 0.28;
            filter: blur(30px);
            animation: glow 8s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from {{ transform: translate(-10px, -8px) scale(1); opacity: 0.22; }}
            to   {{ transform: translate(10px, 8px) scale(1.08); opacity: 0.34; }}
        }

        .hero-content {
            position: relative;
            z-index: 1;
        }

        .orbit-brand {
            display: inline-flex;
            align-items: center;
            gap: 0.85rem;
            padding: 0.7rem 1rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.08);
            color: #fff;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            font-weight: 700;
            font-size: 0.95rem;
            border: 1px solid rgba(255, 255, 255, 0.16);
        }

        .orbit-icon {
            width: 2.2rem;
            height: 2.2rem;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 999px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.18);
            background: rgba(0, 0, 0, 0.08);
        }

        .orbit-icon img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .hero-title {
            margin: 1.5rem 0 0.5rem;
            font-size: clamp(2.8rem, 3.6vw, 4.4rem);
            line-height: 0.95;
            letter-spacing: -0.05em;
            color: #ffffff;
            text-shadow: 0 18px 50px rgba(0, 0, 0, 0.18);
        }

        .hero-subtitle {
            max-width: 780px;
            margin: 0;
            color: var(--orbit-muted);
            font-size: 1.05rem;
            line-height: 1.8;
        }

        .section-card {
            background: var(--orbit-card);
            border: 1px solid var(--orbit-border);
            border-radius: 22px;
            padding: 1.5rem 1.6rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(20px);
        }

        button {
            font-weight: 700;
        }

        .stButton>button {{
            background: linear-gradient(135deg, #ffc94d, #4fb6ff) !important;
            color: #04111f !important;
            border: none;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
        }}

        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        input[type="text"],
        input[type="email"],
        input[type="tel"],
        textarea,
        .stDateInput>div>div>input,
        input:not([type="checkbox"]):not([type="radio"]) {{
            background: rgba(255,255,255,0.18) !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border: 1px solid rgba(255,255,255,0.36) !important;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.12) !important;
            caret-color: #000000 !important;
        }}

        .stTextInput>div>label,
        .stTextArea>div>label,
        label,
        .stDateInput>div>label {
            color: #f4f7ff !important;
            font-weight: 600;
        }

        .stTextInput>div>div>input::placeholder,
        .stTextArea>div>div>textarea::placeholder,
        input::placeholder,
        textarea::placeholder {{
            color: rgba(244, 247, 255, 0.65) !important;
            opacity: 1 !important;
        }}
    </style>

    <div class="hero-banner">
        <div class="hero-content">
            <div class="orbit-brand">
                {logo_html}
                ORBIT-I
            </div>
            <h1 class="hero-title">Manual Override Dashboard</h1>
            <p class="hero-subtitle">A professional HR review workspace to validate candidate information, refine offer details, and generate polished offer letters with ease.</p>
        </div>
    </div>
    """

hero_html = hero_html.replace("{logo_html}", logo_html)
st.markdown(hero_html, unsafe_allow_html=True)

st.divider()

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {
        "name": "",
        "email": "",
        "phone": "",
        "position": "",
        "salary": "",
        "joining_date": "",
        "domain": "",
        "remarks": ""
    }

if "preview_mode" not in st.session_state:
    st.session_state.preview_mode = False

if st.session_state.preview_mode:
    st.subheader(" Offer Letter Preview")

    data = st.session_state.candidate_data

    st.markdown(f"""
---
**Date:** {data.get('joining_date', '')}

**Dear {data.get('name', '')},**

We are pleased to offer you the position of **{data.get('position', '')}**
in the **{data.get('domain', '')}** department.

**Salary:** PKR {data.get('salary', '')} / month

**Joining Date:** {data.get('joining_date', '')}

**Email:** {data.get('email', '')}

**Phone:** {data.get('phone', '')}

**Remarks:** {data.get('remarks', '')}

---

Regards,

**HR Department**

ORBIT-I, karachi, Pakistan
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Edit Again"):
            st.session_state.preview_mode = False
            st.rerun()
    with col2:
        if st.button(" Confirm & Generate Offer"):
            st.success(" Offer letter confirmed and ready for generation!")

else:
    st.subheader(" Candidate Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name", value=st.session_state.candidate_data.get("name", ""))
        email = st.text_input("Email", value=st.session_state.candidate_data.get("email", ""))
        phone = st.text_input("Phone", value=st.session_state.candidate_data.get("phone", ""))
        domain = st.text_input("Domain", value=st.session_state.candidate_data.get("domain", ""))

    with col2:
        position = st.text_input("Position Title", value=st.session_state.candidate_data.get("position", ""))
        salary = st.text_input("Salary (numbers only)", value=st.session_state.candidate_data.get("salary", ""))
        joining_date = st.date_input(
            "Joining Date",
            value=(
                datetime.strptime(st.session_state.candidate_data.get("joining_date", ""), "%Y-%m-%d").date()
                if st.session_state.candidate_data.get("joining_date", "")
                else date.today()
            )
        )
        remarks = st.text_area("Remarks", value=st.session_state.candidate_data.get("remarks", ""))

    st.divider()

    if st.button(" Save & Preview"):
        errors = []

        if not validate_required(name):
            errors.append("Name is required")
        if not validate_required(position):
            errors.append("Position is required")
        if not joining_date:
            errors.append("Joining date is required")
        if not validate_email(email):
            errors.append("Invalid email address")
        if not validate_salary(salary):
            errors.append("Salary must contain numbers only")

        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            st.session_state.candidate_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "position": position,
                "salary": salary,
                "joining_date": joining_date.isoformat() if isinstance(joining_date, date) else str(joining_date),
                "domain": domain,
                "remarks": remarks
            }
            st.session_state.preview_mode = True
            st.rerun()