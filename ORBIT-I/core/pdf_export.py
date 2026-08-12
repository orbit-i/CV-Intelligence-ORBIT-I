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
    `joining` may be "TBD" for batch-generated offers where a start date hasn't been set yet.
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