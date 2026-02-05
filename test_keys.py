import os
from dotenv import load_dotenv

load_dotenv()

print("----------- KEY CHECK -----------")
p_key = os.getenv("PINECONE_API_KEY")

if p_key:
    print(f"✅ Pinecone Key Found: {p_key[:5]}********")
else:
    print("❌ Pinecone Key NOT Found!")

print("---------------------------------")