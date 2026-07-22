import sys
import os

sys.path.insert(0
os. path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pdfplumber
from docx import Document
import zipfile
import os
import pandas as pd

from classifier.domain_classifier import classify_resume


st.set_page_config(page_title="Batch Processing Dashboard",layout="wide"
)

st.title("📄 Batch Processing Dashboard")
st.write("Upload multiple CVs to process them together.")


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
            paragraph.text
            for paragraph in doc.paragraphs
        )


if uploaded_files:

    st.session_state.results = []

    for file in uploaded_files:

        status = st.status(
            f"Processing {file.name}",
            expanded=True
        )

        try:

            text = extract_text(file)

            status.write(
                "Resume text extracted successfully."
            )


            result = classify_domain(text)


            # Adjust keys according to your classifier output
            predicted_domain = result.get(
                " predicted_domain",
                "Unknown"
            )

            confidence = result.get(
                "confidence",
                0
            )


            st.session_state.results.append(
                {
                    "Candidate": file.name,
                    "Domain": domain,
                    "Confidence": confidence,
                    "Status": "Done"
                }
            )


            status.update(
                label=f"{file.name} Done",
                state="complete"
            )


        except Exception as e:

            st.session_state.results.append(
                {
                    "Candidate": file.name,
                    "Domain": "-",
                    "Confidence": "-",
                    "Status": "Failed"
                }
            )


            status.update(
                label=f"{file.name} Failed",
                state="error"
            )

            st.error(e)



if st.session_state.results:

    st.subheader("Processing Summary")

    df = pd.DataFrame(
        st.session_state.results
    )

    st.dataframe(df)


# ZIP download for generated offer letters

output_folder = "data/output"

if os.path.exists(output_folder):

    docx_files = [
        file for file in os.listdir(output_folder)
        if file.endswith(".docx")
    ]

    if docx_files:

        zip_path = "data/output/offer_letters.zip"


        with zipfile.ZipFile(
            zip_path,
            "w"
        ) as zip_file:

            for file in docx_files:
                zip_file.write(
                    os.path.join(output_folder, file),
                    file
                )


        with open(zip_path, "rb") as file:

            st.download_button(
                label="⬇️ Download All Offer Letters",
                data=file,
                file_name="offer_letters.zip",
                mime="application/zip"
            )