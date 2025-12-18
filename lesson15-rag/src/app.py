import streamlit as st
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate

INDEX_DIR = "faiss_index"

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer ONLY using the provided context. If the answer isn't in the context, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

def format_docs(docs):
    return "\n\n---\n\n".join(d.page_content for d in docs)

st.title("Lesson 15 — RAG (Ollama + LangChain + phi3:mini)")

question = st.text_input("Enter your question:")

if st.button("Answer") and question.strip():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = FAISS.load_local(INDEX_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(question)
    context = format_docs(docs)

    llm = ChatOllama(model="phi3:mini", temperature=0.2)
    messages = PROMPT.format_messages(question=question, context=context)
    answer = llm.invoke(messages)

    st.subheader("Answer")
    st.write(answer.content)

    st.subheader("Retrieved Context")
    st.write(context if context.strip() else "(No context retrieved)")