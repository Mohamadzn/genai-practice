# Lesson 08 – Search & Retrieval Augmented Generation (RAG) with Ollama

This project is part of the **Generative AI for Beginners** course.  
In this lesson, I implemented a **Retrieval Augmented Generation (RAG)** pipeline using **local LLMs with Ollama**, without relying on cloud services or paid APIs.

The goal of this exercise is to understand how RAG works end-to-end:
- Chunking documents
- Creating embeddings
- Retrieving relevant context
- Injecting context into the prompt
- Generating grounded answers

---

## 🧠 What This Project Does

- Reads local documents from a text file
- Splits them into small chunks
- Generates vector embeddings using a local embedding model
- Stores embeddings in a simple JSON-based index
- Retrieves the most relevant chunks using cosine similarity
- Sends retrieved context to a local LLM
- Forces the model to answer **only based on provided documents**

If the answer is not present in the documents, the model responds:
> *"I don't know based on the provided documents."*

---

## 🛠 Tech Stack

- **Python**
- **Ollama** (local LLM runtime)
- **phi3:mini** – lightweight chat model
- **nomic-embed-text** – embedding model
- `requests`
- `python-dotenv`

No cloud services. No API costs.

---

## 📂 Project Structure