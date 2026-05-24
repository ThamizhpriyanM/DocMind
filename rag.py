from extractor import extract_text, clean_text
from chunker import chunk_text
from embedder import embeded_chunks, get_embedding
from retriver import get_collection, store_chunks, retrieve
from generator import generate_ans
import os
import sys

def knowledge_base(pdf_path, collection_name="docmind"):

    filename = os.path.basename(pdf_path).replace(".pdf","").replace(" ","_")
    collection_name = f"doc_{filename}"[:50]

    print(f"collection : {collection_name}")
    raw_text = extract_text(pdf_path)
    clean = clean_text(raw_text)
    chunks = chunk_text(clean)
    embedded = embeded_chunks(chunks)

    collection = get_collection(collection_name)

    if collection.count() == 0:
        store_chunks(embedded, collection)
    else:
        print(f"Collection already has {collection.count()} chunks. Skipping indexing.")

    return collection

def ask(question, collection, n_results=3):

    query_vector = get_embedding(question)
    relevent_chunks = retrieve(query_vector, collection, n_results)
    answer = generate_ans(question, relevent_chunks)

    return answer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rag.py path/to/document.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    collection = knowledge_base(pdf_path)
    
    print(f"\n=== DocMind: {pdf_path} ===" )
    print("Ask questions. Type 'quit' to exit.\n")
   
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            break
        answer = ask(question, collection)
        print(f"\nDocMind: {answer}\n")