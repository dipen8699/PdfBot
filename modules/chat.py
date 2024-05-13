import streamlit as st
from .account import account

def chat_screen():
    # Check if the user is logged in
    if 'user_name' not in st.session_state or not st.session_state['user_name']:
        st.warning("Please log in to use the chat feature.")
        st.button("Go to Login", on_click=login_page)
        return
    
    st.title(f'Chat with :red[PdfBot] {st.session_state["user_name"]}')


    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask me a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
   
        with st.chat_message("user"):
            st.markdown(prompt)

def login_page():
    account()
