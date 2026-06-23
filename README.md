# CV-Intelligence-ORBIT-I
# 🚀 ORBIT-I (CV Intelligence & Offer Automation Platform)

ORBIT-I is a Python + Streamlit-based HR automation application designed to streamline CV processing, candidate profiling, and automated offer letter generation.

It enables HR teams to efficiently upload CVs, extract structured data, classify candidates by domain, and generate professional offer letters in DOCX/PDF formats.

---

## 📌 Project Overview

ORBIT-I is built to automate key HR workflows:

- CV upload and validation (single/multiple PDFs)
- Intelligent CV parsing and structured data extraction
- Domain classification of candidates
- Editable offer letter generation
- Template management system
- Export functionality (DOCX & PDF)
- Audit logging using in-memory storage

---

## 👥 User Roles

- HR Manager  
- HR Recruiter  
- Department Head  
- System Administrator  

---

## ⚙️ Core Features

### 📤 CV Upload
- Upload single or multiple PDF CVs  
- File type validation  
- Upload status indicators  
- Progress tracking UI  

---

### 📄 CV Parser
Extracts structured candidate information:

- Full Name  
- Email Address  
- Phone Number  
- Skills  
- Work Experience  
- Education  
- Certifications  
- Location  

Parsed data is displayed in editable form for HR review.

---

### 🧠 Domain Classification
Automatically classifies candidates into domains:

- Software Engineering  
- Artificial Intelligence / Machine Learning  
- Data Science  
- Cyber Security  
- DevOps  
- Quality Assurance  
- UI/UX Design  
- Networking  
- Cloud Computing  
- Other  

Includes confidence score and manual override option.

---

### ✉️ Offer Letter Generator
Generates customized offer letters using templates.

Editable fields include:

- Candidate Name  
- Position Title  
- Department  
- Salary Package  
- Joining Date  
- Reporting Manager  
- Benefits  
- Custom Clauses  

Includes live preview before export.

---

### 🧩 Template Management
- View available templates  
- Duplicate templates  
- Edit placeholders dynamically  
- Preview template structure  

(No database required — uses mock storage)

---

### 📦 Export System
Supports export of generated offer letters:

- DOCX (using `python-docx`)  
- PDF (using `ReportLab`)  

---

### 📊 Audit Log
Tracks system activity:

- CV uploads  
- Offer letter generation  
- Export history  
- User interactions  

Stored in-memory for simplicity.

---

## 🛠️ Tech Stack

- Python 3.10+  
- Streamlit  
- Pandas  
- pdfplumber / PyMuPDF  
- python-docx  
- ReportLab  

---

## 🚫 Project Constraints

This project intentionally avoids:

- Databases  
- Authentication systems  
- External APIs  
- Cloud deployment  
- Docker  
- Email services  

All such features are simulated using mock data or in-memory structures.

---

## 📁 Project Structure

```bash
ORBIT-I/
│
├── app.py
├── pages/
├── components/
├── services/
├── parsers/
├── generators/
├── templates/
├── utils/
├── assets/
├── sample_data/
└── README.md