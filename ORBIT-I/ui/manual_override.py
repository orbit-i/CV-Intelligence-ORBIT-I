import base64
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, datetime
from hr.validation import validate_email, validate_salary, validate_required

st.set_page_config(page_title="ORBIT-I | Manual Override", page_icon="✏️", layout="wide")

st.title("✏️ Manual Override Panel")
st.write("Review and edit candidate information before generating offer letter")

st.divider()

if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {
        "name": "",
        "email": "",
        "phone": "",
        "position": "",
        "salary": "",
        "joining_date": "",
        "domain": "",
        "remarks": ""
    }

if "preview_mode" not in st.session_state:
    st.session_state.preview_mode = False

if st.session_state.preview_mode:
    st.subheader("📄 Offer Letter Preview")

    data = st.session_state.candidate_data

    st.markdown(f"""
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

iCompany Pakistan
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Edit Again"):
            st.session_state.preview_mode = False
            st.rerun()
    with col2:
        if st.button("✅ Confirm & Generate Offer"):
            st.success("✅ Offer letter confirmed and ready for generation!")

else:
    st.subheader("📝 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name", value=st.session_state.candidate_data.get("name", ""))
        email = st.text_input("Email", value=st.session_state.candidate_data.get("email", ""))
        phone = st.text_input("Phone", value=st.session_state.candidate_data.get("phone", ""))
        domain = st.text_input("Domain", value=st.session_state.candidate_data.get("domain", ""))

    with col2:
        position = st.text_input("Position Title", value=st.session_state.candidate_data.get("position", ""))
        salary = st.text_input("Salary (numbers only)", value=st.session_state.candidate_data.get("salary", ""))
        joining_date = st.date_input(
            "Joining Date",
            value=date.today()
        )
        remarks = st.text_area("Remarks", value=st.session_state.candidate_data.get("remarks", ""))

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
            st.session_state.candidate_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "position": position,
                "salary": salary,
                "joining_date": joining_date.isoformat(),
                "domain": domain,
                "remarks": remarks
            }
            st.session_state.preview_mode = True
            st.rerun()
