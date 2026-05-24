def chunk_text(text, chunk_size = 100, overlap = 50):
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start+chunk_size
        chunk = text[start:end]
        chunks.append({
            "id": f"chunk_{chunk_id}",
            "text": chunk,
            "start_char": start,
            "end_char": end,
        })
        start = end - overlap
        chunk_id += 1
    
    return chunks