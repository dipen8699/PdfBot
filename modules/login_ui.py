import streamlit as st
import time
from streamlit_option_menu import option_menu

class LoginPage:
    def __init__(self,hide_menu_bool: bool = False, hide_footer_bool: bool = False):
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool

    def login_page(self)->None:
        """
        Creates the login widget, checks and authenticates the users.
        """

        if st.session_state['log_in'] == False:
            st.session_state['log_out'] == True

        login = st.empty()
        with login.form("Login form"):
            username = st.text_input("Username", placeholder = 'Your unique username')
            password = st.text_input("Password", placeholder = 'Your password', type = 'password')

            st.markdown("###")
            login_submit_button = st.form_submit_button(label = 'Login')

            if login_submit_button == True:
                st.session_state['log_in'] = True
                login.empty()
                st.rerun()

    def sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in the _secret_auth_.json file.
        """

        with st.form("Sign Up Form"):
            name_sign_up = st.text_input("Name *", placeholder = 'test')
            valid_name = check_name(name_sign_up=name_sign_up)

            email_sign_up = st.text_input("Email *", placeholder = 'user@gmail.com')
            vadil_email = check_email(email_sign_up=email_sign_up)

            username_sign_up = st.text_input("Username *", placeholder = 'test@1234')

            password_sign_up = st.text_input("Password *", placeholder = 'Create a strong password', type = 'password')

            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label = 'Register')

            if sign_up_submit_button:
                if valid_name == False:
                    st.error("Please enter valid name")
                elif vadil_email == False:
                    st.error("Please enter valid email address")

                if valid_name == True and vadil_email == True:
                    register_user(name_sign_up,email_sign_up,username_sign_up,password_sign_up)
                    st.success("Registration Successful!")
    
    def forgot_password(self) -> None:
        """
        Creates the forgot password widget and after user authentication (email), triggers an email to the user 
        containing a random password.
        """
        with st.form("Forgot Password Form"):
            email_forgot_passwd = st.text_input("Email", placeholder= 'Please enter your email')

            st.markdown("###")
            forgot_passwd_submit_button = st.form_submit_button(label = 'Get Password')

            if forgot_passwd_submit_button:
                st.success("Secure Password Sent Successfully!")
                # if email_exists_check == False:
                #     st.error("Email ID not registered with us!")

                # if email_exists_check == True:
                    # random_password = generate_random_passwd()
                    # send_passwd_in_email(self.auth_token, username_forgot_passwd, email_forgot_passwd, self.company_name, random_password)
                    # change_passwd(email_forgot_passwd, random_password)

    # def logout_widget(self) -> None:
    #     """
    #     Creates the logout widget in the sidebar only if the user is logged in.
    #     """
    #     if st.session_state['log_in'] == True:
    #         del_logout = st.sidebar.empty()
    #         del_logout.markdown("#")
    #         logout_click_check = del_logout.button("Logout")

    #         if logout_click_check == True:
    #             st.session_state['log_out'] = True
    #             st.session_state['log_in'] = False
    #             del_logout.empty()
    #             st.rerun()

    def hide_menu(self) -> None:
        """
        Hides the streamlit menu situated in the top right.
        """
        st.markdown(""" <style>
        #MainMenu {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    def hide_footer(self) -> None:
        """
        Hides the 'made with streamlit' footer.
        """
        st.markdown(""" <style>
        footer {visibility: hidden;}
        </style> """, unsafe_allow_html=True)

    def navbar(self) -> None:
        """
        Creates the side navigaton bar
        """
        main_navbar = st.empty()
        with main_navbar:
            selected = option_menu(
                menu_title=None,
                default_index=0,
                options=['Login','Create Account','Forgot Password'],
                icons=['key','person-plus','question'],
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "18px"}, 
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "black"},
                }
            )
            return selected

    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """

        selected = self.navbar()

        if selected == 'Login':
            self.login_page()
        
        if selected == 'Create Account':
            self.sign_up_widget()

        if selected == 'Forgot Password':
            self.forgot_password()
        
        # self.logout_widget()

        if st.session_state['log_in'] == True:
            st.sidebar.empty()
        
        if self.hide_menu_bool == True:
            self.hide_menu()
        
        if self.hide_footer_bool == True:
            self.hide_footer()
        
        return st.session_state['log_in']
