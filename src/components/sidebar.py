import streamlit as st


def sidebar_view():
    with st.sidebar:
        st.page_link("app.py", label="HOME", icon="👾")
        st.page_link("pages/simple_chat2.py", label="CHAT", icon="💬")