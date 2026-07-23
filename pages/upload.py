import sys
sys.path.insert(0, r"C:\Users\Admin\Desktop\orbit-I\orbit-I")  # TODO: remove/adjust for other machines/deployment

import streamlit as st
import time
import os
import re
import pdfplumber
import docx

from classifier.domain_classifier import classify_resume
from core.offer_generator import generate_offer
from services.audit_logger import log_event


def extract_candidate_name(text):
    """Extract candidate name from first few lines of CV text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    skip_words = ['resume', 'cv', 'curriculum', 'vitae', 'objective',
                  'summary', 'profile', 'contact', 'email', 'phone',
                  'address', 'linkedin', 'github', 'dear', 'sir', 'madam']

    for line in lines[:10]:
        if any(char in line for char in ['@', 'http', 'www', '+92', '0300', '/', '📧', '📞', '📍']):
            continue
        if any(word in line.lower() for word in skip_words):
            continue
        if len(line) > 50:
            continue
        if any(char in line for char in ['|', '•', '·', '─', '=', ':', ',']):
            continue
        words = line.split()
        if 2 <= len(words) <= 4:
            if all(word[0].isupper() for word in words if word.isalpha()):
                return line

    return "Candidate"


def get_position_title(domain):
    """
    Map a classifier domain to a human-readable job title.
    Extend this dict with ALL domain labels your classifier can actually output
    (check classifier/domain_classifier.py for the exact label strings).
    The fallback below no longer just returns the raw domain name, so
    domain and position won't look identical even for unmapped domains.
    """
    position_mapping = {
        "Engineering": "Engineer",
        "Science": "Scientist",
        "Design": "Designer",
        "Analysis": "Analyst",
        # 👉 add every other domain label your classifier returns here, e.g.:
        # "Marketing": "Marketing Specialist",
        # "Finance": "Financial Analyst",
        # "Sales": "Sales Executive",
        # "HR": "HR Executive",
        # "IT": "IT Specialist",
    }
    return position_mapping.get(domain, f"{domain} Specialist")


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

st.markdown("""
    <style>
        [data-testid="stMetricValue"] {
            font-size: 16px !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 12px !important;
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

        # Step 1: Text extract
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

        # Step 2: Extract candidate name
        candidate_name = extract_candidate_name(extracted_text)

        # Step 3: Classify domain
        result = None
        offer_result = None
        domain = "Unknown"
        confidence = 0
        status = "Manual Review"

        if extracted_text.strip():
            result = classify_resume(extracted_text)

            if st.session_state.get("last_processed") != uploaded_file.name:
                st.session_state.last_processed = uploaded_file.name
                st.session_state.processed += 1
                if st.session_state.pending > 0:
                    st.session_state.pending -= 1

            domain = result.get("predicted_domain", "Unknown")
            confidence = result.get("confidence", 0)
            status = result.get("status", "Manual Review")

            # Step 4: Generate offer letter if confidence score >= 75
            if confidence >= 75:
                position_title = get_position_title(domain)

                candidate_profile = {
                    "candidate_name": candidate_name,
                    "domain": domain,
                    "position_title": position_title,
                    "salary": "PKR 100,000 / month",
                    "company_name": "ORBIT-I",
                    "hr_signatory": "HR Department",
                    "probation_period": "3 months",
                    "location": "Hybrid - Karachi, Pakistan"
                }

                offer_result = generate_offer(candidate_profile)

            # Step 5: Log to audit
            log_event(
                cv_filename=uploaded_file.name,
                domain_assigned=domain,
                confidence_score=confidence,
                offer_status="Generated" if offer_result and offer_result.get("success") else "Flagged for Review",
                edited_by="System",
                notes=f"Confidence: {confidence}% | Candidate: {candidate_name}"
            )

        time.sleep(1)

    st.success(f"✅ File uploaded successfully: {uploaded_file.name}")

    st.divider()

    if result:
        st.subheader("🎯 Classification Result")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Candidate", candidate_name)

        with col2:
            st.metric("Domain", domain)

        with col3:
            st.metric("Confidence Score", f"{confidence}%")

        with col4:
            if status == "Manual Review":
                st.metric("Status", "⚠️ Manual Review")
            else:
                st.metric("Status", "✅ Auto Classified")

        st.divider()

        if status == "Manual Review":
            st.warning("⚠️ Confidence score is below 75%. This CV has been flagged for manual review.")
            if st.button("✏️ Go to Manual Override"):
                st.switch_page("pages/manual_override.py")

        else:
            if offer_result and offer_result.get("success"):
                st.success(f"✅ Offer letter generated for {candidate_name}!")
                offer_path = offer_result.get("offer_letter", "")
                with open(offer_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Offer Letter",
                        data=f,
                        file_name=os.path.basename(offer_path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            elif offer_result and offer_result.get("error"):
                st.error(f"❌ Offer generation failed: {offer_result.get('error')}")

    st.divider()

    if st.button("🏠 Back to Home"):
        st.switch_page("pages/home.py")
