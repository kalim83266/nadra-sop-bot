import streamlit as st
import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="NADRA SOP Assistant",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# ---------------------------------------------------------
# 2. CUSTOM CSS (STYLING)
# ---------------------------------------------------------
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    h1 { color: #006400; font-family: 'Helvetica', sans-serif; text-align: center; }
    [data-testid="stSidebar"] { background-color: #E8F5E9; border-right: 1px solid #c8e6c9; }
    .stChatMessage { background-color: white; border-radius: 15px; padding: 10px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; }
    [data-testid="stChatMessage"][data-testid="user"] { background-color: #E3F2FD; }
    .stButton button { background-color: #006400; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #004d00; color: white; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. BACKEND SETUP (MODEL CHANGED HERE ⬇️)
# ---------------------------------------------------------
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Google API Key nahi mili! .env file check karein.")
    st.stop()

@st.cache_resource(show_spinner=False)
def setup_knowledge_base():
    # -------------------------------------------------------
    # 👇 MODEL UPDATE: GEMINI 2.5 FLASH
    # -------------------------------------------------------
    # Humne yahan user ki request par model change kiya hai
    try:
        llm = Gemini(model="models/gemini-2.0-flash-lite", api_key=os.getenv("GOOGLE_API_KEY"))
    except:
        # Fallback: Agar 2.5 naam se load na ho, to 2.0 experimental try karega
        llm = Gemini(model="models/gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY"))

    # Embedding Model (Data dhoondne wala)
    embed_model = GeminiEmbedding(model_name="models/text-embedding-004")
    
    Settings.llm = llm
    Settings.embed_model = embed_model

    try:
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("nadra_sop")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return index
    except Exception as e:
        return None

# ---------------------------------------------------------
# 4. SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_Pakistan.svg", width=50)
    st.title("⚙️ Control Panel")
    st.markdown("---")
    st.success("🟢 System Online")
    st.info("🧠 Model: Gemini 2.5 Flash")
    st.warning("📂 DB: Local ChromaDB")
    
    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat reset ho gayi hai. Batiye ab kya madad karoon?"}
        ]
        st.rerun()
    st.markdown("---")
    st.caption("NADRA SOP System v1.0")

# ---------------------------------------------------------
# 5. CHAT INTERFACE
# ---------------------------------------------------------
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.title("🇵🇰 NADRA SOP Assistant")
    st.markdown("<p style='text-align: center; color: grey;'>Instant answers regarding SOPs, Fees & Processes</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalam-o-Alaikum! Main NADRA SOP Assistant hoon. Aap Urdu ya English mein sawal pooch sakte hain."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

try:
    index = setup_knowledge_base()
    if index is None:
        st.error("Database Error: Pehle 'ingest.py' chalayein.")
        st.stop()
        
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt=(
            "You are a professional NADRA Customer Service AI. "
            "Your answers must be accurate, polite, and based ONLY on the provided SOPs. "
            "Reply in the same language as the user (Urdu/English). "
            "Use bullet points where necessary."
        ),
        similarity_top_k=5,
        verbose=True
    )
except Exception as e:
    st.error(f"Engine Error: {e}")
    st.stop()

if prompt := st.chat_input("Sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Processing with Gemini 2.5..."):
            try:
                response = chat_engine.chat(prompt)
                st.markdown(response.response)
                st.session_state.messages.append({"role": "assistant", "content": response.response})
            except Exception as e:
                st.error(f"Error: {e}")