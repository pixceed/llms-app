import streamlit as st

from src.components.sidebar import sidebar_view



def main():
    st.set_page_config(layout='wide', page_title="LLMS-APP", page_icon="👾")
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    sidebar_view()

    st.markdown("# LLMS-APP")


if __name__ == '__main__':
    main()