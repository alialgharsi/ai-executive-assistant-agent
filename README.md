# AI Executive Assistant Agent

An AI-powered executive assistant built with Python, Google Gemini, local embeddings, ChromaDB, persistent memory, tool calling, and human approval for sensitive actions.

This project demonstrates how an AI agent can combine an LLM with external tools, persistent data, semantic retrieval, and controlled actions.

## Features

- Google Calendar integration using OAuth 2.0
- Read upcoming calendar events
- Create real calendar events
- Human-in-the-loop approval before sensitive actions
- Automatic retry handling for temporary Google Calendar connection errors
- Conversational AI powered by Google Gemini
- Automatic tool calling
- Task management
- Persistent task memory using JSON
- Local text file reading
- Retrieval-Augmented Generation (RAG) pipeline
- Local sentence-transformer embeddings
- Semantic search
- Persistent ChromaDB vector database
- Knowledge-base retrieval tool
- Human approval before sensitive actions
- Basic API error and rate-limit handling
- Environment-variable protection for API keys

## Architecture

```text
User
  |
  v
AI Executive Assistant
  |
  +-- Gemini LLM
  |
  +-- Tools
  |     +-- Show Tasks
  |     +-- Add Task
  |     +-- Read Text File
  |     +-- Search Knowledge Base
  |     +-- Clear Tasks (requires approval)
  |
  +-- Persistent Memory
  |     +-- tasks.json
  |
  +-- RAG Pipeline
        |
        +-- Document Chunking
        +-- Sentence Transformers
        +-- Local Embeddings
        +-- ChromaDB
        +-- Semantic Retrieval
```

## Human Approval

Sensitive actions should not be executed automatically.

For example, when a user requests:

```text
Delete all tasks
```

the assistant asks for explicit confirmation before deleting the stored tasks.

```text
This action will permanently delete all saved tasks.
Do you want to continue? (yes/no)
```

This demonstrates a basic human-in-the-loop safety mechanism for agent actions.

## RAG and Vector Search

The project includes a local retrieval pipeline:

```text
Documents
   |
   v
Chunking
   |
   v
Sentence Transformer Embeddings
   |
   v
ChromaDB Vector Store
   |
   v
Semantic Search
   |
   v
Relevant Context
```

The current implementation uses `all-MiniLM-L6-v2` through Sentence Transformers for local embeddings.

## Technologies

- Google Calendar API
- Google OAuth 2.0
- Python
- Google Gemini API
- Google Gen AI Python SDK
- Sentence Transformers
- ChromaDB
- scikit-learn
- python-dotenv

## Project Structure

```text
ai-executive-assistant-agent/
|
|-- main.py
|-- agent.py
|-- tools.py
|-- memory.py
|-- rag.py
|-- embeddings.py
|-- vector_store.py
|-- notes.txt
|-- tasks.json
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/alialgharsi/ai-executive-assistant-agent.git
cd ai-executive-assistant-agent
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

Never commit API keys or other secrets to a public repository.

## Run the Assistant

```bash
python main.py
```

## Example

```text
==================================================
AI Executive Assistant Agent
==================================================
Type 'exit' to close the assistant.

You: Delete all tasks

Assistant: This action will permanently delete all saved tasks.
Do you want to continue? (yes/no): no

Assistant: Action cancelled.
```

## What This Project Demonstrates

This project demonstrates practical concepts used in AI agent development:

- LLM integration
- Tool calling
- Persistent memory
- Retrieval-Augmented Generation
- Vector databases
- Semantic search
- Local embeddings
- Human-in-the-loop approval
- Secure API-key management
- Modular Python architecture

## Future Improvements

- Multi-document knowledge ingestion
- PDF document support
- Source-aware RAG responses
- LangGraph workflow orchestration
- Email and calendar integrations
- Improved permission controls
- Web interface
- Docker deployment

## Author

**Ali Algharsi**

Artificial Intelligence Student  
Python Developer | AI & Machine Learning