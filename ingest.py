import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding

# 1. Load Environment Variables
load_dotenv()

def ingest_data():
    """
    Reads PDF documents from the 'data' directory, generates embeddings,
    and stores them in a local ChromaDB vector database.
    """
    
    # Check for API Key
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("❌ Error: GOOGLE_API_KEY not found in .env file.")

    print("⚙️  Initializing Embedding Model (Google text-embedding-004)...")
    
    # Configure the embedding model (Google's optimized model for retrieval)
    embed_model = GeminiEmbedding(model_name="models/text-embedding-004")
    Settings.embed_model = embed_model
    Settings.llm = None  # LLM is not required for ingestion (saves cost)

    # 2. Load Documents
    print("📂 Loading documents from 'data' directory...")
    try:
        documents = SimpleDirectoryReader("data").load_data()
        print(f"📄 Successfully loaded {len(documents)} document pages.")
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return

    # 3. Connect to Local Vector Database (ChromaDB)
    print("💾 Connecting to local ChromaDB...")
    db = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or retrieve the collection
    chroma_collection = db.get_or_create_collection("nadra_sop")
    
    # Set up the Vector Store
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Generate Embeddings and Save to Index
    print("🚀 Generating embeddings and indexing data (this may take a moment)...")
    VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context, 
        show_progress=True
    )

    print("✅ SUCCESS: Knowledge base updated successfully in 'chroma_db'.")

if __name__ == "__main__":
    ingest_data()