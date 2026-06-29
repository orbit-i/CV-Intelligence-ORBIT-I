"""
ORBIT-I
Home Dashboard
"""

import streamlit as st

from ui.components import (
    hero,
    info_card,
    spacer,
)


def render_home():
    """
    Render Home Dashboard.
    """

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    hero(
    "🚀 ORBIT-I",
    "AI-Powered CV Intelligence & Offer Automation Platform"
)

    st.write(
        """
Welcome to **ORBIT-I**.

This platform streamlines the recruitment process by intelligently
analyzing candidate resumes, extracting structured information,
classifying candidates into relevant domains, and generating
professional offer letters automatically.
"""
    )

    spacer()

    # ------------------------------------------------------
    # Dashboard Cards
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        info_card("Uploaded CVs", "0")

    with col2:
        info_card("Candidates", "0")

    with col3:
        info_card("Generated Offers", "0")

    with col4:
        info_card("Supported Domains", "0")

    spacer(2)

    # ------------------------------------------------------
    # Quick Actions
    # ------------------------------------------------------

    st.subheader("Quick Actions")

    action1, action2 = st.columns(2)

    with action1:

        st.button(
            "📄 Upload Candidate CV",
            use_container_width=True
        )

    with action2:

        st.button(
            "📝 Generate Offer Letter",
            use_container_width=True
        )

    spacer(2)

    # ------------------------------------------------------
    # Workflow
    # ------------------------------------------------------

    st.subheader("System Workflow")

    st.markdown(
        """
1. Upload Candidate CV

2. Extract Candidate Information

3. AI Domain Classification

4. Generate Offer Letter

5. Download Final Document
"""
    )

    spacer()

    # ------------------------------------------------------
    # Features
    # ------------------------------------------------------

    st.subheader("Core Features")

    st.markdown(
        """
- PDF & DOCX Resume Support
- AI-Based Information Extraction
- Candidate Domain Classification
- Automated Offer Letter Generation
- Scalable Modular Architecture
"""
    )