# ChatBot: News Research Tool 📈

RockyBot is an AI-powered news research tool built using Streamlit, LangChain, and local Llama 3 models via Ollama. It allows users to input multiple news article URLs, scrapes the content, stores it in a local FAISS vector database, and lets users ask questions directly against the articles' content with accurate source citations.

## Features
- **Local AI execution**: Powered completely by local models using Ollama (`llama3.2:1b`), ensuring 100% data privacy. No API keys needed!
- **Automated Web Scraping**: Extracts text directly from provided URLs (bypassing basic anti-bot blocks using standard User-Agent headers).
- **RAG Architecture**: Uses FAISS for efficient similarity search and semantic retrieval over large, chunked documents.

## Project Structure
- `main.py`: The main Streamlit application script.
- `requirements.txt`: A list of required Python packages for the project.
- `.env`: (Not included) Environment variables if needed.
- `faiss_store_ollama/`: (Auto-generated) The local database where document embeddings are saved after processing URLs.

## Setup Instructions

1. **Install Local AI (Ollama)**
   Download and install [Ollama](https://ollama.com/), then run the following command in your terminal to download the 1B parameter model:
   ```bash
   ollama run llama3.2:1b
   ```

2. **Set up the Python Environment**
   Create a virtual environment to isolate the dependencies:
   ```bash
   python -m venv .venv
   ```

3. **Activate the Environment**
   - Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
   - Mac/Linux: `source .venv/bin/activate`

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the App**
   ```bash
   streamlit run main.py
   ```

## Usage
1. Open the sidebar and paste up to 3 URLs into the input fields.
2. Click **Process URLs** to scrape the content and compute the AI embeddings (this may take a minute on a laptop CPU).
3. Type any search query or question into the text bar on the main screen to receive an intelligent answer using the fetched documentation!
