# 🇵🇰 NADRA SOP AI Assistant (RAG Chatbot)

> **An AI-powered chatbot that provides instant, accurate answers from NADRA's Standard Operating Procedures (SOPs) using Retrieval-Augmented Generation (RAG).**

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LlamaIndex](https://img.shields.io/badge/Framework-LlamaIndex-purple)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-orange)
![Pinecone](https://img.shields.io/badge/Vector%20DB-Pinecone-green)

---

## 📖 About The Project

Navigating through hundreds of pages of official NADRA documentation (PDFs) to find specific rules regarding CNIC renewal, fees, or family registration can be time-consuming and prone to human error.

**NADRA SOP AI Assistant** solves this by allowing users to ask questions in natural language (English or Roman Urdu). It scans the official documents, finds the exact relevant section, and uses **Google Gemini** to generate a precise answer based **only** on the official rules.

---

## 🏗️ System Architecture

The project follows a modern RAG pipeline to ensure high accuracy and low hallucination.

```mermaid
graph TD
    A[📂 NADRA PDFs] -->|1. Load & Chunk| B(📄 Text Chunks)
    B -->|2. Embed via HuggingFace| C{📐 Vectors}
    C -->|3. Upsert| D[(🌲 Pinecone DB)]
    
    U[👤 User Query] -->|4. Embed Query| E{📐 Query Vector}
    E -->|5. Similarity Search| D
    D -->|6. Retrieve Top Matches| F[📝 Relevant Context]
    
    F -->|7. Context + Query| G[🧠 Gemini 1.5 Flash]
    G -->|8. Generate Answer| H[💬 Final Response]

    🌟 Key Features📚 RAG Architecture: Answers are grounded in facts extracted directly from uploaded PDFs.⚡ Fast Search: Utilizes Pinecone (Vector Database) for millisecond-latency semantic search.🧠 Advanced LLM: Powered by Google Gemini 1.5 Flash for understanding complex queries.📂 Automated Ingestion: A dedicated script (ingest.py) to convert PDF SOPs into vector embeddings.💻 Interactive UI: Clean and responsive interface built with Streamlit.🛠️ Tech StackComponentTechnologyDescriptionFrameworkLlamaIndexOrchestrating data retrieval and generation.LLMGoogle Gemini 1.5 FlashGenerates human-like responses.Vector DBPineconeCloud-based vector storage.EmbeddingsHuggingFacesentence-transformers/all-mpnet-base-v2 (768 dimensions).FrontendStreamlitUser Interface.🚀 How to Run LocallyFollow these steps to set up the project on your local machine.1. Clone the RepositoryBashgit clone [https://github.com/kalim83266/nadra-sop-bot.git](https://github.com/kalim83266/nadra-sop-bot.git)
cd nadra-sop-bot
2. Create Conda EnvironmentBashconda create -n nadra_rag python=3.10 -y
conda activate nadra_rag
3. Install DependenciesBashpip install -r requirements.txt
4. Setup Environment VariablesCreate a .env file in the root directory and add your API keys:Ini, TOMLGOOGLE_API_KEY="your_google_api_key"
PINECONE_API_KEY="your_pinecone_api_key"
HF_TOKEN="your_huggingface_token"
5. Ingest Data (Upload to Cloud)Place your NADRA PDF files in the data/ folder and run:Bashpython ingest.py
This will read the PDFs, convert them to vectors, and store them in Pinecone.6. Run the ChatbotBashstreamlit run app.py
📂 Project StructurePlaintextnadra-sop-bot/
├── .env                  # API Keys (Keep this private!)
├── .gitignore            # Prevents secrets from being uploaded
├── requirements.txt      # List of libraries
├── ingest.py             # Script for data processing (Run once)
├── app.py                # Main application script (Run everytime)
└── data/                 # Folder for PDF documents
🤝 ContributingContributions are welcome!Fork the ProjectCreate your Feature BranchCommit your ChangesPush to the BranchOpen a Pull Request📧 ContactDeveloper: KalimGitHub: kalim83266