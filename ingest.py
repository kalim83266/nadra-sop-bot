import os
from dotenv import load_dotenv

# LlamaIndex libraries
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

# 1. Load Environment Variables (API Keys)
load_dotenv()

# 2. Setup Configuration
# Hum "all-mpnet-base-v2" model use kar rahe hain kyunki iska dimension 768 hai
# Jo aapne Pinecone par set kiya tha.
print("Settings configure ho rahi hain...")
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
Settings.llm = None  # Ingestion ke waqt LLM ki zaroorat nahi hoti, sirf Embedding ki hoti hai

# 3. Connect to Pinecone
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)

# Index ka naam wahi hona chahiye jo aapne Pinecone dashboard par banaya tha
index_name = "nadra-sop-index" 
pinecone_index = pc.Index(index_name)

# 4. Connect LlamaIndex to Pinecone
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 5. Load Data & Create Index
print("PDFs read kiye ja rahe hain...")
documents = SimpleDirectoryReader("./data").load_data()

print(f"Total {len(documents)} pages read kiye gaye. Ab upload ho raha hai (Time lag sakta hai)...")

# Yeh line sabse important hai: Yeh data ko convert karke Cloud par bhejti hai
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True
)

print("✅ Success! Aapka data Pinecone par upload ho gaya hai.")