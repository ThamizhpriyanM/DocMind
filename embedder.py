from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os

#dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv()

client = OpenAI(
    api_key = os.getenv("YOUR_JINA_KEY"),
    base_url = "https://api.jina.ai/v1"
)

def get_embedding(text):
    response = client.embeddings.create(
        model = "jina-embeddings-v3",
        input= text
    )
    return response.data[0].embedding

def embeded_chunks(chunks):
    print(f"Embedding {len(chunks)} chunks..")

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = get_embedding(chunk["text"])

        if(i+1) % 10 == 0:
            print(f"Done{i+1}/{len(chunks)}")

    print("All chunks embedded!")
    return chunks