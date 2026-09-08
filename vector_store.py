import os

import chromadb

from rag import split_text
from embeddings import model


DB_PATH = "chroma_db"
COLLECTION_NAME = "knowledge_base"
DEFAULT_KNOWLEDGE_FILE = "notes.txt"

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def index_document(filename: str) -> int:
    """Index a UTF-8 text document into the local ChromaDB collection."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Knowledge file '{filename}' was not found.")

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read().strip()

    if not text:
        return 0

    chunks = split_text(text, max_sentences=2, overlap=1)
    embeddings = model.encode(chunks).tolist()

    ids = [f"{os.path.basename(filename)}_{i}" for i in range(len(chunks))]
    metadatas = [
        {"source": os.path.basename(filename), "chunk_index": i}
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)


def ensure_knowledge_base(filename: str = DEFAULT_KNOWLEDGE_FILE) -> int:
    """Ensure a fresh clone has searchable knowledge without committing ChromaDB files."""
    if collection.count() == 0:
        return index_document(filename)
    return collection.count()


def search_document(question: str, top_k: int = 2):
    """Search the local knowledge base and return document, distance, and metadata."""
    ensure_knowledge_base()

    count = collection.count()
    if count == 0:
        return []

    n_results = min(top_k, count)
    question_embedding = model.encode([question])[0].tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results,
        include=["documents", "distances", "metadatas"],
    )

    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results.get("metadatas", [[]])[0]

    return list(zip(documents, distances, metadatas))
