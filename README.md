# Python backend

Copy your existing `main.py`, `messages.py`, `tool_schemas.py`, and `tools.py` into this folder. The included `api.py` imports `run_agent` from `main.py`.

## Required small change to main.py

Update `run_agent` to accept the optional `messages` argument and append the new user message when history is supplied.

Change:

```python
def run_agent(user_prompt: str) -> str:
    messages = create_messages(user_prompt)
```

to:

```python
def run_agent(user_prompt: str, messages: list | None = None) -> str:
    if messages is None:
        messages = create_messages(user_prompt)
    else:
        messages.append({"role": "user", "content": user_prompt})
```

Keep the rest of the function as-is. This lets the API preserve the same conversation history across requests. Your CLI continues to work.

## Setup on Windows PowerShell

From the `backend` directory:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Make sure Ollama is running and the `MODEL` constant in `main.py` matches the tag shown by `ollama list`.

Run:

```powershell
uvicorn api:app --reload --host 127.0.0.1 --port 8000
```

Test `http://127.0.0.1:8000/health` in a browser.
