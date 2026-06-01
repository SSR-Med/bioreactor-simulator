import streamlit as st


def render_section_title(title):
    st.markdown(f'<p class="section-title">{title}</p>', unsafe_allow_html=True)
