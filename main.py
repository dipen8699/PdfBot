import streamlit as st
from streamlit_option_menu import option_menu
from modules import account,home,chat,document


st.set_page_config(page_title="PdfBot",page_icon=":material/picture_as_pdf:")

if 'log_in' not in st.session_state:
    st.session_state['log_in'] = False
if 'log_out' not in st.session_state:
    st.session_state['log_out'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''

class PdfBot:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='PdfBot',
                options=['Home','Chat','My Documents','My Account'],
                icons=['house-fill','chat-left-text-fill','files','person-circle'],
                menu_icon='filetype-pdf',
                default_index=0,
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "menu-icon": {"color": "red","font-size":"34px"},
                    "menu-title":{"font-size":"34px", "text-align": "center","font-weight":"bold"},
                    "icon": {"color": "red", "font-size": "22px"}, 
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "black"},
                    "title":{"font-size":"24px"},}
                )

        
        if app == "Home":
            home.home()
        elif app == "Chat":
            chat.chat_screen()   
        elif app == "My Documents":
            document.document()        
        elif app == 'My Account':
            account.account()
  

    run() 