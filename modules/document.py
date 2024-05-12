import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials,auth
from dotenv import load_dotenv, dotenv_values
import os
import time

def document():
    st.title(f'Welcome to :red[PdfBot] {st.session_state['user_name']}')
    build_doc_ui()


def doc_navbar() -> None:
    """
    Creates the side navigaton bar
    """
    main_navbar = st.empty()
    with main_navbar:
        selected = option_menu(
            menu_title=None,
            default_index=0,
            options=['Documents','Upload Document'],
            icons=['file-earmark-pdf','file-earmark-arrow-up',],
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "red", "font-size": "18px"}, 
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px","--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "black"},
                "nav-item":{"margin-left":"10px","margin-right":"10px"}
            }
        )
        return selected

def upload_doc() -> None:
    docs = st.file_uploader("Upload documents", accept_multiple_files=True)
    if st.button("Upload"):
        with st.status("Uploading data...", expanded=True) as status:
            st.write("Fetching data...")
            time.sleep(3)
            st.write("Splitting data...")
            time.sleep(2)
            st.write("Embedding data...")
            time.sleep(2)
            st.write("storing data...")
            time.sleep(2)
            status.update(label="Upload complete!", state="complete", expanded=False)

def build_doc_ui():
    if st.session_state['log_in'] == False:
        st.error("Please Login/SignUp to check and Upload Documents")
    else:
        selected = doc_navbar()

        if selected == "Upload Document":
            upload_doc()
