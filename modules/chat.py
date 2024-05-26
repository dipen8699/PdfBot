import streamlit as st
from .account import account
import pinecone
from pinecone import Pinecone, ServerlessSpec
# from PdfBot import modules
import time
from modules import InputParsing
# from InputParsing import ChatClass

def select_document():
        # Check if the user is logged in
    if 'user_name' not in st.session_state or not st.session_state['user_name']:
        st.error("Please log in/ Sign Up to use the chat feature.")
        # st.button("Go to Login", on_click=login_page)
        return
    get_docs()
    selected_doc = st.selectbox("Select a document to chat about",options=st.session_state['doc_names'])
    if st.button('Confirm / Clear'):
        st.session_state["select_doc"] = selected_doc

def chat_screen():
    chatclass = InputParsing.ChatClass(st.session_state['OPEN_AI_KEY'], st.session_state["PINECONE_API_KEY"])

    st.title(f'Chat with :red[PdfBot] {st.session_state["user_name"]}')

    selected_doc = st.session_state["select_doc"]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate stream of response with milliseconds delay
            assistant_response = chatclass.getAnswer(prompt, selected_doc)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def get_docs():
    pc = Pinecone(api_key=st.session_state['PINECONE_API_KEY'])
    index = pc.Index("pdfbot")
    doc_names = index.describe_index_stats()
    for name in doc_names["namespaces"].keys():
        get_name = name.split('-')
        if get_name[1] == st.session_state['user_name']:
            st.session_state['doc_names'].append(name.split('-')[0])

def start_chat():
    print('---select doc :',st.session_state["select_doc"])
    if st.session_state["select_doc"] is None:
        select_document()
        st.rerun
    else:
        chat_screen()
