import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.audit_logger import log_event, get_all_logs, export_to_csv, init_audit_log

st.set_page_config(page_title="ORBIT-I | Audit Log", page_icon="📋", layout="wide")

init_audit_log()

st.title("📋 Audit Log")
st.write("Complete record of all CV processing activity")

st.divider()

# Test event add karne ka button
with st.expander("➕ Add Test Log Entry"):
    col1, col2 = st.columns(2)
    with col1:
        cv_name = st.text_input("CV Filename", placeholder="example_cv.pdf")
        domain = st.text_input("Domain Assigned", placeholder="Software Engineering")
        score = st.number_input("Confidence Score", min_value=0, max_value=100, value=85)
    with col2:
        status = st.selectbox("Offer Status", ["Generated", "Flagged for Review", "Pending", "Manually Edited"])
        edited_by = st.text_input("Edited By", value="System")
        notes = st.text_area("Notes", placeholder="Any additional notes...")

    if st.button("💾 Save Log Entry"):
        if cv_name and domain:
            log_event(cv_name, domain, score, status, edited_by, notes)
            st.success("✅ Log entry saved successfully!")
            st.rerun()
        else:
            st.warning("CV filename and domain are required.")

st.divider()

# Logs display
logs = get_all_logs()

if logs:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(logs))
    with col2:
        flagged = sum(1 for log in logs if "Flagged" in str(log[5]))
        st.metric("Flagged CVs", flagged)
    with col3:
        generated = sum(1 for log in logs if "Generated" in str(log[5]))
        st.metric("Offers Generated", generated)

    st.divider()

    st.subheader("📊 Log Records")

    import pandas as pd
    df = pd.DataFrame(logs, columns=["ID", "Timestamp", "CV File", "Domain", "Score", "Status", "Edited By", "Notes"])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    if st.button("📥 Export to CSV"):
        path = export_to_csv()
        st.success(f"✅ Exported successfully: {path}")

else:
    st.info("No log entries yet. Logs will appear here as CVs are processed.")