from config import debug_mode
import streamlit as st

def build_sidebar():
    with st.sidebar:
        st.image("https://images.squarespace-cdn.com/content/v1/61730a7d9c7a0c57e52d6f0b/2b976baa-1db3-430f-adbe-51ad16482335/MOS-Logo_RGB.png?format=1500w", width=200)
        if debug_mode and 'debug_data' in st.session_state:
            st.code(st.session_state['debug_data'], language='json')

        st.markdown('### Source Documents')
        st.write('[TODO List docs here]')