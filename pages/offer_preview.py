import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'orbit-I'))

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="ORBIT-I | Offer Preview", page_icon="📄", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebarNav"] ul li:first-child {display: none;}
    [data-testid="stSidebarNav"]::before {
        content: "ORBIT-I";
        display: block;
        font-size: 20px;
        font-weight: 700;
        color: #1a3a6b;
        padding: 24px 16px 16px 16px;
        letter-spacing: 1px;
    }

    .summary-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 14px;
    }

    .summary-label {
        color: #64748b;
        width: 140px;
        flex-shrink: 0;
    }

    .summary-value {
        color: #0f172a;
        font-weight: 500;
    }

    .action-btn {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        margin-bottom: 10px;
        cursor: pointer;
        background: white;
    }

    .action-icon { font-size: 20px; }

    .action-label {
        font-weight: 600;
        font-size: 14px;
    }

    .action-desc {
        font-size: 12px;
        color: #64748b;
    }

    .letter-preview {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 40px 48px;
        min-height: 600px;
        font-family: 'Georgia', serif;
        font-size: 14px;
        line-height: 1.7;
        color: #1e293b;
    }

    .letter-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 2px solid #1a3a6b;
    }

    .letter-footer {
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: #94a3b8;
    }

    .note-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 10px;
        padding: 14px 16px;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ── Get candidate data from session state ──
data = st.session_state.get("candidate_data", {})
candidate_name = data.get("name", "Candidate")
position = data.get("position", "—")
domain = data.get("domain", "—")
salary = data.get("salary", "—")
location = data.get("joining_date", "—")
email = data.get("email", "—")
phone = data.get("phone", "—")
remarks = data.get("remarks", "—")
offer_path = st.session_state.get("offer_letter_path", "")
generated_on = datetime.now().strftime("%d %b %Y %I:%M %p")

# ── Header ──
col_title, col_back = st.columns([3, 1])
with col_title:
    st.markdown("## 📄 Offer Letter Preview & Export")
    st.markdown("<p style='color:#64748b; font-size:14px;'>Review the generated offer letter and export or send it to the candidate.</p>", unsafe_allow_html=True)
with col_back:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Manual Override", use_container_width=True):
        st.switch_page("pages/manual_override.py")

st.divider()

left_col, right_col = st.columns([3, 2], gap="large")

