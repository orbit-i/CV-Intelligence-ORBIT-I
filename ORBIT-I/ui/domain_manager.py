import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin.domain_manager import (
    create_table,
    add_domain,
    view_domains,
    update_domain,
    delete_domain,
)

create_table()

st.set_page_config(page_title="ORBIT-I | Domain Manager", page_icon="🌐", layout="wide")

st.title("🌐 Domain Manager")
st.write("Manage hiring domains for CV classification")

st.divider()

menu = st.selectbox(
    "Choose Action",
    ["View All Domains", "Add Domain", "Update Domain", "Delete Domain"]
)

st.divider()

if menu == "View All Domains":
    domains = view_domains()
    if domains:
        import pandas as pd
        df = pd.DataFrame(domains, columns=["ID", "Domain Name", "Keywords", "Required Skills", "Salary Range", "Offer Letter Template"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("Total Domains", len(domains))
    else:
        st.info("No domains added yet.")

elif menu == "Add Domain":
    st.subheader("Add New Domain")
    col1, col2 = st.columns(2)
    with col1:
        domain_name = st.text_input("Domain Name", placeholder="e.g. Software Engineering")
        keywords = st.text_input("Keywords", placeholder="e.g. Python, Django, FastAPI")
        required_skills = st.text_input("Required Skills", placeholder="e.g. Git, SQL")
    with col2:
        salary_range = st.text_input("Salary Range", placeholder="e.g. 100k-200k")
        offer_letter_template = st.text_input("Offer Letter Template", placeholder="e.g. software_offer.docx")

    if st.button("✅ Add Domain"):
        if domain_name:
            message = add_domain(domain_name, keywords, required_skills, salary_range, offer_letter_template)
            st.success(message)
        else:
            st.warning("Domain name is required.")

elif menu == "Update Domain":
    st.subheader("Update Existing Domain")
    col1, col2 = st.columns(2)
    with col1:
        old_domain_name = st.text_input("Current Domain Name")
        domain_name = st.text_input("New Domain Name")
        required_skills = st.text_input("Required Skills")
    with col2:
        keywords = st.text_input("Keywords")
        salary_range = st.text_input("Salary Range")
        offer_letter_template = st.text_input("Offer Letter Template")

    if st.button("✅ Update Domain"):
        if old_domain_name:
            message = update_domain(old_domain_name, domain_name, keywords, required_skills, salary_range, offer_letter_template)
            st.success(message)
        else:
            st.warning("Current domain name is required.")

elif menu == "Delete Domain":
    st.subheader("Delete Domain")
    domain_name = st.text_input("Domain Name to Delete")
    if st.button("🗑️ Delete Domain"):
        if domain_name:
            message = delete_domain(domain_name)
            st.success(message)
        else:
            st.warning("Domain name is required.")
