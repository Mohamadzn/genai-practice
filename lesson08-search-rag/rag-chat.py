import os, json, math
import requests
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
CHAT_MODEL = os.getenv('CHAT_MODEL', 'phi3:mini')
EMBED_MODEL = os.getenv('EMBED_MODEL', 'nomic-embed-text')
INDEX_FILE = 'index.json'

def embed(text: str):
    r = requests.post(f'{HOST}/api/embeddings', json={'model': EMBED_MODEL, 'prompt': text}, timeout=300)
    r.raise_for_status()
    return r.json()['embedding']

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)) or 1.0
    nb = math.sqrt(sum(x*x for x in b)) or 1.0
    return dot / (na * nb)

def retrieve(question: str, k: int = 2):
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        items = json.load(f)
    qv = embed(question)
    scored = [(cosine(qv, it['embedding']), it['text']) for it in items]
    scored.sort(reverse=True, key=lambda x: x[0])
    return [t for _, t in scored[:k]]

def ask_llm(context: str, question: str):
    messages = [
        {'role': 'system', 'content': "Answer ONLY using the provided context. If the answer is not in the context, say: I don't know based on the provided documents."},
        {'role': 'user', 'content': f"Context:\n{context}\n\nQuestion:\n{question}"}
    ]
    r = requests.post(f'{HOST}/api/chat', json={'model': CHAT_MODEL, 'messages': messages, 'stream': False}, timeout=300)
    r.raise_for_status()
    return r.json()['message']['content']

def main():
    print('✅ Lesson 08 – RAG Search (Ollama)')
    print(\"Type 'exit' to quit.\\n\")
    while True:
        q = input('Question: ').strip()
        if q.lower() == 'exit':
            break
        ctx_chunks = retrieve(q, k=2)
        context = '\\n'.join(ctx_chunks)
        ans = ask_llm(context, q)
        print('\\n--- Retrieved Context ---')
        print(context)
        print('--- Answer ---')
        print(ans)
        print('-------------------------\\n')

if __name__ == '__main__':
    main()