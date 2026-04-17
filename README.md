
# PubMed-Chatbot

## Overview
A conversational AI chatbot powered by retrieval-augmented generation (RAG) that queries and summarizes PubMed research papers.

## Features
- Search PubMed database
- Retrieve relevant research papers
- Generate conversational responses based on paper content
- Context-aware Q&A

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
git clone https://github.com/ManuBansalS/PubMed-Chatbot.git
cd PubMed-Chatbot
pip install -r requirements.txt
```

## Usage
```bash
cd src
python main.py
```

## Project Structure
```
PubMed-Chatbot/
├── data/
    ├── raw/
    └── processed/
├── src/
│   ├── database/
│   │   └──vector_store.py
│   ├── generation/
│   │   ├──generators.py
│   │   └── prompt_templates.py
│   ├── ingestion/
│   │   ├── embedder.py
│   │   ├── parser.py
│   │   └── pubmed_client.py
│   ├── logs/
│   ├── retrieval/
│   │   └── search_engine.py
│   ├── utils/
│   │   ├── logger.py
│   │   └── config.py
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
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
