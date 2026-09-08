# AI Executive Assistant Agent

A Python AI agent that combines Google Gemini tool calling, persistent task memory, local RAG with ChromaDB, and Google Calendar actions protected by explicit human approval.

## Highlights

- Conversational assistant powered by Google Gemini
- Gemini function/tool calling for task and knowledge operations
- Persistent task memory stored locally in JSON
- Local RAG using Sentence Transformers + ChromaDB
- Knowledge base automatically initializes from `notes.txt` on a fresh clone
- Source metadata returned with RAG search results
- Google Calendar OAuth 2.0 integration
- Natural-language calendar event proposals
- Human-in-the-loop approval before calendar writes and destructive task deletion
- Least-privilege Calendar event OAuth scope
- Retry/error handling for Gemini and Calendar API requests
- Project-local file access controls to reduce path-traversal risk
- Secrets and generated local data excluded from Git

## Architecture

```text
User
  |
  v
main.py -- approval boundary for sensitive actions
  |
  +-- agent.py
  |     +-- Gemini conversation + tool calling
  |     +-- natural-language calendar proposal extraction
  |
  +-- tools.py
  |     +-- task tools
  |     +-- safe project file reader
  |     +-- knowledge-base search
  |
  +-- calendar_tool.py
  |     +-- OAuth 2.0
  |     +-- list events
  |     +-- create event (only after caller approval)
  |
  +-- RAG
        +-- notes.txt
        +-- chunking
        +-- all-MiniLM-L6-v2 embeddings
        +-- ChromaDB (generated locally)
        +-- semantic retrieval
```

## Human-in-the-Loop Safety

Calendar creation is split into two stages:

1. Gemini converts a natural-language request into a proposed event payload.
2. The application displays the title, start, end, and timezone and requires an explicit `yes` before calling Google Calendar.

Example:

```text
You: Schedule a meeting with Ahmed tomorrow at 6 PM for one hour

Assistant: Proposed Google Calendar action
Title: Meeting with Ahmed
Start: 2026-09-09T18:00:00
End: 2026-09-09T19:00:00
Timezone: Asia/Riyadh

Create this event? (yes/no): no
Assistant: Action cancelled.
```

Deleting all saved tasks uses the same explicit approval pattern.

## RAG and Fresh-Clone Behavior

`chroma_db/` is generated data and is intentionally not committed. When the knowledge base is empty, the application automatically indexes `notes.txt`. This keeps the repository small while allowing RAG search to work after a fresh clone.

The current embedding model is `all-MiniLM-L6-v2` from Sentence Transformers.

## Technologies

- Python
- Google Gemini API / Google Gen AI Python SDK
- Google Calendar API
- Google OAuth 2.0
- Sentence Transformers
- ChromaDB
- scikit-learn
- python-dotenv

## Project Structure

```text
ai-executive-assistant-agent/
|-- main.py
|-- agent.py
|-- tools.py
|-- calendar_tool.py
|-- memory.py
|-- rag.py
|-- embeddings.py
|-- vector_store.py
|-- notes.txt
|-- requirements.txt
|-- .env.example
|-- .gitignore
`-- README.md
```

Generated/private local files such as `.env`, `credentials.json`, `token.json`, `tasks.json`, and `chroma_db/` are not committed.

## Installation

```bash
git clone https://github.com/alialgharsi/ai-executive-assistant-agent.git
cd ai-executive-assistant-agent
python -m venv .venv
```

Activate the virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

## Google Calendar Setup

1. Create a Google Cloud project and enable Google Calendar API.
2. Configure the OAuth consent screen.
3. Create an OAuth client with application type **Desktop app**.
4. Download the OAuth JSON and save it locally as `credentials.json` in the project folder.
5. Run the assistant. Google will open an authorization page on the first Calendar action and the app will create a local `token.json`.

`credentials.json` and `token.json` are ignored by Git and must never be committed.

If you previously authorized this project with a different Calendar OAuth scope, delete your local `token.json` once and authorize again.

## Run

```bash
python main.py
```

Try normal assistant requests, RAG questions, task management, or a scheduling request such as:

```text
Schedule a project review tomorrow at 6 PM for one hour
```

The event is not created until the user explicitly approves the displayed proposal.

## Security Notes

- API keys are loaded from environment variables.
- OAuth credentials/tokens remain local.
- Calendar writes require explicit approval in application code; the Calendar write function is not exposed directly as a Gemini tool.
- The text-file tool resolves paths inside the repository and only permits `.txt` and `.md` files.
- Calendar authorization uses the `calendar.events` scope rather than broad full-calendar access.

## Future Improvements

- LangGraph workflow/state orchestration
- Multi-document and PDF ingestion
- Source citations in generated RAG answers
- Calendar conflict/free-busy checking
- Email integration
- Automated tests and CI
- Web interface
- Docker deployment

## Author

**Ali Algharsi**  
Artificial Intelligence Student  
Python Developer | AI & Machine Learning
