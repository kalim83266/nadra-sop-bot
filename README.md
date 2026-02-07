# 🇵🇰 NADRA SOP Assistant

**AI‑Powered Retrieval‑Augmented Generation (RAG) Chatbot for Official SOPs**

&#x20; &#x20;

---

## 📌 Overview

**NADRA SOP Assistant** is a production‑grade AI chatbot built to deliver **accurate, verifiable answers** strictly from official NADRA documents (SOPs, CNIC fee schedules, and registration policies).

The system uses **Retrieval‑Augmented Generation (RAG)** to ground every response in source PDFs—minimizing hallucinations and ensuring policy‑level accuracy. It supports **English, Urdu, and Roman Urdu** queries.

> ⚠️ This repository demonstrates an **AI reference assistant**. It is **not an official NADRA product**.

---

## ✨ Key Capabilities

- **🧠 Fast, Reliable Reasoning:** Powered by **Google Gemini 2.5 Flash** for low‑latency responses.
- **📂 Secure Local Vector Store:** **ChromaDB** with persistent local storage (no external vector DB required).
- **🔎 Grounded Answers (RAG):** Responses are generated **only** from indexed PDFs.
- **💬 Context‑Aware Chat:** Maintains conversational history for accurate follow‑ups.
- **🌐 Multilingual:** English, Urdu, and Roman Urdu input/output.
- **🎨 Clean UI:** Streamlit‑based interface with chat bubbles and sidebar controls (ideal for demos/admin use).

---

## 🧱 Architecture (High‑Level)

```
User (Web / Mobile)
        │
        ▼
  Streamlit UI (Demo/Admin)
        │
        ▼
   RAG Pipeline (LlamaIndex)
        │
        ▼
 Gemini 2.5 Flash  +  ChromaDB (Local)
```

> **Note:** For production web/mobile apps, the RAG logic can be exposed via **FastAPI** and consumed by React/Flutter clients.

---

## 🛠️ Technology Stack

| Layer                     | Technology                   |
| ------------------------- | ---------------------------- |
| **Language**              | Python 3.10+                 |
| **LLM**                   | Google Gemini 2.5 Flash      |
| **Embeddings**            | Google `text-embedding-004`  |
| **RAG Framework**         | LlamaIndex                   |
| **Vector Database**       | ChromaDB (Local, Persistent) |
| **Frontend (Demo/Admin)** | Streamlit                    |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/nadra-sop-bot.git
cd nadra-sop-bot
```

### 2️⃣ Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

> 🔒 **Security:** Never commit `.env` files or API keys to version control.

---

## ▶️ Usage Guide

### Step 1: Add Source Documents

Place official SOP and policy PDFs into the `data/` directory.

### Step 2: Build the Vector Database

Run the ingestion pipeline to parse PDFs and generate embeddings:

```bash
python ingest.py
```

Wait for the **"✅ SUCCESS"** confirmation.

### Step 3: Launch the Application

```bash
streamlit run app.py
```

Open the provided local URL in your browser to start chatting.

---

## 📁 Project Structure

```
nadra-sop-bot/
│
├── chroma_db/             # Auto-generated local vector database
├── data/                  # Source PDF documents
├── .env                   # Environment variables (ignored by git)
├── .gitignore             # Git ignore rules
├── app.py                 # Streamlit chatbot UI
├── ingest.py              # PDF ingestion & indexing script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 📸 Screenshots

*Add UI screenshots here to showcase the chat experience.*

---

## 🚀 Production Notes

- Streamlit is recommended for **demos, internal tools, and admin panels**.
- For public deployment (Web/Android/iOS), expose the RAG logic via **FastAPI** and build a dedicated frontend (React / Flutter).
- Implement **authentication, rate limiting, and HTTPS** for enterprise or government‑grade deployments.

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request with clear details

---

## 📄 License & Disclaimer

This project is intended for **educational and reference purposes only**. It is not affiliated with or endorsed by NADRA. All documents remain the property of their respective owners.

---

## 👤 Author

**Kaleem Ullah**\
*AI & RAG Systems Developer*

> Built as a portfolio‑grade project demonstrating secure, multilingual, document‑grounded AI systems.

