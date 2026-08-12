"""
core/pdf_export.py

Shared PDF generation and validation logic for offer letters.
Used by pages/offer_preview.py (single candidate) and pages/batch_processing.py (bulk export).
"""
import os
from io import BytesIO

from reportlab.lib.pagesizes import letter as PAGE_LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)

# Full field set — used on the single-offer Preview page, where Start Date is
# always collected via Manual Override before the letter is finalized.
FULL_REQUIRED_FIELDS = {
    "name": "Candidate Name",
    "position": "Position",
    "domain": "Department",
    "salary": "Salary",
    "joining_date": "Start Date",
    "email": "Email",
}

# Reduced field set — used for Batch Processing exports, where offers are
# auto-generated without a Start Date being collected yet.
BATCH_REQUIRED_FIELDS = {
    "name": "Candidate Name",
    "position": "Position",
    "domain": "Department",
    "salary": "Salary",
    "email": "Email",
}


def validate_offer_data(data: dict, required_fields: dict = None) -> tuple[bool, list[str]]:
    """Checks that required fields exist and are populated before PDF generation.
    Pass `required_fields` to control which fields are mandatory (see FULL_REQUIRED_FIELDS
    vs BATCH_REQUIRED_FIELDS above). Defaults to the full set.
    Returns (is_valid, list_of_missing_field_labels).
    """
    fields = required_fields if required_fields is not None else FULL_REQUIRED_FIELDS
    missing = []
    for key, label in fields.items():
        value = data.get(key)
        if not value or str(value).strip() in ("", "—", "TBD", "None"):
            missing.append(label)
    return (len(missing) == 0, missing)


def generate_offer_pdf(data: dict, offer_number: str, today: str, joining: str, logo_path: str) -> BytesIO:
    """Builds a single offer letter as a PDF in memory and returns it as a BytesIO buffer.
    Mirrors the wording and layout of templates/offer_template.docx (the DOCX export)
    so both formats produce a consistent letter. `joining` may be "TBD" for
    batch-generated offers where a start date hasn't been set yet.
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
        fontSize=14, textColor=HexColor("#1a3a6b")
    )
    company_sub_style = ParagraphStyle(
        "CompanySub", parent=styles["Normal"], fontName="Helvetica",
        fontSize=8, textColor=HexColor("#64748b"), leading=11
    )
    meta_style = ParagraphStyle(
        "Meta", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9, textColor=HexColor("#64748b"), alignment=2, leading=13
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=12, textColor=HexColor("#1a3a6b"), spaceBefore=6, spaceAfter=8
    )
    sign_style = ParagraphStyle(
        "Sign", parent=styles["Normal"], fontName="Times-Roman",
        fontSize=10, leading=15
    )

    story = []

    # ── Header: logo + company name/address (left), offer no/date (right) ──
    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=0.5 * inch, height=0.5 * inch)
    else:
        logo = Paragraph("", body_style)

    header_left = Table(
        [[logo, Paragraph(
            "ORBIT-I<br/>"
            "<font size=8 color='#64748b'>CV Intelligence &amp; Offer Automation Platform<br/>"
            "Karachi, Sindh, Pakistan &nbsp;&middot;&nbsp; orbiti2026@gmail.com</font>",
            company_style
        )]],
        colWidths=[0.55 * inch, 3.45 * inch]
    )
    header_left.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))

    header_right = Paragraph(
        f"Date: {today}<br/>Ref: {offer_number}", meta_style
    )

    header_table = Table([[header_left, header_right]], colWidths=[4.0 * inch, 2.0 * inch])
    header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    story.append(header_table)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=HexColor("#2E5AAC")))
    story.append(Spacer(1, 16))

    # ── Body — same wording as the DOCX template ──
    candidate_name = data.get("name", "Candidate")
    position = data.get("position", "—")
    domain = data.get("domain", "—")
    salary = data.get("salary", "—")
    location = data.get("location") or "Hybrid — Karachi, Pakistan"
    probation_period = data.get("probation_period") or "3 months"
    hr_signatory = data.get("hr_signatory") or "HR Department"

    story.append(Paragraph(f"Dear <b>{candidate_name}</b>,", body_style))
    story.append(Paragraph(
        f"We are pleased to extend this formal offer of employment for the position of "
        f"<b>{position}</b> within the <b>{domain}</b> department at <b>ORBIT-I</b>. "
        f"We believe your skills and experience make you an excellent fit for our team.",
        body_style
    ))

    story.append(Paragraph("Employment Details", section_style))

    details = [
        ["Position Title", position],
        ["Department / Domain", domain],
        ["Monthly Salary", f"PKR {salary}"],
        ["Date of Joining", joining],
        ["Work Location", location],
        ["Probation Period", probation_period],
        ["Reporting To", hr_signatory],
    ]
    details_table = Table(details, colWidths=[2.0 * inch, 3.8 * inch])
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Times-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Times-Roman"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, HexColor("#e2e8f0")),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 14))

    story.append(Paragraph(
        f"This offer is subject to the successful completion of your probation period of "
        f"<b>{probation_period}</b>, during which your performance will be evaluated against "
        f"the key objectives of your role.", body_style
    ))
    story.append(Paragraph(
        "Please confirm your acceptance of this offer by signing and returning a copy of "
        "this letter within three (3) working days of receipt. Failure to do so may result "
        "in the offer being withdrawn.", body_style
    ))
    story.append(Paragraph(
        "We look forward to welcoming you to the team and are excited about the "
        "contributions you will bring to ORBIT-I.", body_style
    ))
    story.append(Spacer(1, 24))

    # ── Signature block (mirrors the DOCX acceptance table) ──
    sign_table = Table(
        [[
            Paragraph(
                f"Sincerely,<br/><br/>_______________________<br/>"
                f"{hr_signatory}<br/>ORBIT-I<br/>Karachi, Sindh, Pakistan",
                sign_style
            ),
            Paragraph(
                f"Accepted by:<br/><br/>_______________________<br/>"
                f"{candidate_name}<br/>Date: _______________",
                sign_style
            ),
        ]],
        colWidths=[2.9 * inch, 2.9 * inch]
    )
    sign_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(sign_table)

    # ── Footer ──
    story.append(Spacer(1, 26))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#e2e8f0")))
    story.append(Spacer(1, 6))
    footer_style = ParagraphStyle(
        "Footer", parent=styles["Normal"], fontName="Helvetica",
        fontSize=7.5, textColor=HexColor("#94a3b8"), alignment=1
    )
    story.append(Paragraph(
        "ORBIT-I &nbsp;&middot;&nbsp; Karachi, Sindh, Pakistan &nbsp;&middot;&nbsp; "
        "orbiti2026@gmail.com &nbsp;&middot;&nbsp; This document is confidential and "
        "intended solely for the named recipient.", footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer