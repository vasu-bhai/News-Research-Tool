from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model="llama3.2:1b", temperature=0.2)

context = """
The city is located 284 km (176 mi) south of the state capital, Gandhinagar; 265 km (165 mi) south of Ahmedabad; and 289 km (180 mi) north of Mumbai. The city centre is located on the Tapti River (popularly known as Tapi), close to the Arabian Sea.[16]
"""

question = "which city in the western Indian state of Gujarat?"

# Using the exact prompt template that RetrievalQAWithSourcesChain uses by default
prompt = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
If you don't know the answer, just say that you don't know. Don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.

QUESTION: {question}
=========
{summaries}
=========
FINAL ANSWER:"""

formatted_prompt = prompt.format(question=question, summaries=context)
print(llm.invoke(formatted_prompt).content)
