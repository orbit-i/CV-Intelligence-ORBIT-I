# 🚀 ORBIT-I
### Optimized Resume Benchmarking, Intelligence & Talent Identification

An AI-powered Resume Analyzer and Offer Letter Automation platform built using **Python**, **Streamlit**, and **Google Gemini AI**.

ORBIT-I streamlines the recruitment process by intelligently analyzing resumes, extracting candidate information, classifying professional domains, and generating personalized offer letters.

---

## 📌 Project Overview

Traditional recruitment involves manually reviewing hundreds of resumes, consuming significant time and effort.

ORBIT-I automates this workflow by:

- Parsing resumes (PDF & DOCX)
- Extracting structured candidate information
- Performing AI-powered resume analysis
- Classifying candidate domains
- Generating professional offer letters
- Preparing the project for future ATS integration

---

## ✨ Key Features

- 📄 PDF Resume Parsing
- 📝 DOCX Resume Parsing
- 👤 Candidate Information Extraction
- 🤖 Google Gemini AI Integration
- 🎯 Domain Classification
- 📊 Resume Analysis Dashboard
- 📑 Automated Offer Letter Generation
- 💾 Export Results
- 🎨 Modern Streamlit UI
- 🔒 Modular & Scalable Architecture

---

## 🛠 Tech Stack

### Frontend

- Streamlit
- HTML
- CSS

### Backend

- Python 3.10+

### AI

- Google Gemini API

### NLP

- spaCy

### Document Processing

- PyMuPDF
- python-docx
- docxtpl

### Data Processing

- Pandas

---

## 📂 Project Structure

```text
ORBIT-I/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── styles.css
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── prompts.py
│
├── parser/
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   └── extractor.py
│
├── services/
│   ├── file_handler.py
│   ├── candidate_service.py
│   └── offer_service.py
│
├── ui/
│   ├── components.py
│   ├── home.py
│   └── upload.py
│
├── models/
│
├── uploads/
│
├── output/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/ORBIT-I.git
```

Move into the project

```bash
cd ORBIT-I
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download spaCy language model

```bash
python -m spacy download en_core_web_sm
```

Run the application

```bash
streamlit run app.py
```

---

## 📋 Current Progress

- [x] Project Planning
- [x] Folder Structure
- [x] Environment Setup
- [x] Streamlit Configuration
- [x] Global Styling
- [x] Home Dashboard
- [x] Resume Upload Module

### Upcoming

- [ ] PDF Parser
- [ ] DOCX Parser
- [ ] Information Extraction
- [ ] AI Resume Analysis
- [ ] Domain Classification
- [ ] Offer Letter Generation
- [ ] Dashboard Analytics
- [ ] Database Integration
- [ ] Authentication
- [ ] Deployment

---

## 🎯 Future Scope

- Applicant Tracking System (ATS)
- HR Dashboard
- Resume Scoring
- Candidate Ranking
- Skill Gap Analysis
- Email Automation
- Interview Scheduling
- Multi-language Resume Support
- Cloud Deployment

---

## 🤝 Contribution Guidelines

1. Create a new branch before starting work.
2. Follow the project folder structure.
3. Write clean and modular code.
4. Test your code before committing.
5. Submit changes through a Pull Request.
6. Update documentation whenever necessary.

---

## 👨‍💻 Team Members

| Name | Role | Contributions |
|------|------|---------------|
| **Musawir Hassan** | Project Lead | Project Architecture, Backend Development, AI Integration |
| **Mahnoor**| Backend Developer Intern| Python|
| | | |
| **Kashif Lakho** | Python Developer | Backend Development |
| | | |

> Add your name and contributions before your first commit.

---

## 📜 License

This project is developed for educational and research purposes.

---

## ⭐ Acknowledgements

- Google Gemini AI
- Streamlit
- spaCy
- PyMuPDF
- Python Community

---

### 🚀 ORBIT-I

**Transforming Recruitment Through Artificial Intelligence**
