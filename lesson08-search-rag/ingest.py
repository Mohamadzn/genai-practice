import os, json, math
import requests
from dotenv import load_dotenv

load_dotenv()
HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
EMBED_MODEL = os.getenv('EMBED_MODEL', 'nomic-embed-text')
DATA_FILE = os.path.join('data', 'documents.txt')
OUT_FILE = 'index.json'

def embed(text: str):
    r = requests.post(f'{HOST}/api/embeddings', json={'model': EMBED_MODEL, 'prompt': text}, timeout=300)
    r.raise_for_status()
    return r.json()['embedding']

def load_chunks():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    return [line.strip() for line in text.splitlines() if line.strip()]

def main():
    chunks = load_chunks()
    items = []
    for i, ch in enumerate(chunks):
        vec = embed(ch)
        items.append({'id': f'doc_{i}', 'text': ch, 'embedding': vec})
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)
    print(f'✅ Indexed {len(items)} chunks into {OUT_FILE}')

if __name__ == '__main__':
    main()