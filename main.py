import streamlit as st
from streamlit_option_menu import option_menu
from modules import account, home, chat, document
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

st.set_page_config(page_title="PdfBot", page_icon=":material/picture_as_pdf:")

if 'log_in' not in st.session_state:
    st.session_state['log_in'] = False
if 'log_out' not in st.session_state:
    st.session_state['log_out'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''
if 'doc_names' not in st.session_state:
    st.session_state['doc_names'] = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "select_doc" not in st.session_state:
    st.session_state["select_doc"] = None

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate('modules/service_acnt.json')  
    firebase_admin.initialize_app(cred)

class PdfBot:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        load_dotenv()
        st.session_state['OPEN_AI_KEY'] = os.getenv("OPEN_AI_KEY")
        st.session_state["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
        st.session_state['doc_names'] = []
        with st.sidebar:
            app = option_menu(
                menu_title='PdfBot',
                options=['Home', 'Chat', 'My Documents', 'My Account'],
                icons=['house-fill', 'chat-left-text-fill', 'files', 'person-circle'],
                menu_icon='filetype-pdf',
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "menu-icon": {"color": "red", "font-size":"34px"},
                    "menu-title": {"font-size":"34px", "text-align": "center", "font-weight":"bold"},
                    "icon": {"color": "red", "font-size": "22px"},
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "black"},
                    "title": {"font-size":"24px"}
                }
            )

        if app == "Home":
            home.home()
        elif app == "Chat":
            chat.start_chat()
        elif app == "My Documents":
            document.document()
        elif app == 'My Account':
            account.account()

    run()

