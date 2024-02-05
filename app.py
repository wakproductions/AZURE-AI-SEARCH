import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import *
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure_openai import *
from config import *
from messages import add_chat_message, ai_conversation_messages, build_messages
from personality import personality_system_prompt
from sidebar import build_sidebar
import streamlit as st

def initialize():
    if "messages" not in st.session_state: 
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Welcome to the document repository assistant. Enter a question about the document library below and I will try to answer it."
        }]

def perform_references_search():
    service_name = "YOUR-SEARCH-SERVICE-NAME"
    service_name = searchservice
    key = "YOUR-SEARCH-SERVICE-ADMIN-API-KEY"
    key = searchkey

    # We are using the Python client, but this can be done using raw requests on the endpoint too:
    # https://learn.microsoft.com/en-us/rest/api/searchservice/search-documents
    # https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python
    endpoint = "https://{}.search.windows.net/".format(searchservice)
    index_name = index

    azure_credential =  AzureKeyCredential(key)

    search_client = SearchClient(endpoint=endpoint, index_name=index_name, credential=azure_credential)

    # TODO replace with proper environment variables loading
    KB_FIELDS_CONTENT = os.environ.get("KB_FIELDS_CONTENT") or "content"
    KB_FIELDS_FILEPATH = os.environ.get("KB_FIELDS_FILEPATH") or "filepath"

    exclude_category = None

    print("Searching:", user_input)
    print("-------------------")
    filter = "category ne '{}'".format(exclude_category.replace("'", "''")) if exclude_category else None
    r = search_client.search(user_input, 
                            filter=filter,
                            query_type=QueryType.SEMANTIC, 
                            query_language="en-us", 
                            query_speller="lexicon", 
                            semantic_configuration_name="default", 
                            top=3)
    
    results = [doc[KB_FIELDS_FILEPATH] + ": " + doc[KB_FIELDS_CONTENT].replace("\n", "").replace("\r", "") for doc in r]
    rag_content = "\n".join(results)

    references =[]
    for result in results:
        references.append(result.split(":")[0])
    references_message_text = f"References: {' , '.join(set(references))}"
    add_chat_message({ "role": "ai", "content": references_message_text })

    return rag_content



initialize()
build_sidebar()

st.header('GPT4 with Custom Document Repository')

build_messages()

user_input = st.chat_input('Enter your question here:')

if user_input:
    user_message = {"role": "user", "content": user_input}
    add_chat_message(user_message)

    conversation = [{"role": "system", "content": personality_system_prompt()}]
    if st.session_state["selectPersonality"] != "Default Personality":
        add_chat_message({"role": "assistant", "content": f"Personality: {st.session_state['selectPersonality']}"})

    rag_content = perform_references_search()

    prompt = create_prompt(rag_content,user_input)            
    print("Prompt: {}", prompt)
    print("-------------------")

    conversation.append({"role": "assistant", "content": prompt})

    conversation.append(user_message)

    reply = generate_answer(conversation)
    print("Conversation: {}", conversation)
    print("-------------------")

    add_chat_message({ "role": "assistant", "content": reply})



