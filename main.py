import os
import streamlit as st
import pickle
import time

from dotenv import load_dotenv
load_dotenv()

# NEW IMPORTS (OLLAMA)
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQAWithSourcesChain

# UI
st.title("ChatBot: News Research Tool 📈")
st.sidebar.title("News Article URLs")

# Input URLs
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_groq"

main_placeholder = st.empty()

# 🔥 CLOUD LLM (FAST & LIGHTWEIGHT FOR DEPLOYMENT)
llm = ChatGroq(
    model="llama-3.1-8b-instant", 
    temperature=0.2
)

# Process URLs
if process_url_clicked and urls:
    loader = WebBaseLoader(
        web_paths=urls,
        header_template={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    )

    main_placeholder.text("Data Loading...Started...✅")
    data = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    main_placeholder.text("Text Splitting...Started...✅")
    docs = text_splitter.split_documents(data)
    main_placeholder.text("Text Splitting...Done...✅")

    # 🔥 LOCAL FAST EMBEDDINGS (HuggingFace CPU)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(docs, embeddings)

    main_placeholder.text("Embedding + FAISS Index Created...✅")
    time.sleep(1)

    # Save index
    vectorstore.save_local(file_path)

    st.success("Processing Complete!")

# Query input
query = st.text_input("Ask a Question:")

if query:
    if os.path.exists(file_path):
        vectorstore = FAISS.load_local(
            file_path, 
            HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
            allow_dangerous_deserialization=True
        )

        from langchain_core.prompts import PromptTemplate
        
        template = """You are a helpful assistant. Use the following pieces of context to answer the user's question.
If the context contains the answer, extract it. If it doesn't, just say you don't know.
ALWAYS include the source URL exactly as provided.

Context: {summaries}

Question: {question}

Answer with Sources:"""
        PROMPT = PromptTemplate(template=template, input_variables=["summaries", "question"])

        chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": PROMPT}
        )

        result = chain.invoke({"question": query})

        st.header("Answer")
        st.write(result["answer"])

        # Sources
        sources = result.get("sources", "")
        if sources:
            st.subheader("Sources:")
            for source in sources.split("\n"):
                st.write(source)
    else:
        st.error("Please process URLs first!")