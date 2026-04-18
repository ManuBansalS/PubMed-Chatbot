# PubMed-Chatbot

## Overview
A full-stack conversational AI chatbot tailored for medical research. Powered by a retrieval-augmented generation (RAG) backend that queries and summarizes PubMed research papers, and a sleek, modern React frontend.

## Features
- **Intelligent Search Engine**: Autonomously formulates optimized queries to search the PubMed database.
- **RAG Capabilities**: Fetches, chunks, and vector-stores relevant medical research papers.
- **Responsive Generation**: Delivers context-aware, accurately cited conversational responses based on real medical literature.
- **Modern Web Interface**: A premium dark-mode, glassmorphic UI built with React + Vite, featuring dynamic response animations.
- **FastAPI Backend**: Seamless, lightning-fast integration between the UI and the Python AI pipeline, served dynamically via Uvicorn.

## Installation

### Prerequisites
- Python 3.8+
- Node.js (v16+ for Vite UI)
- Git

### Initial Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ManuBansalS/PubMed-Chatbot.git
   cd PubMed-Chatbot
   ```

2. **Backend Setup**
   Ensure your `.env` is configured correctly (e.g., `CHROMA_API_KEY`).
   ```bash
   python -m venv .venv
   # On windows use: .venv\Scripts\activate
   # On unix use: source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd src_ui
   npm install
   npm run build
   cd ..
   ```

## Usage

### Run the Web Application (Recommended)
This starts up the backend API and powerfully serves the beautifully designed React frontend.

```bash
uvicorn api:app --reload
```
Navigate to **http://localhost:8000** in your web browser.

### Run the CLI System
If you prefer a lightning-fast terminal AI experience, you can still run the bot headless:
```bash
python main.py
```

## Project Structure
```text
PubMed-Chatbot/
├── src_rag/                # Core Python RAG Pipeline
│   ├── data/
│   │   ├── processed/      # Contains latest_chunks.json
│   │   └── raw/            # Contains latest_fetch.xml
│   ├── database/
│   │   └── vector_store.py
│   ├── generation/
│   │   ├── generators.py
│   │   ├── optimizer.py
│   │   └── prompt_templates.py
│   ├── ingestion/
│   │   ├── embedder.py
│   │   ├── parser.py
│   │   └── pubmed_client.py
│   ├── logs/
│   │   └── pipeline.log
│   ├── retrieval/
│   │   └── search_engine.py
│   └── utils/
│       ├── check_models.py
│       ├── config.py
│       └── logger.py
├── src_ui/                 # Vite + React Frontend
│   ├── public/             # Contains favicon & icons
│   ├── src/                # Web application source files
│   ├── index.html          
│   ├── package.json
│   ├── vite.config.ts
│   └── [configuration files...]
├── .env
├── .env.example
├── .gitignore
├── api.py                  # FastAPI application & web server mount
├── LICENSE
├── main.py                 # Fallback Command Line Entry point
├── README.md
└── requirements.txt
```

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## Issues
Found a bug? Please [open an issue](https://github.com/ManuBansalS/PubMed-Chatbot/issues) with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior

## Author
**Manu Bansal**

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Support
For questions or support, please open an issue on GitHub.
