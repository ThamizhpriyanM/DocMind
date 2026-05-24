import chromadb

def get_collection(collection_name= "docmind"):
    client = chromadb.PersistentClient(path= "./chroma_db")
    collection = client.get_or_create_collection(
        name = collection_name,
        metadata={"hsnw:space":"cosine"}
    )
    return collection

def store_chunks(chunks, collection):
    ids = [chunk["id"] for chunk in chunks]
    embeddings = [chunk["embedding"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"page" : chunk.get("page", "unknown")} for chunk in chunks]

    collection.add(
        ids = ids,
        embeddings = embeddings,
        documents = documents,
        metadatas = metadatas
    )
    print(f"Stored {len(chunks)} chunks in chromaDB")
    return collection

def retrieve(query_embedding, collection, n_results = 3):
    results = collection.query(
        query_embeddings = [query_embedding],
        n_results = n_results
    )
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    return list(zip(chunks, metadatas))

