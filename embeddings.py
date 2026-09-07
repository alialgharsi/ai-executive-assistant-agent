from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Convert text chunks into numerical embeddings.
    """

    embeddings = model.encode(chunks)

    return embeddings


def semantic_search(question, chunks, chunk_embeddings, top_k=2):
    """
    Return the most semantically relevant chunks.
    """

    question_embedding = model.encode([question])

    similarities = cosine_similarity(
        question_embedding,
        chunk_embeddings
    )[0]

    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "chunk": chunks[index],
            "score": float(similarities[index])
        })

    return results