import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/handbook.md"
INDEX_DIR = "faiss_index"

def main():
    # 1) Load
    docs = TextLoader(DATA_PATH, encoding="utf-8").load()
    print("Loaded docs:", len(docs))
    if not docs or not docs[0].page_content.strip():
        raise SystemExit(f"❌ '{DATA_PATH}' is empty or not loaded. Check path and file content.")

    # 2) Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(docs)
    print("Chunks:", len(chunks))
    if not chunks:
        raise SystemExit("❌ No chunks were created. Check your document content.")

    # 3) Embeddings health-check
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    test_vecs = embeddings.embed_documents([chunks[0].page_content])
    if not test_vecs or not test_vecs[0]:
        raise SystemExit("❌ Embeddings returned empty. Make sure Ollama is running and 'nomic-embed-text' is available.")

    # 4) Build FAISS
    db = FAISS.from_documents(chunks, embeddings)

    os.makedirs(INDEX_DIR, exist_ok=True)
    db.save_local(INDEX_DIR)
    print(f"✅ Indexed {len(chunks)} chunks into {INDEX_DIR}")

if __name__ == "__main__":
    main()
