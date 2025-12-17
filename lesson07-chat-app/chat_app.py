import requests

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:mini"

def chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    r = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["message"]["content"]

def main():
    print("✅ Lesson 07 – Chat Application (Ollama)")
    print("Type 'exit' to quit.\n")

    # system message (important part of the lesson)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        try:
            reply = chat(messages)
            print(f"Assistant: {reply}\n")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()