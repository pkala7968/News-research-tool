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

urls= []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_urls= st.sidebar.button("Load URLS")

main_placeholder = st.empty()

#initialize globally 
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

if process_urls:
    #load data
    loader= UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Loading data, please wait...")
    data= loader.load()
    #split data
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        separators=["\n\n", "\n", ".", ","]
    )
    main_placeholder.text("Splitting data into chunks...")
    docs = text_splitter.split_documents(data)
    
    #create vectorstore
    main_placeholder.text("Creating vectorstore...")
    time.sleep(2) 
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    

query = main_placeholder.text_input("Enter your query:")
if query:
    if os.path.exists("faiss_index"):
        vectorindex = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
        )
        chain= RetrievalQAWithSourcesChain.from_llm(
            llm=GoogleGenerativeAI(model="gemini-2.0-flash", api_key=GOOGLE_API_KEY, temperature=0.5, max_output_tokens=250),
            retriever=vectorindex.as_retriever()
        )
        main_placeholder.text("Processing your query...")
        result= chain({"question": query}, return_only_outputs=True)
        main_placeholder.empty()  # Clear the placeholder after processing

        st.subheader("Results:")
        st.write(result['answer'])

        sources= result.get('sources', [])
        if sources:
            st.subheader("Sources:")
            sources_list= sources.split("\n")
            for source in sources_list:
                st.write(source)