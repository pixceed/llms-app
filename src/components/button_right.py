import streamlit as st

def align_button_right():
    button_css = f"""
    <style>
    div.stButton > button:first-child {{
        float: right;
    }}
    </style>
    """
    st.markdown(button_css, unsafe_allow_html=True)