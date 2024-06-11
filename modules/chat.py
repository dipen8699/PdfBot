import streamlit as st
from .account import account
import pinecone
from pinecone import Pinecone, ServerlessSpec
# from PdfBot import modules
import time
from modules import InputParsing
from translate import Translator
from langdetect import detect

languages = {
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'tl': 'Filipino',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ko': 'Korean',
    'ku': 'Kurdish (Kurmanji)',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'or': 'Odia (Oriya)',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu',
}


# from InputParsing import ChatClass

def select_document():
    if 'user_name' not in st.session_state or not st.session_state['user_name']:
        st.error("Please log in/ Sign Up to use the chat feature.")
        return
    get_docs()
    selected_doc = st.selectbox("Select a document to chat about",options=st.session_state['doc_names'])
    if st.button('Confirm / Clear'):
        st.session_state["select_doc"] = selected_doc

def chat_screen():
    chatclass = InputParsing.ChatClass(st.session_state['OPEN_AI_KEY'], st.session_state["PINECONE_API_KEY"])

    st.title(f'Chat with :red[PdfBot] {st.session_state["user_name"]}')

    selectModel = st.selectbox(label='Select Model', options=['GPT-4', 'Llama'])
    selectLanguage = st.selectbox(
        label='Select Language',
        options=list(languages.keys()),
        format_func=lambda x: languages[x]
    )

    if selectModel == 'GPT-4':
        selected_doc = st.session_state["select_doc"]

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("What is up?"):
            # Detect the language of the user message
            detected_language = detect(prompt)

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get assistant response in English
            assistant_response = chatclass.getAnswer(prompt, selected_doc)

            # Translate the bot's response to the selected language
            translator = Translator(to_lang=selectLanguage)
            translated_response = translator.translate(assistant_response)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                # Simulate stream of response with milliseconds delay
                for chunk in translated_response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    elif selectModel == 'Llama':
        st.title('Coming Soon')

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


# import streamlit as st
# from .account import account
# import pinecone
# from pinecone import Pinecone, ServerlessSpec
# import time
# from modules import InputParsing
# from googletrans import Translator

# # Initialize the translator
# translator = Translator()

# def select_document():
#     if 'user_name' not in st.session_state or not st.session_state['user_name']:
#         st.error("Please log in/ Sign Up to use the chat feature.")
#         return
#     get_docs()
#     selected_doc = st.selectbox("Select a document to chat about", options=st.session_state['doc_names'])
#     if st.button('Confirm / Clear'):
#         st.session_state["select_doc"] = selected_doc

# def chat_screen():
#     chatclass = InputParsing.ChatClass(st.session_state['OPEN_AI_KEY'], st.session_state["PINECONE_API_KEY"])

#     st.title(f'Chat with :red[PdfBot] {st.session_state["user_name"]}')

#     selectModel = st.selectbox(label='Select Model', options=['GPT-4', 'Llama'])

#     if selectModel == 'GPT-4':
#         selected_doc = st.session_state["select_doc"]

#         if "messages" not in st.session_state:
#             st.session_state.messages = []

#         # Display chat messages from history on app rerun
#         for message in st.session_state.messages:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         if prompt := st.chat_input("What is up?"):
#             # Detect the language of the user message
#             detected_language = translator.detect(prompt).lang

#             # Add user message to chat history
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             # Display user message in chat message container
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             # Get assistant response in English
#             assistant_response = chatclass.getAnswer(prompt, selected_doc)

#             # Translate the bot's response to the detected language
#             translated_response = translator.translate(assistant_response, dest=detected_language).text

#             # Display assistant response in chat message container
#             with st.chat_message("assistant"):
#                 message_placeholder = st.empty()
#                 full_response = ""
#                 # Simulate stream of response with milliseconds delay
#                 for chunk in translated_response.split():
#                     full_response += chunk + " "
#                     time.sleep(0.05)
#                     # Add a blinking cursor to simulate typing
#                     message_placeholder.markdown(full_response + "▌")
#                 message_placeholder.markdown(full_response)
#             # Add assistant response to chat history
#             st.session_state.messages.append({"role": "assistant", "content": full_response})

#     elif selectModel == 'Llama':
#         st.title('Coming Soon')

# def get_docs():
#     pc = Pinecone(api_key=st.session_state['PINECONE_API_KEY'])
#     index = pc.Index("pdfbot")
#     doc_names = index.describe_index_stats()
#     for name in doc_names["namespaces"].keys():
#         get_name = name.split('-')
#         if get_name[1] == st.session_state['user_name']:
#             st.session_state['doc_names'].append(name.split('-')[0])

# def start_chat():
#     print('---select doc :', st.session_state["select_doc"])
#     if st.session_state["select_doc"] is None:
#         select_document()
#         st.rerun()
#     else:
#         chat_screen()

