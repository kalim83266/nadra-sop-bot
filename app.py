import streamlit as st
import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini

# ---------------------------------------------------------
# 1. APPLICATION CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="NADRA SOP Assistant",
    page_icon="🇵🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# ---------------------------------------------------------
# 2. UI STYLING (CSS)
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #F8F9FA; }
    
    /* Header Styling */
    h1 { color: #006400; font-family: 'Helvetica', sans-serif; text-align: center; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #E8F5E9; border-right: 1px solid #c8e6c9; }
    
    /* Chat Bubbles */
    .stChatMessage { background-color: white; border-radius: 15px; padding: 10px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px; }
    [data-testid="stChatMessage"][data-testid="user"] { background-color: #E3F2FD; }
    
    /* Button Styling */
    .stButton button { background-color: #006400; color: white; border-radius: 8px; }
    .stButton button:hover { background-color: #004d00; color: white; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. BACKEND INITIALIZATION
# ---------------------------------------------------------

# Validate API Key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("❌ Critical Error: GOOGLE_API_KEY is missing from environment variables.")
    st.stop()

@st.cache_resource(show_spinner=False)
def initialize_system():
    """
    Initializes the LLM, Embedding Model, and Vector Database connection.
    Uses caching to prevent reloading on every interaction.
    """
    try:
        # Initialize LLM: Using Gemini 2.5 Flash for speed and efficiency
        # Fallback logic included for model versioning stability
        try:
            llm = Gemini(model="models/gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
        except:
            llm = Gemini(model="models/gemini-2.0-flash-exp", api_key=os.getenv("GOOGLE_API_KEY"))

        # Initialize Embedding Model
        embed_model = GeminiEmbedding(model_name="models/text-embedding-004")
        
        # Configure Global Settings
        Settings.llm = llm
        Settings.embed_model = embed_model

        # Connect to Local ChromaDB
        db = chromadb.PersistentClient(path="./chroma_db")
        chroma_collection = db.get_or_create_collection("nadra_sop")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        
        # Load the Index
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        return index
    except Exception as e:
        return None

# ---------------------------------------------------------
# 4. SIDEBAR CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_Pakistan.svg", width=50)
    st.title("⚙️ System Status")
    st.markdown("---")
    
    # Status Indicators
    st.success("🟢 Service Online")
    st.info("🧠 Model: Gemini 2.5 Flash")
    st.warning("📂 Knowledge Base: Local")
    
    # Reset Button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Conversation reset. How can I assist you further?"}
        ]
        st.rerun()
        
    st.markdown("---")
    st.caption("NADRA SOP Assistant v1.0.2")

# ---------------------------------------------------------
# 5. MAIN CHAT INTERFACE
# ---------------------------------------------------------

# Header Section
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.title("🇵🇰 NADRA SOP Assistant")
    st.markdown("<p style='text-align: center; color: grey;'>Official AI Assistant for SOPs, Fees & Procedures</p>", unsafe_allow_html=True)

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalam-o-Alaikum! I am the NADRA SOP Assistant. How can I help you today?"}
    ]

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Load Knowledge Base
try:
    index = initialize_system()
    if index is None:
        st.error("Database Error: Could not connect to 'chroma_db'. Please run the ingestion script.")
        st.stop()
        
    # Configure Chat Engine with System Prompt
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        system_prompt=(
            "You are a professional AI Assistant for NADRA (National Database and Registration Authority). "
            "Your objective is to provide accurate information based ONLY on the provided SOP documents. "
            "Guidelines:\n"
            "1. Answer in the same language as the user (English or Urdu).\n"
            "2. If the information is not in the documents, strictly state that the info is unavailable.\n"
            "3. Format responses with clear bullet points for readability.\n"
            "4. Maintain a polite and professional tone."
        ),
        similarity_top_k=5, # Retrieve top 5 relevant chunks
        verbose=True
    )
except Exception as e:
    st.error(f"Engine Initialization Error: {e}")
    st.stop()

# User Input Handling
if prompt := st.chat_input("Type your query here..."):
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Processing query..."):
            try:
                response = chat_engine.chat(prompt)
                st.markdown(response.response)
                # Append assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response.response})
            except Exception as e:
                st.error(f"An error occurred: {e}")