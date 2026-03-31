# News Research Tool 🔍

An AI-powered news research assistant that answers questions over any set of news article URLs — **100% offline, no API keys required**. Paste up to 3 URLs, ask anything, and receive accurate answers with source citations backed by a local LLM.

> **Live demo:** _[Deploy to Streamlit Cloud and add your link here]_

---

## Demo

> _Add a screenshot or GIF here showing a question being answered with source citations._
>
> ```
> ![App demo](docs/demo.gif)
> ```

---

## How it works

```
User pastes article URLs
         ↓
Web scraper fetches article text
         ↓
Text split into chunks (RecursiveCharacterTextSplitter)
         ↓
Chunks embedded and stored in FAISS vector index
         ↓
User asks a question
         ↓
FAISS retrieves the most relevant chunks (similarity search)
         ↓
Llama 3 (via Ollama) generates a grounded answer with citations
         ↓
Answer + source URLs displayed in Streamlit
```

This is a **Retrieval-Augmented Generation (RAG)** pipeline. The LLM never generates from memory alone — every answer is grounded in the retrieved article text.

---

## Features

- **Fully offline** — runs on your laptop CPU using Ollama's `llama3.2:1b` model. No OpenAI or Anthropic API key needed.
- **RAG architecture** — FAISS vector database with semantic similarity search prevents hallucination.
- **Source citations** — every answer includes the source URL it was derived from.
- **Anti-bot scraping** — uses standard `User-Agent` headers to bypass basic blocks on news sites.
- **Persistent index** — embeddings are saved locally in `faiss_store_ollama/` so you don't re-process URLs on every run.

---

## Tech stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | Llama 3.2 1B (via Ollama) |
| Embeddings | `nomic-embed-text` (Ollama) |
| Vector DB | FAISS (local) |
| Orchestration | LangChain |
| Web scraping | `UnstructuredURLLoader` |

---

## Project structure

```
News-Research-Tool/
├── main.py              # Streamlit app — UI, scraping, RAG pipeline
├── requirements.txt     # Python dependencies
├── .gitignore
├── .env                 # (not committed) environment variables if needed
└── faiss_store_ollama/  # (auto-generated) local FAISS vector index
```

---

## Setup

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running

### 1. Install Ollama and pull the models

```bash
# Install Ollama from https://ollama.com/

# Pull the LLM
ollama pull llama3.2:1b

# Pull the embedding model
ollama pull nomic-embed-text
```

### 2. Clone and install dependencies

```bash
git clone https://github.com/vasu-bhai/News-Research-Tool.git
cd News-Research-Tool

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run main.py
```

App opens at `http://localhost:8501`.

---

## Usage

1. Paste up to **3 news article URLs** into the sidebar input fields.
2. Click **Process URLs** — the app scrapes content, generates embeddings, and saves the FAISS index (this takes 30–60 seconds on a laptop CPU the first time).
3. Type any question in the main input box and press Enter.
4. The app returns a grounded answer with the source URL.

---

## Example questions

After processing a few financial news articles:

> "What did the Fed announce about interest rates?"
> "Which companies were mentioned as being affected by the new policy?"
> "What is the analyst forecast for Q4?"

---

## Limitations

- Processes up to 3 URLs per session (expandable by modifying `main.py`).
- Response time is 15–45 seconds on a CPU depending on article length.
- Some news sites with heavy JavaScript rendering may not scrape correctly.

---

## Future improvements

- [ ] Deploy to Streamlit Cloud with a cloud-hosted LLM option
- [ ] Support more than 3 URLs
- [ ] Add multi-session history / saved searches
- [ ] Add async scraping for faster URL processing
- [ ] Support PDF uploads in addition to URLs

---

## License

MIT — free to use and modify.
