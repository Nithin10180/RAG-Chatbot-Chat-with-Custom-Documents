"""
ingest.py — Run this ONCE to load your documents into ChromaDB
Usage: python ingest.py
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
import pdfplumber

# ─── CONFIG ───────────────────────────────────────────────
DOCS_FOLDER = "documents"        # put your PDFs / .txt files here
DB_FOLDER   = "my_rag_db"        # ChromaDB will save here automatically
CHUNK_SIZE  = 500                # characters per chunk
CHUNK_OVERLAP = 50               # overlap between chunks
EMBED_MODEL = "all-MiniLM-L6-v2" # fast, free, runs locally
# ──────────────────────────────────────────────────────────


def load_pdf(path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def load_txt(path):
    """Extract text from a plain text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text, source_name):
    """Split text into overlapping chunks."""
    chunks = []
    metadatas = []
    start = 0
    i = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            metadatas.append({"source": source_name, "chunk_index": i})
        start = end - CHUNK_OVERLAP
        i += 1
    return chunks, metadatas


def ingest_documents():
    if not os.path.exists(DOCS_FOLDER):
        print(f"ERROR: '{DOCS_FOLDER}' folder not found.")
        print("Create a 'documents' folder and put your PDF or .txt files inside it.")
        return

    files = [f for f in os.listdir(DOCS_FOLDER) if f.endswith((".pdf", ".txt"))]
    if not files:
        print(f"No PDF or .txt files found in '{DOCS_FOLDER}' folder.")
        print("Add some documents and run ingest.py again.")
        return

    print(f"Found {len(files)} file(s): {files}\n")

    # Load embedding model
    print("Loading embedding model (first run downloads ~80MB)...")
    embedder = SentenceTransformer(EMBED_MODEL)
    print("Embedding model ready.\n")

    # Setup ChromaDB
    client = chromadb.PersistentClient(path=DB_FOLDER)
    # Clear old collection so we start fresh
    try:
        client.delete_collection("rag_docs")
    except Exception:
        pass
    collection = client.get_or_create_collection("rag_docs")

    total_chunks = 0

    for filename in files:
        filepath = os.path.join(DOCS_FOLDER, filename)
        print(f"Processing: {filename}")

        if filename.endswith(".pdf"):
            text = load_pdf(filepath)
        else:
            text = load_txt(filepath)

        if not text.strip():
            print(f"  WARNING: Could not extract text from {filename}, skipping.")
            continue

        chunks, metadatas = chunk_text(text, filename)
        print(f"  Split into {len(chunks)} chunks")

        # Generate embeddings
        embeddings = embedder.encode(chunks, show_progress_bar=True).tolist()

        # Store in ChromaDB
        ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        total_chunks += len(chunks)
        print(f"  Stored successfully.\n")

    print(f"Done! {total_chunks} total chunks stored in '{DB_FOLDER}'.")
    print("You can now run: python chatbot.py")


if __name__ == "__main__":
    ingest_documents()
