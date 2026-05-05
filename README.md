🤖 Chat with your own PDF documents using AI — 100% local, no API key, zero cost.
# RAG Chatbot — Chat with Your Documents

> Ask questions to your own PDF files using AI. Runs fully offline. No API key. No cost.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Demo

![Demo Screenshot](screenshots/demo.png)

---

## What is this?

This is a **Retrieval-Augmented Generation (RAG)** chatbot that lets you
have AI-powered conversations with your own documents.

Unlike ChatGPT or Gemini, this chatbot:
- Only answers from YOUR documents — no hallucination
- Shows which file the answer came from
- Runs 100% on your own computer
- Requires no internet, no API key, no subscription

---

## How it Works

```
Your Question
     ↓
Search your documents for relevant chunks
     ↓
Send question + relevant chunks to local LLM
     ↓
Get accurate answer grounded in your document
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Ollama | Run LLM locally (phi3 / llama3) |
| ChromaDB | Local vector database |
| Sentence Transformers | Text embeddings |
| pdfplumber | PDF text extraction |

---

## Features

- Chat with any PDF or .txt document
- Answers sourced directly from your files
- Shows source file name with every answer
- Maintains conversation history in session
- Supports multiple documents at once
- Switch between any Ollama model
- Persistent database — ingest once, chat forever

---

## Requirements

- Python 3.9+
- Ollama (free, from ollama.com)
- 4GB RAM minimum (8GB recommended)

---

## Installation

**Step 1 — Clone the repository**
```bash
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot
```

**Step 2 — Install Python libraries**
```bash
pip install -r requirements.txt
```

**Step 3 — Install Ollama**

Download from https://ollama.com and install for your OS.

**Step 4 — Pull an AI model**
```bash
ollama pull phi3        # 4GB RAM
ollama pull llama3      # 8GB RAM (better quality)
```

**Step 5 — Add your documents**

Put your PDF or .txt files inside the `documents/` folder.

**Step 6 — Ingest your documents**
```bash
python ingest.py
```

---

## Running the Chatbot

**Terminal 1 — Ollama runs automatically on Windows.**
If on Mac/Linux, run:
```bash
ollama serve
```

**Terminal 2 — Start chatting**
```bash
python chatbot.py
```

Then type any question about your document and press Enter!

---

## Example Output

```
You: What is RAG?

Searching documents...
Bot: Retrieval-Augmented Generation (RAG) is a method in artificial
intelligence whereby when asked a question, the system first searches
for relevant documents from its database and uses that as context to
generate an accurate answer...

[Sources: sample_AI_notes.txt]
```

---

## Project Structure

```
rag-chatbot/
├── documents/               ← Put your PDFs here
│   └── sample_AI_notes.txt  ← Sample document included
├── screenshots/
│   └── demo.png             ← Demo screenshot
├── ingest.py                ← Load documents into database
├── chatbot.py               ← Main chat interface
├── requirements.txt         ← Python dependencies
└── README.md                ← This file
```

---

## Changing the Model

Open `chatbot.py` and change:
```python
OLLAMA_MODEL = "phi3"     # default
# to
OLLAMA_MODEL = "llama3"   # better quality
OLLAMA_MODEL = "mistral"  # good balance
OLLAMA_MODEL = "gemma:2b" # very lightweight
```

---

## Future Improvements

- [ ] Streamlit web UI
- [ ] Support for Word documents (.docx)
- [ ] Voice input and output
- [ ] Google Drive integration
- [ ] Multi-user support

---

## Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [your linkedin](https://linkedin.com/in/yourprofile)

---

## License

MIT License — free to use, modify and share.
