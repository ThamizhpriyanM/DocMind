from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
     api_key = os.getenv("OPENAI_API_KEY"),
    base_url = "https://api.groq.com/openai/v1"
)

def generate_ans(question, chunk_pairs):

    chunks = [pair[0] for pair in chunk_pairs]
    context = "\n\n---\n\n".join(chunks)

    system_prompt = """You are a friendly and helpful AI assistant that answers questions
strictly based on the provided document context.

Rules:
- Only use information from the provided context for document-related questions
- If the answer is not in the context, say:
  "I don't find that in the document."
- Be concise, clear, and direct
- Quote relevant parts when useful

Conversation Rules:
- Respond naturally to greetings and casual messages
- If the user says "hi", greet them warmly
- If the user says "thanks", reply politely like:
  "You're welcome!" or "Happy to help!"
- Maintain a friendly and professional tone
- Do not invent document information outside the context"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role" : "system" , "content" : system_prompt},
            {"role" : "user" , "content" : f"Context:\n{context}\n\nQuestion: {question}"}
        ],temperature=0
    )
    answer = res.choices[0].message.content
    return f"{answer}\n\n"
