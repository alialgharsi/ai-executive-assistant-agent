from memory import load_tasks, save_tasks
import os
from vector_store import search_document

tasks = load_tasks()


def show_tasks() -> dict:
    """Show all saved tasks."""
    return {
        "tasks": tasks
    }


def add_task(task: str) -> dict:
    """Add a new task to the saved task list."""
    tasks.append(task)
    save_tasks(tasks)

    return {
        "status": "success",
        "task_added": task,
        "tasks": tasks
    }


def read_text_file(filename: str) -> dict:
    """Read a text file from the current project folder.

    Args:
        filename: Name of the text file, for example notes.txt

    Returns:
        File contents or an error message.
    """

    if not os.path.exists(filename):
        return {
            "status": "error",
            "message": f"File '{filename}' was not found."
        }

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        return {
            "status": "success",
            "filename": filename,
            "content": content
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }

def search_knowledge_base(question: str) -> dict:
    """Search the local knowledge base for information relevant to a question.

    Args:
        question: The user's question about the stored documents.

    Returns:
        Relevant information retrieved from the vector database.
    """

    results = search_document(
        question,
        top_k=2
    )

    documents = []

    for document, distance in results:
        documents.append({
            "content": document,
            "distance": float(distance)
        })

    return {
        "status": "success",
        "question": question,
        "results": documents
    }
def clear_all_tasks() -> dict:
    """Delete all saved tasks.

    This is a sensitive action and should only be called
    after explicit user approval.
    """

    tasks.clear()
    save_tasks(tasks)

    return {
        "status": "success",
        "message": "All tasks were deleted."
    }