# ═══════════════════════════════
# LEFT — Offer Letter Preview
# ═══════════════════════════════
with left_col:
    # Zoom controls (visual only)
    z1, z2, z3, z4 = st.columns([1, 1, 1, 5])
    with z1:
        st.button("−")
    with z2:
        st.markdown("<div style='padding:8px 4px; font-size:13px; color:#64748b;'>100%</div>", unsafe_allow_html=True)
    with z3:
        st.button("+")
    with z4:
        if offer_path and os.path.exists(offer_path):
            with open(offer_path, "rb") as f:
                st.download_button("⬇", data=f,
                    file_name=os.path.basename(offer_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # Letter Preview
    offer_number = f"ORB/{datetime.now().year}/{datetime.now().strftime('%m%d')}"
    today = datetime.now().strftime("%d %B %Y")
    joining = data.get("joining_date", "TBD")
    expiry = data.get("joining_date", "TBD")

    st.markdown(f"""
    <div class="letter-preview">
        <div class="letter-header">
            <div>
                <div style='font-size:22px; font-weight:800; color:#1a3a6b; letter-spacing:-0.5px;'>ORBIT-I</div>
                <div style='font-size:12px; color:#64748b;'>Building Ideas. Creating Impact.</div>
            </div>
            <div style='text-align:right; font-size:12px; color:#64748b;'>
                <div>Offer No: {offer_number}</div>
                <div>Date: {today}</div>
            </div>
        </div>

        <p>Dear <strong>{candidate_name}</strong>,</p>

        <p>We are pleased to offer you the position of <strong>{position}</strong> at <strong>ORBIT-I</strong>.
        We were impressed with your qualifications and believe you will be a valuable addition to our team.</p>

        <table style='width:100%; margin:20px 0; border-collapse:collapse;'>
            <tr><td style='padding:6px 0; font-weight:600; width:180px;'>Position:</td><td>{position}</td></tr>
            <tr><td style='padding:6px 0; font-weight:600;'>Department:</td><td>{domain}</td></tr>
            <tr><td style='padding:6px 0; font-weight:600;'>Work Location:</td><td>Hybrid — Karachi, Pakistan</td></tr>
            <tr><td style='padding:6px 0; font-weight:600;'>Employment Type:</td><td>Full Time</td></tr>
            <tr><td style='padding:6px 0; font-weight:600;'>Start Date:</td><td>{joining}</td></tr>
        </table>

        <p>Your monthly compensation will be <strong>PKR {salary}</strong>.
        Details of your compensation and other benefits are outlined in the accompanying terms.</p>

        <p>Please review this offer letter carefully and confirm your acceptance within <strong>3 working days</strong>
        of receipt.</p>

        <p>We are excited about the possibility of you joining our team!</p>

        <br>
        <p>Sincerely,</p>
        <p><strong>HR Department</strong><br>ORBIT-I Team</p>

        <div class="letter-footer">
            <span>✉ orbiti2026@gmail.com</span>
            <span>📍 Karachi, Sindh, Pakistan</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════
# RIGHT — Summary + Actions
# ═══════════════════════════════
with right_col:

    # Candidate Summary
    st.markdown("### Candidate Summary")
    summary_items = [
        ("👤", "Candidate Name", candidate_name),
        ("💼", "Position", position),
        ("🏢", "Department", domain),
        ("📍", "Work Location", "Hybrid — Karachi, Pakistan"),
        ("⏰", "Employment Type", "Full Time"),
        ("📅", "Start Date", joining),
        ("💰", "Annual Salary", f"PKR {salary}"),
    ]

    for icon, label, value in summary_items:
        st.markdown(f"""
            <div class="summary-row">
                <span style='font-size:16px;'>{icon}</span>
                <span class="summary-label">{label}</span>
                <span class="summary-value">{value}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Offer Details
    st.markdown("### Offer Details")
    offer_items = [
        ("📅", "Offer Expiry", "3 working days"),
        ("📄", "Offer Template", f"{domain} Offer"),
        ("🕐", "Generated On", generated_on),
        ("👤", "Generated By", "HR System"),
    ]

    for icon, label, value in offer_items:
        st.markdown(f"""
            <div class="summary-row">
                <span style='font-size:16px;'>{icon}</span>
                <span class="summary-label">{label}</span>
                <span class="summary-value">{value}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Actions
    st.markdown("### Actions")

    # Edit Offer Details
    if st.button("✏️ Edit Offer Details", use_container_width=True):
        st.switch_page("pages/manual_override.py")

    st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:-8px; margin-bottom:12px;'>Make changes to candidate or offer details</p>", unsafe_allow_html=True)

    # Download DOCX
    if offer_path and os.path.exists(offer_path):
        with open(offer_path, "rb") as f:
            st.download_button(
                "📄 Download as DOCX",
                data=f,
                file_name=os.path.basename(offer_path),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:-8px; margin-bottom:12px;'>Export offer letter as Word document</p>", unsafe_allow_html=True)
    else:
        st.button("📄 Download as DOCX", use_container_width=True, disabled=True)
        st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:-8px; margin-bottom:12px;'>No offer letter generated yet</p>", unsafe_allow_html=True)

    # Send to Candidate
    st.button("📧 Send Offer to Candidate", use_container_width=True, disabled=True)
    st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:-8px; margin-bottom:12px;'>Email the offer letter to the candidate (coming soon)</p>", unsafe_allow_html=True)

    # Note
    st.markdown("""
        <div class="note-box">
            <p style='font-size:13px; color:#92400e; margin:0;'>
                ⚠️ <strong>Note:</strong> Please review all information carefully before
                sending the offer to the candidate.
            </p>
        </div>
    """, unsafe_allow_html=True)
