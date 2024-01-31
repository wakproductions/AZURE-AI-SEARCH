import os
import argparse
import glob
import html
import io
import re
import time
from pypdf import PdfReader, PdfWriter
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import *
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure_openai import *
from config import *
from messages import build_messages
from sidebar import build_sidebar
import streamlit as st

def initialize():
    st.session_state.messages = []

initialize()
build_sidebar()

st.header('GPT4 with Custom Document Repository')

build_messages()

user_input = st.chat_input('Enter your question here:')

if user_input:
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

    st.session_state['debug_data'] = results
    content = "\n".join(results)

    references =[]
    for result in results:
        references.append(result.split(":")[0])
    st.markdown("### References:")
    breakpoint()
    st.write(" , ".join(set(references)))

    conversation=[{"role": "system", "content": "You are a technical AI assistant. Answer every question like a grumpy New Yorker."}]
    prompt = create_prompt(content,user_input)            
    print("Prompt: {}", prompt)
    print("-------------------")

    conversation.append({"role": "assistant", "content": prompt})
    conversation.append({"role": "user", "content": user_input})
    reply = generate_answer(conversation)
    print("Conversation: {}", conversation)
    print("-------------------")

    st.markdown("### Answer is:")
    st.write(reply)

