"""
chatbot.py — Run this to chat with your documents
Usage: python chatbot.py

Make sure you have run ingest.py first!
Make sure Ollama is running: ollama serve
"""

import sys
import chromadb
from sentence_transformers import SentenceTransformer
import ollama

# ─── CONFIG ───────────────────────────────────────────────
DB_FOLDER    = "my_rag_db"
EMBED_MODEL  = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "phi3"     # change to "llama3" if you have 8GB+ RAM
TOP_K        = 3          # number of chunks to retrieve per question
# ──────────────────────────────────────────────────────────


def load_resources():
    """Load embedder and ChromaDB collection."""
    try:
        client = chromadb.PersistentClient(path=DB_FOLDER)
        collection = client.get_collection("rag_docs")
    except Exception:
        print("ERROR: Could not find the database.")
        print("Please run 'python ingest.py' first to load your documents.")
        sys.exit(1)

    print("Loading embedding model...")
    embedder = SentenceTransformer(EMBED_MODEL)
    print("Ready!\n")
    return embedder, collection


def search_docs(question, embedder, collection):
    """Find the most relevant document chunks for a question."""
    question_embedding = embedder.encode([question]).tolist()
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=TOP_K
    )
    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    return chunks, sources


def ask_rag(question, embedder, collection, chat_history):
    """Search docs then ask Ollama with context."""

    # Step 1: Retrieve relevant chunks
    chunks, sources = search_docs(question, embedder, collection)
    context = "\n\n---\n\n".join(chunks)
    unique_sources = list(set(sources))

    # Step 2: Build prompt
    system_prompt = """You are a helpful assistant that answers questions based on the provided document context.
If the answer is clearly in the context, answer it directly.
If the answer is not in the context, say: "I couldn't find that in the provided documents."
Keep answers clear and concise."""

    user_message = f"""Context from documents:
{context}

Question: {question}"""

    # Step 3: Build messages with history
    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history[-6:]  # keep last 3 exchanges for context
    messages.append({"role": "user", "content": user_message})

    # Step 4: Call Ollama
    response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
    answer = response["message"]["content"]

    return answer, unique_sources


def main():
    print("=" * 50)
    print("  RAG Chatbot — Chat with your documents")
    print("=" * 50)
    print(f"  Model : {OLLAMA_MODEL}")
    print(f"  DB    : {DB_FOLDER}")
    print("  Type 'quit' to exit | 'clear' to reset history")
    print("=" * 50 + "\n")

    embedder, collection = load_resources()

    # Show how many documents are loaded
    count = collection.count()
    print(f"Database contains {count} chunks from your documents.\n")

    chat_history = []

    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not question:
            continue

        if question.lower() == "quit":
            print("Goodbye!")
            break

        if question.lower() == "clear":
            chat_history = []
            print("Chat history cleared.\n")
            continue

        print("\nSearching documents...", end="\r")

        try:
            answer, sources = ask_rag(question, embedder, collection, chat_history)
        except Exception as e:
            print(f"\nERROR: {e}")
            print("Make sure Ollama is running: open a terminal and run 'ollama serve'\n")
            continue

        # Add to history
        chat_history.append({"role": "user", "content": question})
        chat_history.append({"role": "assistant", "content": answer})

        print(f"\nBot: {answer}")
        print(f"\n[Sources: {', '.join(sources)}]")
        print("-" * 50 + "\n")


if __name__ == "__main__":
    main()
