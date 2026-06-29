"""
ORBIT-I
Reusable UI Components
"""

from pathlib import Path

import streamlit as st


# ==========================================================
# LOAD GLOBAL CSS
# ==========================================================

def load_css():
    """
    Load global stylesheet.
    """

    css_file = Path("assets/styles.css")

    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as file:
            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )


# ==========================================================
# PAGE HEADER
# ==========================================================

def page_header(title: str, subtitle: str = ""):
    """
    Display page title and subtitle.
    """

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()


# ==========================================================
# SECTION TITLE
# ==========================================================

def section_title(title: str):
    """
    Display section heading.
    """

    st.markdown(f"## {title}")


# ==========================================================
# INFO CARD
# ==========================================================

def info_card(title: str, value: str):
    """
    Display dashboard KPI card.
    """

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# SPACER
# ==========================================================

def spacer(height: int = 1):
    """
    Add vertical spacing.
    """

    for _ in range(height):
        st.write("")


# ==========================================================
# FOOTER
# ==========================================================

def footer():
    """
    Display application footer.
    """

    st.markdown("---")

    st.markdown(
        """
        <div class="footer">
            © 2026 ORBIT-I • CV Intelligence & Offer Automation Platform
        </div>
        """,
        unsafe_allow_html=True
    )
# ==========================================================
# HERO SECTION
# ==========================================================

def hero(title: str, subtitle: str):
    """
    Display application hero section.
    """

    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )