from docx import Document
from pathlib import Path

def generate_offer(candidate_profile):
    base_dir = Path(__file__).resolve().parent.parent
    template_path = base_dir / "templates" / "offer_template.docx"

    print("Template path:", template_path)
    print("Exists:", template_path.exists())

    doc = Document(template_path)

    for paragraph in doc.paragraphs:
        paragraph.text = paragraph.text.replace("{{candidate_name}}", candidate_profile.get("candidate_name", ""))
        paragraph.text = paragraph.text.replace("{{domain}}", candidate_profile.get("domain", ""))
        paragraph.text = paragraph.text.replace("{{salary}}", candidate_profile.get("salary", ""))
        paragraph.text = paragraph.text.replace("{{start_date}}", candidate_profile.get("start_date", ""))

    output_file = base_dir / "templates" / f"{candidate_profile.get('candidate_name', 'candidate')}_offer.docx"
    doc.save(output_file)

    return {"offer_letter": str(output_file)}

if __name__ == "__main__":
    test_data = {
        "candidate_name": "Ahsan Khan",
        "domain": "AI Engineering", 
        "salary": "150000",
        "start_date": "2026-12-01"
    }
    
    result = generate_offer(test_data)
    print("Success! Offer saved to:", result["offer_letter"])