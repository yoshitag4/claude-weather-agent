# Claude Weather Agent

A tool-using Claude agent that answers weather and date/time questions. It can be run in three ways:

1. **Command line** – standalone interactive chat (`app4.py`)
2. **Postman / any HTTP client** – FastAPI backend (`api/main.py`)
3. **Web UI** – React + Vite frontend talking to the FastAPI backend

## Table of Contents

- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Run 1: Command Line (Standalone)](#run-1-command-line-standalone)
- [Run 2: From Postman (REST API)](#run-2-from-postman-rest-api)
- [Run 3: With the Frontend](#run-3-with-the-frontend)
- [Troubleshooting](#troubleshooting)

---

## How It Works

### Flow diagram

```
                 User
                  │
                  ▼
           ClaudeAgent.chat()
                  │
                  ▼
         add_user_message()
                  │
                  ▼
            call_claude()
                  │
                  ▼
        Claude decides tools
                  │
                  ▼
      Assistant Message
   (ToolUse + Text Blocks)
                  │
                  ▼
        find_tool_uses()
                  │
                  ▼
         execute_tool()
                  │
                  ▼
     Weather Tool / DateTime Tool
                  │
                  ▼
      ToolResultBlockParams
                  │
                  ▼
      add_tool_results_message()
                  │
                  ▼
           call_claude()
                  │
                  ▼
          Final Assistant Text
                  │
                  ▼
              Return Text
```

### Step by step

```python
# 1. User message
add_user_message()

# 2. Ask Claude
response = call_claude()

# 3. Preserve Claude's response
add_assistant_message()

# 4. Check if Claude requested a tool
tool_use = find_tool_use()

# 5. Execute Python function
result = execute_tool()

# 6. Send result back
add_tool_result_message()

# 7. Ask Claude again
final = call_claude()
```

---

## Project Structure

```
.
├── app4.py              # CLI entry point (interactive chat loop)
├── api/main.py          # FastAPI app (/health, /chat, /chat/{session_id})
├── agent/               # ClaudeAgent – the chat / tool-use loop
├── services/            # Claude API calls and tool dispatcher
├── tools/               # Weather and date/time tool implementations
├── schemas/             # Tool schemas sent to Claude (ALL_TOOLS)
├── models/              # Pydantic request/response models
├── config/              # Anthropic client, model, and settings
├── prompts/             # System prompts
├── utils/               # Message helpers, logging, JSON utils
├── tests/               # Tests
├── frontend/            # React + Vite + TypeScript web UI
├── requirements.txt
└── .env                 # API keys (never commit this)
```

---

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm (only for the frontend)
- An [Anthropic API key](https://console.anthropic.com/)
- An [OpenWeather API key](https://openweathermap.org/api)
- [Postman](https://www.postman.com/downloads/) (only for Run 2)

## Setup

Run from the project root.

1. **(Optional) Create a virtual environment**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install Python dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure API keys** – create a `.env` file in the project root:

   ```env
   ANTHROPIC_API_KEY="your-anthropic-key"
   OPENWEATHER_API_KEY="your-openweather-key"
   ```

   > Keep `.env` out of version control and never share these keys.

---

## Run 1: Command Line (Standalone)

No server or frontend needed.

```powershell
python app4.py
```

Example session:

```
Weather Agent Started 🌤️
Ask me weather questions.
Type 'exit' to quit.

You: What's the weather in Hyderabad and what time is it there?

Assistant:
...
--------------------------------------------------
```

Type `exit`, `quit`, or `bye` to stop.

---

## Run 2: From Postman (REST API)

### 1. Start the backend

```powershell
python -m uvicorn api.main:app --reload --port 8000
```

- Base URL: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`

### 2. Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/health` | Health check |
| POST | `/chat` | Send a message to the agent |
| DELETE | `/chat/{session_id}` | End a session and clear its history |

### 3. Postman requests

**Health check**

- Method: `GET`
- URL: `http://localhost:8000/health`
- Response: `{ "status": "ok" }`

**Start a conversation**

- Method: `POST`
- URL: `http://localhost:8000/chat`
- Headers: `Content-Type: application/json`
- Body → raw → JSON:

  ```json
  {
    "message": "What's the weather in London?"
  }
  ```

- Response:

  ```json
  {
    "session_id": "3f2b9c1e-....",
    "response": "It's currently ..."
  }
  ```

**Continue the conversation** – copy `session_id` from the previous response and send it back so the agent remembers the history:

```json
{
  "message": "And what about tomorrow?",
  "session_id": "3f2b9c1e-...."
}
```

**End the session**

- Method: `DELETE`
- URL: `http://localhost:8000/chat/{session_id}`
- Response: `{ "status": "deleted", "session_id": "..." }` (`404` if the session doesn't exist)

> Tip: in Postman, add a test script to `POST /chat` to save the session automatically, then use `{{session_id}}` in later requests:
>
> ```js
> pm.collectionVariables.set("session_id", pm.response.json().session_id);
> ```

**Error codes:** `422` invalid body (e.g. empty `message`), `502` the Claude call failed (check your API key).

Sessions are stored in memory and are lost when the server restarts.

---

## Run 3: With the Frontend

The frontend is a React + Vite app that calls the FastAPI backend, so you need two terminals.

**Terminal 1 – backend** (from the project root)

```powershell
python -m uvicorn api.main:app --reload --port 8000
```

**Terminal 2 – frontend**

```powershell
cd frontend
npm install     # first time only
npm run dev
```

Open the URL printed by Vite (default `http://localhost:5173`). The header shows **API: ok** when the backend is reachable.

Configuration notes:

- The frontend calls `http://localhost:8000` by default. To change it, create `frontend/.env` with `VITE_API_BASE_URL=http://localhost:<port>`.
- The backend only allows CORS from `http://localhost:5173` (see `api/main.py`). If Vite starts on another port, update `allow_origins` there.

Production build: `npm run build` (output in `frontend/dist`).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` from the project root, and start uvicorn from the project root. |
| `502` from `/chat` | Check `ANTHROPIC_API_KEY` in `.env` and your network. |
| Weather lookups fail | Check `OPENWEATHER_API_KEY` in `.env` (new keys can take a while to activate). |
| Frontend shows API: offline / CORS error | Make sure the backend is running on port 8000 and the frontend is on port 5173. |
| Port 8000 already in use | Use `--port 8001` and set `VITE_API_BASE_URL` accordingly. |