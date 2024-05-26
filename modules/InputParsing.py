import os 
import pinecone
import re
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st
# from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from pinecone import Pinecone, ServerlessSpec


class ChatClass:
    def __init__(self, openAIKey, pineConeKey) -> None:
        self.OpenAIkey = openAIKey
        self.pineConeKey = pineConeKey
        # Initialize Pinecone instance with the provided API key
        self.pinecone_instance = Pinecone(api_key=pineConeKey)

        if 'pdfbot' not in self.pinecone_instance.list_indexes().names():
            self.pinecone_instance.create_index(
                name='pdfbot',
                dimension=1536,
                metric='euclidean',
                spec=ServerlessSpec(cloud='aws', region='us-west-2')
            )
        self.initiateModel()

    def generateBaseQuestion(self, userQuestion):
        basePrompt = "You are a advanced Document Q and A agent that answers user queries \
        based on information provided in a speicific document. Currently the user has \
        asked a question, possibly, this is not the first question that the user has asked to you. \
        You will be provided a chat history between the user and responses generated by system along \
        the current question posted by user. You need to combine the chat history and the current question \
        and generate a single question only and then find the answer of that question based on the information of the provided document.\n \n "

        if(len(self.bufw_history) == 0):
            self.bufw_history = "No History Available "

        chatHistoryPrompt = f"Chat History : \n \n {self.bufw_history}"

        userQuestionPrompt = f"User Question : \n \n {userQuestion}"

        prompt = basePrompt + chatHistoryPrompt + userQuestionPrompt

        # Generate the answer
        generatedQuestion = self.conversation_sum_bufw(prompt)

        return generatedQuestion['response']
    
    def sanitizeFileName(self, filename):
        filename_lower = filename.lower()
        sanitized_filename = re.sub(r'[^a-z0-9\.]', '', filename_lower)
        return sanitized_filename + '-' + st.session_state['user_name']

    def findRelevantSources(self, generatedQuestion, documentNameSpace):
        embeddingModel = OpenAIEmbeddings(openai_api_key = self.OpenAIkey)
        embeddings = embeddingModel.embed_documents([generatedQuestion])
        embeddings = embeddings[0]
        sanitized_filename = self.sanitizeFileName(documentNameSpace)

        index = self.pinecone_instance.Index("pdfbot")
        relevantSources = index.query(vector=embeddings, top_k=3,include_metadata=True, namespace=sanitized_filename)
        
        sources = ""
        for source in relevantSources['matches']:
            sources = sources + source['metadata']['values'] + "\n \n"

        return sources


    def generateAnswer(self, sources, generatedQuestion):
        secondBasePrompt = "You will be asked a question and will be provided relevant document snippets. \
        I want you to read the document snippets and answer the question based on the document snippets provided.\
        When asked to write programming code, you utilize your trained knowledge to provide accurate code solutions based on your programming expertise \n \n"

        documentPrompt = f"Document Snippets : \n \n {sources}"
        questionPrompt = f"Question : \n \n {generatedQuestion}"

        secondPrompt = secondBasePrompt + documentPrompt + questionPrompt

        generatedAnswer = self.conversation_sum_bufw(secondPrompt)

        return (generatedAnswer['response'])
    
    def initiateModel(self):
        try:
            model = ChatOpenAI(openai_api_key=self.OpenAIkey, model_name="gpt-4")
            self.conversation_sum_bufw = ConversationChain(llm=model, memory=ConversationSummaryBufferMemory(llm=model, max_token_limit=650))
            self.bufw_history = self.conversation_sum_bufw.memory.load_memory_variables(inputs=[])['history']
        except Exception as e:
            print(f"There was an error in initiating the model: {str(e)}")

    def getAnswer(self, textInput, documentNameSpace):
        baseQuestion = self.generateBaseQuestion(textInput)
        relevantSources = self.findRelevantSources(baseQuestion, documentNameSpace)
        answer = self.generateAnswer(relevantSources, baseQuestion)
        return answer

