import os
from pathlib import Path

from memory import load_tasks, save_tasks
from vector_store import search_document


tasks = load_tasks()
PROJECT_ROOT = Path(__file__).resolve().parent
ALLOWED_TEXT_EXTENSIONS = {".txt", ".md"}


def show_tasks() -> dict:
    """Show all saved tasks."""
    return {"tasks": tasks}


def add_task(task: str) -> dict:
    """Add a new task to the saved task list."""
    tasks.append(task)
    save_tasks(tasks)
    return {
        "status": "success",
        "task_added": task,
        "tasks": tasks,
    }


def read_text_file(filename: str) -> dict:
    """Read a safe text/Markdown file from inside the project folder."""
    try:
        requested_path = (PROJECT_ROOT / filename).resolve()

        if PROJECT_ROOT not in requested_path.parents and requested_path != PROJECT_ROOT:
            return {
                "status": "error",
                "message": "Access outside the project folder is not allowed.",
            }

        if requested_path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
            return {
                "status": "error",
                "message": "Only .txt and .md files can be read.",
            }

        if not requested_path.is_file():
            return {
                "status": "error",
                "message": f"File '{filename}' was not found.",
            }

        with open(requested_path, "r", encoding="utf-8") as file:
            content = file.read()

        return {
            "status": "success",
            "filename": filename,
            "content": content,
        }

    except Exception as error:
        return {"status": "error", "message": str(error)}


def search_knowledge_base(question: str) -> dict:
    """Search the local vector knowledge base for information relevant to a question."""
    try:
        results = search_document(question, top_k=2)
    except Exception as error:
        return {"status": "error", "message": str(error)}

    documents = []
    for document, distance, metadata in results:
        documents.append(
            {
                "content": document,
                "distance": float(distance),
                "source": (metadata or {}).get("source", "unknown"),
            }
        )

    return {
        "status": "success",
        "question": question,
        "results": documents,
    }


def clear_all_tasks() -> dict:
    """Delete all saved tasks. Call only after explicit user approval."""
    tasks.clear()
    save_tasks(tasks)
    return {
        "status": "success",
        "message": "All tasks were deleted.",
    }
