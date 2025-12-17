# Lesson 06 – Text Generation (Ollama)

A simple CLI app that generates text using a local LLM via Ollama.

## Requirements
- Python 3.x
- Ollama running locally
- Model: `phi3:mini`

## Setup
```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install requests python-dotenv
ollama pull phi3:mini


<img width="742" height="145" alt="image" src="https://github.com/user-attachments/assets/04cf93bc-2d66-44de-bcd9-abdb87ae52e6" />
