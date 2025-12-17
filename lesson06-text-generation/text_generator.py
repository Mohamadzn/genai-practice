import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

def generate(prompt: str, temperature: float = 0.7, max_tokens: int = 200) -> str:
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,  # ollama generation length
        },
    }
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    return r.json().get("response", "").strip()

def main():
    print("✅ Lesson 06 – Text Generation (Ollama)")
    print("Type 'exit' to quit.\n")

    while True:
        prompt = input("Prompt> ").strip()
        if prompt.lower() == "exit":
            break
        if not prompt:
            print("❌ Please enter a prompt.\n")
            continue

        t = input("temperature [0.7]> ").strip() or "0.7"
        mx = input("max_tokens [200]> ").strip() or "200"

        try:
            out = generate(prompt, float(t), int(mx))
            print("\n--- Output ---")
            print(out)
            print("--------------\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()