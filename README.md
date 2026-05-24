# DocMind — PDF Question Answering with RAG

Ask questions about any PDF document and get grounded, cited answers using Retrieval Augmented Generation (RAG) — built from scratch with Python and OpenAI.

---

## What it does

DocMind lets you load any PDF and chat with it. Instead of asking an LLM to "remember" your document, it:

1. Extracts text from the PDF
2. Splits it into overlapping chunks
3. Converts each chunk into a vector (embedding)
4. Stores everything in a local vector database (ChromaDB)
5. For every question: finds the most relevant chunks → sends them to the LLM → returns a grounded answer with page citations

No hallucinations. No guessing. If the answer isn't in the document, it says so.

---

## Project structure

```
docmind/
├── rag.py           # orchestrator — the ask() function lives here
├── extractor.py     # PDF text extraction (PyMuPDF)
├── chunker.py       # splits text into overlapping chunks
├── embedder.py      # converts text to vectors (OpenAI API)
├── retriever.py     # stores and searches ChromaDB
├── generator.py     # builds prompts and calls the LLM
├── data/            # put your PDFs here
├── chroma_db/       # auto-created — your local vector database
├── .env             # your API key (never commit this)
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/docmind.git
cd docmind
```

### 2. Install dependencies

```bash
pip install openai pymupdf chromadb python-dotenv
```

### 3. Add your OpenAI API key

Create a `.env` file in the root folder:

```
OPENAI_API_KEY=your-key-here
```

Get a free key at [platform.openai.com](https://platform.openai.com)

### 4. Add a PDF

Drop any PDF into the `data/` folder.

---

## Usage

```bash
python rag.py data/your_document.pdf
```

Then just type your questions:

```
=== DocMind: data/your_document.pdf ===
Ask questions. Type 'quit' to exit.

You: What are the main findings?

DocMind: The document highlights three key findings...
[Sources: p.4, p.7]

You: quit
```

## How RAG works (the full pipeline)

```
PDF file
  └── extractor.py   → raw text + page numbers
        └── chunker.py     → overlapping 500-char chunks
              └── embedder.py    → 1536-dim vectors per chunk
                    └── retriever.py   → stored in ChromaDB on disk
                          └── (user asks a question)
                                └── embedder.py    → embed the question
                                      └── retriever.py   → find top 3 similar chunks
                                            └── generator.py   → LLM answers using only those chunks
```

The key insight: the LLM never sees the whole document. It only sees the 3 most relevant chunks for each question. This keeps answers focused and prevents hallucination.

---

## Configuration

You can tune these values in the source files:

| Setting | File | Default | Effect |
|---|---|---|---|
| `chunk_size` | chunker.py | 500 chars | Larger = more context per chunk |
| `overlap` | chunker.py | 50 chars | More overlap = fewer boundary issues |
| `n_results` | retriever.py | 3 chunks | More chunks = more context for the LLM |
| `temperature` | generator.py | 0.2 | Lower = more factual, higher = more creative |
| `model` | generator.py | gpt-4o-mini | Swap for gpt-4o for harder questions |

---

## Tech stack

- **Python 3.10+**
- **OpenAI API** — embeddings (`text-embedding-3-small`) + chat (`gpt-4o-mini`)
- **PyMuPDF (fitz)** — PDF text extraction
- **ChromaDB** — local vector database, persists to disk
- **python-dotenv** — environment variable management

---

## License

MIT — use it, break it, learn from it.
