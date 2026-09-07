import chromadb

from rag import split_text
from embeddings import model


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="knowledge_base"
)


def index_document(filename):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = split_text(
        text,
        max_sentences=2,
        overlap=1
    )

    embeddings = model.encode(chunks).tolist()

    ids = [
        f"{filename}_{i}"
        for i in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(chunks)


def search_document(question, top_k=2):
    question_embedding = model.encode([question])[0].tolist()

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]
    distances = results["distances"][0]

    return list(zip(documents, distances))