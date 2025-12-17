from datetime import datetime

def get_time():
    return datetime.utcnow().isoformat()

def calculate(expression: str):
    try:
        return eval(expression, {"__builtins__": {}})
    except Exception:
        return "operation not available"

def search_docs(query: str, docs):
    results = []
    for d in docs:
        if query.lower() in d["text"].lower():
            results.append(d["text"])
    return results[:2]