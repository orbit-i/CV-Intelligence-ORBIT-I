import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, r"C:\Users\Admin\Desktop\orbit-I\orbit-I")

import streamlit as st
import pdfplumber
from docx import Document
import zipfile
import pandas as pd

from classifier.domain_classifier import classify_resume
from core.offer_generator import generate_offer

st.set_page_config(page_title="ORBIT-I | Batch Processing", layout="wide")

st.title("📄 Batch Processing Dashboard")
st.write("Upload multiple CVs to process them together.")

st.divider()

uploaded_files = st.file_uploader(
    "Upload Resume Files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if "results" not in st.session_state:
    st.session_state.results = []

output_folder = os.path.join(
    r"C:\Users\Admin\Desktop\orbit-I\orbit-I",
    "data", "output"
)
os.makedirs(output_folder, exist_ok=True)


def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    return ""


def extract_name(filename):
    name = filename.replace(".pdf", "").replace(".docx", "").replace("_", " ")
    return name


def get_position_title(domain):
    domain_lower = domain.lower()
    mapping = {
        "software engineering": "Software Engineer",
        "software development": "Software Developer",
        "web development": "Web Developer",
        "data science": "Data Scientist",
        "data analysis": "Data Analyst",
        "machine learning": "Machine Learning Engineer",
        "artificial intelligence": "AI Engineer",
        "cybersecurity": "Cybersecurity Analyst",
        "cyber security": "Cybersecurity Analyst",
        "ui/ux design": "UI/UX Designer",
        "graphic design": "Graphic Designer",
        "cloud computing": "Cloud Engineer",
        "devops": "DevOps Engineer",
        "business analysis": "Business Analyst",
        "public health": "Public Health Officer",
    }
    for key, value in mapping.items():
        if key in domain_lower:
            return value
    return f"{domain} Professional"


if uploaded_files:
    st.session_state.results = []
if uploaded_files:
    st.session_state.results = []
    if "total_uploaded" not in st.session_state:
        st.session_state.total_uploaded = 0
    if "processed" not in st.session_state:
        st.session_state.processed = 0
    if "pending" not in st.session_state:
        st.session_state.pending = 0
    for file in uploaded_files:
        status = st.status(f"Processing {file.name}", expanded=True)

        try:
            text = extract_text(file)
            status.write("Text extracted successfully.")

            result = classify_resume(text)

            predicted_domain = result.get("predicted_domain", "Unknown")
            confidence = result.get("confidence", 0)
            candidate_name = extract_name(file.name)

            offer_path = None
            if confidence >= 75:
                candidate_profile = {
                    "candidate_name": candidate_name,
                    "domain": predicted_domain,
                    "position_title": get_position_title(predicted_domain),
                    "salary": "PKR 100,000 / month",
                    "company_name": "ORBIT-I",
                    "hr_signatory": "HR Department",
                    "probation_period": "3 months",
                    "location": "Hybrid - Karachi, Pakistan",
                }
                offer_result = generate_offer(candidate_profile)
                if offer_result.get("success"):
                    offer_path = offer_result.get("offer_letter")
                    status.write("✅ Offer letter generated.")
            else:
                status.write("⚠️ Score below 75% — flagged for manual review.")

            st.session_state.results.append({
                "Candidate": candidate_name,
                "File": file.name,
                "Domain": predicted_domain,
                "Confidence (%)": confidence,
                "Status": "✅ Done" 
                 if confidence >= 75:
                st.session_state.total_uploaded += 1
                st.session_state.processed += 1
            else:
                st.session_state.total_uploaded += 1
                st.session_state.pending += 1
                if confidence >= 75 else "⚠️ Manual Review",
                "Offer Path": offer_path or ""
            })

            status.update(
                label=f"{file.name} — {'Done ✅' if confidence >= 75 else 'Manual Review ⚠️'}",
                state="complete" if confidence >= 75 else "error"
            )

        except Exception as e:
            st.session_state.results.append({
                "Candidate": file.name,
                "File": file.name,
                "Domain": "-",
                "Confidence (%)": "-",
                "Status": "❌ Failed",
                "Offer Path": ""
            })
            status.update(label=f"{file.name} — Failed ❌", state="error")
            st.error(str(e))

if st.session_state.results:
    st.divider()
    st.subheader("📊 Processing Summary")

    display_df = pd.DataFrame(st.session_state.results)[
        ["Candidate", "Domain", "Confidence (%)", "Status"]
    ]
    st.dataframe(display_df, use_container_width=True)

    st.divider()

    manual_review = [r for r in st.session_state.results if "Manual Review" in r["Status"]]

    if manual_review:
        st.subheader("⚠️ Candidates Flagged for Manual Review")
        for candidate in manual_review:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{candidate['Candidate']}** — Domain: {candidate['Domain']} | Score: {candidate['Confidence (%)']}%")
            with col2:
                if st.button("✏️ Manual Override", key=f"override_{candidate['File']}"):
                    st.session_state.candidate_data = {
                        "name": candidate['Candidate'],
                        "email": "",
                        "phone": "",
                        "position": get_position_title(candidate['Domain']),
                        "salary": "100000",
                        "joining_date": "",
                        "domain": candidate['Domain'],
                        "remarks": ""
                    }
                    st.session_state.preview_mode = False
                    st.switch_page("pages/manual_override.py")

    st.divider()

    generated_offers = [
        r["Offer Path"] for r in st.session_state.results
        if r["Offer Path"] and os.path.exists(r["Offer Path"])
    ]

    if generated_offers:
        zip_path = os.path.join(output_folder, "offer_letters.zip")

        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for offer_path in generated_offers:
                zip_file.write(offer_path, os.path.basename(offer_path))

        with open(zip_path, "rb") as f:
            st.download_button(
                label="⬇️ Download All Offer Letters (ZIP)",
                data=f,
                file_name="offer_letters.zip",
                mime="application/zip"
            )
    else:
        st.info("No offer letters generated yet — all CVs are pending manual review.")
