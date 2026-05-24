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
    pages = [pair[1].get("page", "?") for pair in chunk_pairs]
    
    context = "\n\n---\n\n".join(chunks)

    system_prompt = """Answer based only on the provided context. 
Cite sources when possible. Say I don't know if not in context."""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role" : "system" , "content" : system_prompt},
            {"role" : "user" , "content" : f"Context:\n{context}\n\nQuestion: {question}"}
        ],temperature=0
    )
    answer = res.choices[0].message.content
    #sources = ", ".join([f"p.{p}" for p in set(pages)])
    return f"{answer}\n\n"

def build_prompt(question, chunks):
    context = "\n\n---\n\n".join([chunk[0] for chunk in chunks])

    system_prompt = """you are a helpful  assistant that answers questions
    strictly based on the provided context

    Rules:
    - Only use information from the context below
    - If the answer is not in the context, say "I don't find that in the document"
    - Be concise and direct
    - Quote relevant parts when useful"""

    user_message = f"""context from the document : {context} ---- Question : {question}"""

    return system_prompt, user_message