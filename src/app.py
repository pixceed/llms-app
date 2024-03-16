import shutil
from pathlib import Path
import streamlit as st

from components.sidebar import sidebar_view


def move_font_files():
    STREAMLIT_STATIC_PATH = Path(st.__path__[0]) / "static"
    CSS_PATH = STREAMLIT_STATIC_PATH / "assets/fonts/"
    if not CSS_PATH.is_dir():
        CSS_PATH.mkdir()

    css_file = CSS_PATH / "Nosutaru-dotMPlusH-10-Regular.ttf"
    if not css_file.exists():
        shutil.copy("src/fonts/Nosutaru-dotMPlusH-10-Regular.ttf", css_file)

def main():
    # move_font_files()
    st.set_page_config(layout='wide', page_title="LLMS-APP", page_icon="👾")
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    with open( "src/style.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


    sidebar_view()

    st.write("<span style='font-size:50px;font-weight:bold'>👾 LLMS-APP</span>",  unsafe_allow_html=True)

    # if st.button("Move font files"):
    #    move_font_files()


if __name__ == '__main__':
    main()