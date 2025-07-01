import os
import streamlit as st
import pickle
import time
import langchain
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources  import load_qa_with_sources_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.title("News Research Tool 📈")
st.sidebar.title("News URLs")

for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")

process_urls= st.sidebar.button("Load URLS")

if process_urls:
    pass