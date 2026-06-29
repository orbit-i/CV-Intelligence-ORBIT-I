import streamlit as st

from config.settings import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
)

from ui.components import (
    load_css,
    footer,
)

from ui.home import render_home


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
)

load_css()

render_home()

footer()