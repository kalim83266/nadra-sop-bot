import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding  # <-- Hum Google use karenge
from dotenv import load_dotenv

# 1. Environment Load
load_dotenv()

# Google API Key check
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ Google API Key nahi mili! .env file check karein.")

# 2. Setup Embedding Model (GOOGLE ONLINE) 🌐
# Hum HuggingFace ke bajaye Google ka 'text-embedding-004' use kar rahe hain.
# Yeh online chalega aur bohot fast hai.
print("⚙️ Connecting to Google Embeddings (Online)...")
embed_model = GeminiEmbedding(model_name="models/text-embedding-004")

Settings.embed_model = embed_model
Settings.llm = None

# 3. Read PDFs
print("📂 PDFs read kiye ja rahe hain...")
try:
    documents = SimpleDirectoryReader("data").load_data()
    print(f"📄 Total {len(documents)} pages read kiye gaye.")
except Exception as e:
    print(f"❌ Error reading PDFs: {e}")
    exit()

# 4. Create Local Database (ChromaDB)
print("💾 Local Database (ChromaDB) bana rahe hain...")
db = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db.get_or_create_collection("nadra_sop")

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 5. Save Data (Ingest)
print("🚀 Data Google se process hokar save ho raha hai...")
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)

print("✅ SUCCESS! Data save ho gaya hai.")