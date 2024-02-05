import base64
from config import debug_mode
import streamlit as st

from personality import PERSONALITY_OPTIONS

def build_sidebar():
    with st.sidebar:
        st.image("https://images.squarespace-cdn.com/content/v1/61730a7d9c7a0c57e52d6f0b/2b976baa-1db3-430f-adbe-51ad16482335/MOS-Logo_RGB.png?format=1500w", width=200)

        st.markdown('### Source Documents')
        build_documents()

        build_peronality_selections()

        # if debug_mode and 'messages' in st.session_state:
        #     st.code(st.session_state['messages'])


def build_documents():
    # Can't use this basic link becuase Streamlit sends wrong MIME type: 
    # https://docs.streamlit.io/library/advanced-features/static-file-serving#details-on-usage
    #
    # st.markdown('[Prawn PDF Manual](data/prawn-pdf-manual.pdf)')
    
    download_file_button("prawn-pdf-manual.pdf")
    download_file_button("prawn-table-manual.pdf")


def build_peronality_selections():
    st.selectbox(
        "Personality",
        PERSONALITY_OPTIONS,
        key="selectPersonality"
    )


def download_file_button(filename):
    with open(f"./data/{filename}", "rb") as f:
        file_bytes = f.read()
        # encoded_string = base64.b64encode(file_bytes).decode()
        # download_link = f"data:{mime_type};base64,{encoded_string}"

    st.download_button(
        filename, 
        file_bytes, 
        file_name=filename, 
        mime="application/pdf"
    )
