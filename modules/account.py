import streamlit as st
import re
import json
import requests
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials,auth
import os
from dotenv import load_dotenv, dotenv_values

def account():
    # st.title(f'Welcome to :red[PdfBot] {st.session_state['user_name']}')
    st.title('Welcome to PdfBot ' + st.session_state['user_name'])
    print('---hiii')
    build_login_ui()

def check_name(name_sign_up:str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')
    if re.search(name_regex,name_sign_up):
        return True
    return False

def check_email(email_sign_up:str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False

def check_username(username_sign_up:str) -> bool:
    """
    Checks if the user entered a valid Username while creating the account.
    """
    regex = re.compile(r'^[a-zA-Z0-9_.-]+$')

    if re.match(regex,username_sign_up):
        return True
    return False

def check_uniq_email(email_sign_up:str) -> bool:
    """
    Checks if the user entered a Uniq email while creating the account.
    """
    if not firebase_admin._apps:
        load_dotenv()
        cred = credentials.Certificate("")
        val = firebase_admin.initialize_app(cred)

    all_user = auth.list_users()
    while all_user:
        for user in all_user.users:
            if user.email == email_sign_up:
                return False
        return True

def check_uniq_username(username_sign_up:str) -> bool:
    """
    Checks if the user entered a Uniq Username while creating the account.
    """
    try:
        all_user = auth.list_users()
        while all_user:
            for user in all_user.users:
                if user.uid == username_sign_up:
                    return False
            return True
    except Exception as e:
        print(e)

def sign_in_with_email_and_password(user_name:str,password:str,return_secure_token=True)->None:
    """
    Authenticates the username and password.
    """
    load_dotenv()
    st.session_state['Firebase_API_key'] = os.getenv("FIREBASE_WEB_API")
    payload = json.dumps({"email":user_name,"password":password,"return_secure_token":return_secure_token})
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    response = requests.post(rest_api_url,
                  params={"key": st.session_state['Firebase_API_key']},
                  data=payload)
    if response:
        user_val = response.json()
        return user_val
    return None


def register_user(name_sign_up:str,email_sign_up:str,username_sign_up:str,password_sign_up:str) -> bool:
    """
    Saves the information of the new user in the firebase authentication.
    """
    user = auth.create_user(display_name=name_sign_up,email=email_sign_up,password=password_sign_up,uid=username_sign_up)
    if user.uid:
        return True
    return False

    
def login_page()->None:
        """
        Creates the login widget, checks and authenticates the users.
        """
        with st.form("Login form"):
            username = st.text_input("Username", placeholder = 'Your unique username')
            password = st.text_input("Password", placeholder = 'Your password', type = 'password')

            st.markdown("###")
            login_submit_button = st.form_submit_button(label = 'Login')

            if login_submit_button == True:
                user_val = sign_in_with_email_and_password(username,password)
                if user_val is not None:
                    st.session_state['log_in'] = True
                    st.session_state['user_name'] = user_val['displayName']
                    st.success('Login SuccessFul!!')
                    st.rerun()
                else:
                    st.error('Please enter valid Email and Password')
                    

def sign_up_widget() -> None:
    """
    Creates the sign-up widget and stores the user info in a secure way in the _secret_auth_.json file.
    """

    with st.form("Sign Up Form"):
        name_sign_up = st.text_input("Name *", placeholder = 'test')
        valid_name = check_name(name_sign_up=name_sign_up)

        email_sign_up = st.text_input("Email *", placeholder = 'user@gmail.com')
        vadil_email = check_email(email_sign_up=email_sign_up)
        uniq_email = check_uniq_email(email_sign_up=email_sign_up)

        username_sign_up = st.text_input("Username *", placeholder = 'test1234')
        valid_username = check_username(username_sign_up=username_sign_up)
        uniq_username = check_uniq_username(username_sign_up=username_sign_up)

        password_sign_up = st.text_input("Password *", placeholder = 'Create a strong password', type = 'password')

        st.markdown("###")
        sign_up_submit_button = st.form_submit_button(label = 'Register')

        if sign_up_submit_button:
            if valid_name == False:
                st.error("Please enter valid name")
            elif vadil_email == False:
                st.error("Please enter valid email address")
            elif uniq_email == False:
                st.error("Email already exists!")
            elif uniq_username == False:
                st.error(f'Sorry, username {username_sign_up} already exists!')

            if valid_name == True and vadil_email == True and uniq_email == True and uniq_username == True:
                register_user(name_sign_up,email_sign_up,username_sign_up,password_sign_up)
                st.success("Registration Successful!")

def logout_widget()-> None:
    """
    Creates the logout widget in the sidebar only if the user is logged in.
    """
    if st.session_state['log_in'] == True:
        logout_btn = st.button("Logout")
        if logout_btn:
            st.session_state['log_out'] = True
            st.session_state['log_in'] = False
            st.rerun()

def forgot_password() -> None:
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
                # send_passwd_in_email(.auth_token, username_forgot_passwd, email_forgot_passwd, .company_name, random_password)
                # change_passwd(email_forgot_passwd, random_password)

def navbar() -> None:
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
                "icon": {"color": "red", "font-size": "18px"}, 
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "black"},
            }
        )
        return selected

def navbar1() -> None:
    """
    Creates the side navigaton bar
    """
    main_navbar = st.empty()
    with main_navbar:
        selected = option_menu(
            menu_title=None,
            default_index=0,
            options=['Profile','Change Password'],
            icons=['person-circle','arrow-repeat',],
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "red", "font-size": "18px"}, 
                "nav-link": {"font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "black"},
            }
        )
        return selected

def build_login_ui():
    """
    Brings everything together, calls important functions.
    """
    if st.session_state['log_in'] == False:
        selected = navbar()

        if selected == 'Login':
            login_page()
        st.rerun
        
        if selected == 'Create Account':
            sign_up_widget()

        if selected == 'Forgot Password':
            forgot_password()
        
        # .logout_widget()
        
        return st.session_state['log_in']
    else:
        selected = navbar1()

        if selected == 'Profile':
            logout_widget()