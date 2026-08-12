import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "ORBIT-I")
)
sys.path.insert(0, BASE_DIR)

from datetime import date
from hr.validation import (
    validate_email,
    validate_salary,
    validate_required,
)
from services.offer_service import create_offer
from classifier.preprocess import preprocess_text
from classifier.keyword_matcher import keyword_match
from classifier.confidence_score import calculate_confidence


def get_confidence_for_domain(domain_name, resume_text):
    """
    Given a domain name and the original resume text, return the
    confidence score for that specific domain.
    """
    if not resume_text or not domain_name:
        return 0
    preprocessed = preprocess_text(resume_text)
    match_results = keyword_match(preprocessed)
    confidence_results = calculate_confidence(match_results)

    # Try exact match first, then case-insensitive
    for d, info in confidence_results.items():
        if d.lower().strip() == domain_name.lower().strip():
            return info["confidence"]
    return 0

st.set_page_config(
    page_title="ORBIT-I | Manual Override",
    page_icon="✏️",
    layout="wide",
)

with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "style.css"), encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col_title, col_badge = st.columns([3, 2])
with col_title:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="stat-icon-circle">✏️</div>
            <div>
                <h1 style="margin:0; padding:0; line-height:1.1;">Manual Override Panel</h1>
                <p style="margin:0; color: var(--lb-text-muted); font-size:14px;">Review and edit AI extracted candidate details before generating the final offer letter.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_badge:
    _confidence_for_badge = st.session_state.get("candidate_data", {}).get("confidence", 0) or 0
    st.markdown(f"""
        <div class="confidence-badge">
            <div class="cb-title">AI Extraction Confidence</div>
            <div class="cb-value">{_confidence_for_badge}% Accurate</div>
            <div class="cb-sub">{"High Confidence" if _confidence_for_badge >= 75 else "Needs Review"}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# -----------------------------
# Session State Initialization
# -----------------------------
if "candidate_data" not in st.session_state:
    st.session_state["candidate_data"] = {
        "name": "",
        "email": "",
        "phone": "",
        "position": "",
        "salary": "",
        "joining_date": "",
        "domain": "",
        "remarks": "",
    }

if "preview_mode" not in st.session_state:
    st.session_state["preview_mode"] = False


# ==========================================================
# PREVIEW MODE
# ==========================================================
if st.session_state["preview_mode"]:

    data = st.session_state["candidate_data"]

    st.subheader("📄 Offer Letter Preview")

    st.markdown(
        f"""
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

ORBIT-I
"""
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✏️ Edit Again"):
            st.session_state["preview_mode"] = False
            st.rerun()

    with col2:
        if st.button("✅ Confirm & Generate Offer"):

            candidate_profile = {
                "candidate_name": data.get("name", "Candidate"),
                "domain": data.get("domain", ""),
                "position_title": data.get("position", ""),
                "salary": data.get("salary", ""),
                "company_name": "ORBIT-I",
                "hr_signatory": "HR Department",
                "probation_period": "3 months",
                "location": "Hybrid - Karachi, Pakistan",
            }

            offer_result = create_offer(candidate_profile)

            if offer_result.get("success"):

                st.session_state["candidate_data"] = data
                st.session_state["offer_letter_path"] = offer_result["offer_letter"]

                st.switch_page("pages/offer_preview.py")

            else:
                st.error(
                    offer_result.get(
                        "error",
                        "Failed to generate offer letter.",
                    )
                )

# ==========================================================
# EDIT MODE
# ==========================================================
else:

  with st.container(border=True):
    st.markdown("##### 👤 Candidate Information")
    st.caption("Editable candidate details extracted by AI.")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Full Name",
            value=st.session_state["candidate_data"].get("name", ""),
        )

        email = st.text_input(
            "Email",
            value=st.session_state["candidate_data"].get("email", ""),
        )

        phone = st.text_input(
            "Phone",
            value=st.session_state["candidate_data"].get("phone", ""),
        )

        # ── Domain selector with live confidence ──────────────────
        known_domains = [
            "Software Engineering",
            "Data Science",
            "Cybersecurity",
            "Web Development",
            "Data Engineering",
            "DevOps",
            "UI/UX Design",
        ]

        current_domain = st.session_state["candidate_data"].get("domain", "")
        default_idx = 0
        for i, d in enumerate(known_domains):
            if d.lower().strip() == current_domain.lower().strip():
                default_idx = i
                break

        domain = st.selectbox(
            "Domain",
            options=known_domains,
            index=default_idx,
            help="Select the domain that best matches this candidate's CV.",
        )

        # ── Look up confidence for the selected domain ─────────────
        # all_domain_scores is a dict: {"Cybersecurity": 87.5, "Data Science": 62.0, ...}
        # populated by the upload page after classification.
        all_scores = st.session_state.get("all_domain_scores", {})

        # Find the score for the currently selected domain (case-insensitive)
        selected_confidence = 0
        for d, score in all_scores.items():
            if d.lower().strip() == domain.lower().strip():
                selected_confidence = score
                break

        # If all_scores is empty (user navigated here directly),
        # fall back to re-computing from the stored resume text
        if selected_confidence == 0 and not all_scores:
            resume_text = st.session_state.get("extracted_text", "")
            if resume_text:
                selected_confidence = get_confidence_for_domain(domain, resume_text)

        # Display the confidence for the selected domain
        if selected_confidence > 0:
            bar_color = "#16a34a" if selected_confidence >= 75 else "#f59e0b" if selected_confidence >= 50 else "#ef4444"
            st.markdown(
                f"""
                <div style='margin-top:4px; margin-bottom:12px; padding:8px 12px;
                            background:#f8fafc; border-radius:6px; border-left:3px solid {bar_color};'>
                    <span style='font-size:13px; color:#64748b;'>Confidence for <b>{domain}</b>: </span>
                    <span style='font-size:18px; font-weight:700; color:{bar_color};'>{selected_confidence}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.caption(f"⚠️ No keyword matches found for '{domain}'. Please verify this domain is correct.")

    with col2:

        # Auto-suggest position from selected domain
        def get_position_title_mo(d):
            mapping = {
                "software engineering": "Software Engineer",
                "data science": "Data Scientist",
                "cybersecurity": "Cybersecurity Analyst",
                "web development": "Web Developer",
                "data engineering": "Data Engineer",
                "devops": "DevOps Engineer",
                "ui/ux design": "UI/UX Designer",
            }
            return mapping.get(d.lower().strip(), f"{d} Professional")

        # Use the auto-suggested title if the stored position matches
        # the old domain, otherwise keep whatever HR typed
        suggested_position = get_position_title_mo(domain)
        stored_position = st.session_state["candidate_data"].get("position", "")

        position = st.text_input(
            "Position Title",
            value=suggested_position if not stored_position else stored_position,
            help="Auto-filled from domain. You can edit this.",
        )

        salary = st.text_input(
            "Salary (numbers only)",
            value=st.session_state["candidate_data"].get("salary", ""),
        )

        joining_date = st.date_input(
            "Joining Date",
            value=date.today(),
        )

        remarks = st.text_area(
            "Remarks",
            value=st.session_state["candidate_data"].get("remarks", ""),
        )

    st.divider()

    if st.button("💾 Save & Preview"):

        errors = []

        if not validate_required(name):
            errors.append("Name is required")

        if not validate_required(position):
            errors.append("Position is required")

        if not validate_email(email):
            errors.append("Invalid email address")

        if not validate_salary(salary):
            errors.append("Salary must contain numbers only")

        if errors:

            for error in errors:
                st.error(f"❌ {error}")

        else:

            st.session_state["candidate_data"] = {
                "name": name,
                "email": email,
                "phone": phone,
                "position": position,
                "salary": salary,
                "joining_date": joining_date.isoformat(),
                "domain": domain,
                "confidence": selected_confidence,
                "remarks": remarks,
            }

            st.session_state["preview_mode"] = True
            st.rerun()
