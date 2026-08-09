import sys
import os
import textwrap
import base64
from io import BytesIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'orbit-I'))

import streamlit as st
from datetime import datetime

from reportlab.lib.pagesizes import letter as PAGE_LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)

st.set_page_config(page_title="ORBIT-I | Offer Preview", page_icon="📄", layout="wide")


def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""


def get_logo_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "logo.png")


# ═══════════════════════════════
# PDF EXPORT — validation + generation
# ═══════════════════════════════

def validate_offer_data(data: dict) -> tuple[bool, list[str]]:
    """Checks that required fields exist and are populated before PDF generation.
    Returns (is_valid, list_of_missing_field_labels).
    """
    required_fields = {
        "name": "Candidate Name",
        "position": "Position",
        "domain": "Department",
        "salary": "Salary",
        "joining_date": "Start Date",
        "email": "Email",
    }
    missing = []
    for key, label in required_fields.items():
        value = data.get(key)
        if not value or str(value).strip() in ("", "—", "TBD", "None"):
            missing.append(label)
    return (len(missing) == 0, missing)


def generate_offer_pdf(data: dict, offer_number: str, today: str, joining: str, logo_path: str) -> BytesIO:
    """Builds the offer letter as a PDF in memory and returns it as a BytesIO buffer.
    Mirrors the on-screen HTML preview's structure and content.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=PAGE_LETTER,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontName="Times-Roman",
        fontSize=11, leading=16, spaceAfter=10
    )
    company_style = ParagraphStyle(
        "Company", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=16, textColor=HexColor("#1a3a6b")
    )
    meta_style = ParagraphStyle(
        "Meta", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9, textColor=HexColor("#64748b"), alignment=2
    )

    story = []

    # ── Header: logo + company name (left), offer no/date (right) ──
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=0.55 * inch, height=0.55 * inch)
    else:
        logo = Paragraph("", body_style)

    header_left = Table(
        [[logo, Paragraph(
            "ORBIT-I<br/><font size=8 color='#64748b'>Building Ideas, Creating Impacts</font>",
            company_style
        )]],
        colWidths=[0.6 * inch, 2.5 * inch]
    )
    header_left.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))

    header_right = Paragraph(f"Offer No: {offer_number}<br/>Date: {today}", meta_style)

    header_table = Table([[header_left, header_right]], colWidths=[3.5 * inch, 2.5 * inch])
    header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(header_table)
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=HexColor("#2E5AAC")))
    story.append(Spacer(1, 16))

    # ── Body ──
    candidate_name = data.get("name", "Candidate")
    position = data.get("position", "—")
    domain = data.get("domain", "—")
    salary = data.get("salary", "—")

    story.append(Paragraph(f"Dear <b>{candidate_name}</b>,", body_style))
    story.append(Paragraph(
        f"We are pleased to offer you the position of <b>{position}</b> at <b>ORBIT-I</b>. "
        f"We were impressed with your qualifications and believe you will be a valuable "
        f"addition to our team.", body_style
    ))

    details = [
        ["Position:", position],
        ["Department:", domain],
        ["Work Location:", "Hybrid — Karachi, Pakistan"],
        ["Employment Type:", "Full Time"],
        ["Start Date:", joining],
    ]
    details_table = Table(details, colWidths=[1.8 * inch, 4.0 * inch])
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Times-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 10))
    story.append(details_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"Your monthly compensation will be <b>PKR {salary}</b>. Details of your "
        f"compensation and other benefits are outlined in the accompanying terms.", body_style
    ))
    story.append(Paragraph(
        "Please review this offer letter carefully and confirm your acceptance within "
        "<b>3 working days</b> of receipt.", body_style
    ))
    story.append(Paragraph("We are excited about the possibility of you joining our team!", body_style))
    story.append(Spacer(1, 20))
    story.append(Paragraph("Sincerely,<br/><b>HR Department</b><br/>ORBIT-I Team", body_style))

    # ── Footer ──
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#e2e8f0")))
    story.append(Spacer(1, 6))
    footer_table = Table(
        [["orbiti2026@gmail.com", "Karachi, Sindh, Pakistan"]],
        colWidths=[3.5 * inch, 2.5 * inch]
    )
    footer_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), HexColor("#94a3b8")),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(footer_table)

    doc.build(story)
    buffer.seek(0)
    return buffer


logo_base64 = get_logo_base64()

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
        border-bottom: 3px solid #2E5AAC;
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

    letter_html = f"""<div class="letter-preview">
<div class="letter-header">
<div style="display:flex; align-items:center; gap:14px;">
<img src="data:image/png;base64,{logo_base64}" style="height:48px;">
<div>
<div style='font-size:22px; font-weight:800; color:#1a3a6b; letter-spacing:-0.5px;'>ORBIT-I</div>
<div style='font-size:12px; color:#64748b;'>Building Ideas, Creating Impacts</div>
</div>
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
</div>"""

    st.markdown(letter_html, unsafe_allow_html=True)

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

    # ── Download DOCX / PDF ──
    is_valid, missing_fields = validate_offer_data(data)

    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        if offer_path and os.path.exists(offer_path):
            with open(offer_path, "rb") as f:
                st.download_button(
                    "📄 DOCX",
                    data=f,
                    file_name=os.path.basename(offer_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
        else:
            st.button("📄 DOCX", use_container_width=True, disabled=True)

    with dl_col2:
        if is_valid:
            pdf_buffer = generate_offer_pdf(
                data, offer_number, today, joining, logo_path=get_logo_path()
            )
            st.download_button(
                "📕 PDF",
                data=pdf_buffer,
                file_name=f"Offer_Letter_{candidate_name.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.button("📕 PDF", use_container_width=True, disabled=True)

    if not is_valid:
        st.markdown(
            f"<p style='font-size:11px; color:#dc2626; margin-top:4px; margin-bottom:12px;'>⚠️ Missing required fields: {', '.join(missing_fields)}. Fix these in Manual Override before exporting.</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown("<p style='font-size:11px; color:#94a3b8; margin-top:4px; margin-bottom:12px;'>Export offer letter as Word or PDF</p>", unsafe_allow_html=True)

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