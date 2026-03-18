import os
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQAWithSourcesChain

llm = ChatOllama(model="llama3.2:1b", temperature=0.2)
embeddings = OllamaEmbeddings(model="llama3.2:1b")
file_path = "faiss_store_ollama"

if os.path.exists(file_path):
    vectorstore = FAISS.load_local(
        file_path, 
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    docs = vectorstore.similarity_search("which city in the western Indian state of Gujarat?")
    print("--- FIRST RETRIEVED DOC (TOP) ---")
    if docs:
        print(docs[0].page_content[:1500])
        print("Metadata:", docs[0].metadata)
    else:
        print("No documents found for query!")
    
    print("\n--- TEST CHAIN ---")
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    result = chain.invoke({"question": "which city in the western Indian state of Gujarat?"})
    print("Answer:", result.get("answer"))
    print("Sources:", result.get("sources"))
else:
    print("No FAISS index found")
