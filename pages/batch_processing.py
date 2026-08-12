import sys
import os
import re
import hashlib
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'orbit-I'))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pdfplumber
from docx import Document
import zipfile
import pandas as pd

from classifier.domain_classifier import classify_resume
from core.offer_generator import generate_offer
from core.pdf_export import validate_offer_data, generate_offer_pdf, BATCH_REQUIRED_FIELDS

st.set_page_config(page_title="ORBIT-I | Batch Processing", page_icon="📄", layout="wide")

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col_title, col_top = st.columns([3, 2])
with col_title:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="stat-icon-circle">📄</div>
            <div>
                <h1 style="margin:0; padding:0; line-height:1.1;">Batch Processing Dashboard</h1>
                <p style="margin:0; color: var(--lb-text-muted); font-size:14px;">Upload multiple CVs to process them together.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_top:
    st.markdown("""
        <div class="orbit-topbar">
            <div class="orbit-search">🔍 <span>Search...</span></div>
            <div class="orbit-icon-btn">🔔</div>
            <div class="orbit-avatar">A</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

with st.container(border=True):
    st.markdown("##### Upload Resume Files")
    uploaded_files = st.file_uploader(
        "Drag & drop resume files here, or click Browse Files",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )
    st.caption("Supports PDF, DOCX  •  Max file size: 200MB per file")

if "results" not in st.session_state:
    st.session_state.results = []

if "total_uploaded" not in st.session_state:
    st.session_state.total_uploaded = 0

if "processed" not in st.session_state:
    st.session_state.processed = 0

if "pending" not in st.session_state:
    st.session_state.pending = 0

output_folder = os.path.join(BASE_DIR, "data", "output")
os.makedirs(output_folder, exist_ok=True)


def get_logo_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")


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


def extract_name(text):
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


def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group() if match else ""


def extract_phone(text):
    match = re.search(r'(\+92|0)[0-9\-]{9,12}', text)
    return match.group() if match else ""


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
    seen_hashes = set()
    seen_emails = set()

    for file in uploaded_files:
        status = st.status(f"Processing {file.name}", expanded=True)

        try:
            file_hash = hashlib.md5(file.getvalue()).hexdigest()

            if file_hash in seen_hashes:
                st.session_state.results.append({
                    "Candidate": file.name,
                    "Email": "",
                    "Phone": "",
                    "File": file.name,
                    "Domain": "-",
                    "Confidence (%)": "-",
                    "Status": "🔁 Duplicate File",
                    "Offer Path": ""
                })
                status.update(label=f"{file.name} — Duplicate File 🔁", state="error")
                continue

            seen_hashes.add(file_hash)

            text = extract_text(file)
            status.write("Text extracted successfully.")

            result = classify_resume(text)

            predicted_domain = result.get("predicted_domain", "Unknown")
            confidence = result.get("confidence", 0)
            candidate_name = extract_name(text)
            candidate_email = extract_email(text)
            candidate_phone = extract_phone(text)

            if candidate_email and candidate_email in seen_emails:
                st.session_state.results.append({
                    "Candidate": candidate_name,
                    "Email": candidate_email,
                    "Phone": candidate_phone,
                    "File": file.name,
                    "Domain": "-",
                    "Confidence (%)": "-",
                    "Status": "🔁 Duplicate Candidate",
                    "Offer Path": ""
                })
                status.update(label=f"{file.name} — Duplicate Candidate 🔁", state="error")
                continue

            if candidate_email:
                seen_emails.add(candidate_email)

            offer_path = None

            if confidence >= 75:
                candidate_profile = {
                    "candidate_name": candidate_name,
                    "domain": predicted_domain,
                    "position_title": get_position_title(predicted_domain),
                    "salary": "100,000",
                    "company_name": "ORBIT-I",
                    "hr_signatory": "HR Department",
                    "probation_period": "3 months",
                    "location": "Hybrid - Karachi, Pakistan",
                }
                offer_result = generate_offer(candidate_profile)
                if offer_result.get("success"):
                    offer_path = offer_result.get("offer_letter")
                    status.write("✅ Offer letter generated.")

                st.session_state.total_uploaded += 1
                st.session_state.processed += 1

            else:
                status.write("⚠️ Score below 75% — flagged for manual review.")
                st.session_state.total_uploaded += 1
                st.session_state.pending += 1

            st.session_state.results.append({
                "Candidate": candidate_name,
                "Email": candidate_email,
                "Phone": candidate_phone,
                "File": file.name,
                "Domain": predicted_domain,
                "Confidence (%)": confidence,
                "Status": "✅ Done" if confidence >= 75 else "⚠️ Manual Review",
                "Offer Path": offer_path or ""
            })

            status.update(
                label=f"{file.name} — {'Done ✅' if confidence >= 75 else 'Manual Review ⚠️'}",
                state="complete" if confidence >= 75 else "error"
            )

        except Exception as e:
            st.session_state.results.append({
                "Candidate": file.name,
                "Email": "",
                "Phone": "",
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

    total_count = len(st.session_state.results)
    done_count = sum(1 for r in st.session_state.results if "Done" in r["Status"])
    review_count = sum(1 for r in st.session_state.results if "Manual Review" in r["Status"])
    failed_count = sum(1 for r in st.session_state.results if "Failed" in r["Status"] or "Duplicate" in r["Status"])
    progress_pct = int(round((done_count / total_count) * 100)) if total_count else 0

    st.markdown("##### Processing Progress")
    st.progress(progress_pct / 100 if total_count else 0)
    st.caption(f"{progress_pct}% processed")

    st.markdown(f"""
        <div class="stat-card-row">
            <div class="stat-card">
                <div class="stat-icon-circle">📄</div>
                <div>
                    <div class="stat-label">Total Uploaded</div>
                    <div class="stat-value">{total_count}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon-circle success">✅</div>
                <div>
                    <div class="stat-label">Processed</div>
                    <div class="stat-value">{done_count}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon-circle warning">⏳</div>
                <div>
                    <div class="stat-label">Pending / Review</div>
                    <div class="stat-value">{review_count}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon-circle danger">✖️</div>
                <div>
                    <div class="stat-label">Failed</div>
                    <div class="stat-value">{failed_count}</div>
                </div>
            </div>
        </div>
        <br>
    """, unsafe_allow_html=True)

    st.subheader("📊 Batch Status")

    display_df = pd.DataFrame(st.session_state.results)[
        ["Candidate", "Email", "Phone", "Domain", "Confidence (%)", "Status"]
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
                        "name": candidate["Candidate"],
                        "email": candidate["Email"],
                        "phone": candidate["Phone"],
                        "position": get_position_title(candidate["Domain"]),
                        "salary": "100000",
                        "joining_date": "",
                        "domain": candidate["Domain"],
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

        dl_col1, dl_col2 = st.columns(2)

        with dl_col1:
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download All Offer Letters (DOCX ZIP)",
                    data=f,
                    file_name="offer_letters.zip",
                    mime="application/zip",
                    use_container_width=True
                )

        # ── PDF ZIP export ──
        # Build a candidate data dict per generated offer, matching the field
        # names generate_offer_pdf expects. Start Date isn't collected in the
        # batch flow, so "TBD" is used and Start Date is excluded from validation
        # (see BATCH_REQUIRED_FIELDS in core/pdf_export.py).
        pdf_candidates = []
        for r in st.session_state.results:
            if r["Offer Path"] and os.path.exists(r["Offer Path"]):
                pdf_data = {
                    "name": r["Candidate"],
                    "position": get_position_title(r["Domain"]),
                    "domain": r["Domain"],
                    "salary": "100,000",
                    "joining_date": "TBD",
                    "email": r["Email"],
                }
                is_valid, _missing = validate_offer_data(pdf_data, required_fields=BATCH_REQUIRED_FIELDS)
                if is_valid:
                    pdf_candidates.append(pdf_data)

        skipped_count = len(generated_offers) - len(pdf_candidates)

        with dl_col2:
            if pdf_candidates:
                pdf_zip_path = os.path.join(output_folder, "offer_letters_pdf.zip")
                offer_number_base = f"ORB/{datetime.now().year}/{datetime.now().strftime('%m%d')}"
                today = datetime.now().strftime("%d %B %Y")
                logo_path = get_logo_path()

                with zipfile.ZipFile(pdf_zip_path, "w") as pdf_zip:
                    for idx, cd in enumerate(pdf_candidates, start=1):
                        offer_number = f"{offer_number_base}-{idx:03d}"
                        pdf_buffer = generate_offer_pdf(
                            cd, offer_number, today, cd["joining_date"], logo_path=logo_path
                        )
                        safe_name = cd["name"].replace(" ", "_")
                        pdf_zip.writestr(f"Offer_Letter_{safe_name}.pdf", pdf_buffer.getvalue())

                with open(pdf_zip_path, "rb") as f:
                    st.download_button(
                        label="📕 Download All Offer Letters (PDF ZIP)",
                        data=f,
                        file_name="offer_letters_pdf.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
            else:
                st.button("📕 Download All Offer Letters (PDF ZIP)", use_container_width=True, disabled=True)

        if skipped_count > 0:
            st.caption(f"⚠️ {skipped_count} offer(s) skipped from PDF export due to missing required fields (name, position, department, salary, or email).")

    else:
        st.info("No offer letters generated yet — all CVs are pending manual review.")