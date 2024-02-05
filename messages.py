import streamlit as st

def add_chat_message(message):
    with st.chat_message(message["role"]):
        st.write(message["content"])
    st.session_state.messages.append(message)

def ai_conversation_messages():
    [m for m in st.session_state.messages if m['local'] != True]
    
    
def build_messages():
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "results" in message:
                st.dataframe(message["results"])
