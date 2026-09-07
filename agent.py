import os
from rag import split_text, build_context
from embeddings import create_embeddings, semantic_search
from dotenv import load_dotenv
from google import genai
from google.genai import types
import time
from google.genai.errors import ClientError, ServerError

from tools import (
    show_tasks,
    add_task,
    read_text_file,
    search_knowledge_base,
    clear_all_tasks
)


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-3.7-flash",
    config=types.GenerateContentConfig(
        tools=[
           show_tasks,
           add_task,
           read_text_file,
           search_knowledge_base
       ]
    )
)


import time
from google.genai.errors import ServerError


import time
from google.genai.errors import ClientError, ServerError


def ask_ai(user_input):
    max_attempts = 4

    for attempt in range(max_attempts):
        try:
            response = chat.send_message(user_input)
            return response.text

        except ClientError as error:
            if error.code == 429:
                wait_time = 15 * (attempt + 1)

                print(
                    f"\nRate limit reached. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

        except ServerError as error:
            if error.code == 503:
                wait_time = 5 * (attempt + 1)

                print(
                    f"\nGemini is busy. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

    return (
        "The AI service is temporarily unavailable. "
        "Please wait a little and try again."
    )
def ask_rag(question, filename="notes.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    chunks = split_text(
        text,
        max_sentences=2,
        overlap=1
    )

    chunk_embeddings = create_embeddings(chunks)

    results = semantic_search(
        question,
        chunks,
        chunk_embeddings,
        top_k=2
    )

    context = build_context(results)

    prompt = f"""
Answer the user's question using only the context below.

Context:
{context}

Question:
{question}

If the answer is not in the context, say:
I could not find the answer in the provided document.
"""

    response = chat.send_message(prompt)

    return response.text