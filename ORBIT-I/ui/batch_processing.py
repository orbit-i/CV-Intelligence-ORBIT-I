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


def extract_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(
            paragraph.text for paragraph in doc.paragraphs
        )
    return ""


if uploaded_files:
    st.session_state.results = []

    for file in uploaded_files:
        status = st.status(f"Processing {file.name}", expanded=True)

        try:
            text = extract_text(file)
            status.write("Resume text extracted successfully.")

            result = classify_resume(text)

            predicted_domain = result.get("predicted_domain", "Unknown")
            confidence = result.get("confidence", 0)

            st.session_state.results.append({
                "Candidate": file.name,
                "Domain": predicted_domain,
                "Confidence (%)": confidence,
                "Status": "Done"
            })

            status.update(label=f"{file.name} — Done ✅", state="complete")

        except Exception as e:
            st.session_state.results.append({
                "Candidate": file.name,
                "Domain": "-",
                "Confidence (%)": "-",
                "Status": "Failed"
            })

            status.update(label=f"{file.name} — Failed ❌", state="error")
            st.error(str(e))

if st.session_state.results:
    st.divider()
    st.subheader("📊 Processing Summary")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df, use_container_width=True)

st.divider()

output_folder = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "output"
)

if os.path.exists(output_folder):
    docx_files = [
        f for f in os.listdir(output_folder)
        if f.endswith(".docx") and f != "offer_letters.zip"
    ]

    if docx_files:
        zip_path = os.path.join(output_folder, "offer_letters.zip")

        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for f in docx_files:
                zip_file.write(os.path.join(output_folder, f), f)

        with open(zip_path, "rb") as f:
            st.download_button(
                label="⬇️ Download All Offer Letters (ZIP)",
                data=f,
                file_name="offer_letters.zip",
                mime="application/zip"
            )
    else:
        st.info("No offer letters generated yet.")
