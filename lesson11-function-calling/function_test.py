import json, requests
from tools import get_time, calculate, search_docs

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi3:mini"

with open("index.jsonl") as f:
    DOCS = [json.loads(line) for line in f]

def call_ollama(messages):
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False},
        timeout=180
    )
    r.raise_for_status()
    return r.json()["message"]["content"]

def main():
    system_prompt = open("prompt.md").read()
    messages = [{"role": "system", "content": system_prompt}]

    print("✅ Lesson 11 Function Calling (Ollama). Type 'exit' to quit.\n")

    while True:
        user = input("User: ")
        if user == "exit":
            break

        messages.append({"role": "user", "content": user})
        raw = call_ollama(messages)

        try:
            data = json.loads(raw)
        except:
            print("Assistant:", raw)
            continue

        tool = data.get("tool")

        if tool == "get_time":
            result = get_time()
        elif tool == "calculate":
            result = calculate(data["arguments"]["expression"])
        elif tool == "search_docs":
            result = search_docs(data["arguments"]["query"], DOCS)
        elif tool == "final":
            print("Assistant:", data["answer"])
            continue
        else:
            result = "Unknown tool"

        messages.append({"role": "assistant", "content": str(result)})
        print("Assistant:", result)

if __name__ == "__main__":
    main()