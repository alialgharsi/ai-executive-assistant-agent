import re


def split_text(text, max_sentences=2, overlap=1):
    """
    Split text by sentences instead of characters.

    max_sentences:
        Number of sentences in each chunk.

    overlap:
        Number of sentences repeated between chunks.
    """

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    start = 0

    while start < len(sentences):
        end = start + max_sentences

        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)

        if end >= len(sentences):
            break

        start = end - overlap

    return chunks
def retrieve_relevant_chunk(question, chunks):
    """
    Return the chunk with the highest number of matching words
    with the user's question.
    """

    question_words = set(question.lower().split())

    best_chunk = ""
    best_score = 0

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())

        score = len(question_words.intersection(chunk_words))

        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk
def build_context(results):
    """
    Combine retrieved chunks into one context string.
    """

    context_parts = []

    for result in results:
        context_parts.append(result["chunk"])

    return "\n\n".join(context_parts)