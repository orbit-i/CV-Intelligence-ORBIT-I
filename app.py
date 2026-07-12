import streamlit as st

st.set_page_config(
    page_title="ORBIT-I",
    page_icon="🚀",
    layout="wide"
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.switch_page("pages/home.py")