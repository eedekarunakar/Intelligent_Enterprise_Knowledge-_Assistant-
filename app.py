import streamlit as st
from pathlib import Path

from config.settings import APP_NAME, GROQ_API_KEY

from services.document_service import DocumentService
from services.vector_service import VectorService
from services.rag_service import RAGService

from rag.retriever import RetrieverService
from rag.chat_service import ChatService

# -------------------------------------------------------
# Streamlit Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.title("🤖 Enterprise Knowledge Assistant")
st.markdown("---")

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

st.sidebar.title("⚙️ Settings")

st.sidebar.success("Enterprise RAG Application")

if GROQ_API_KEY:
    st.sidebar.success("✅ Groq Connected")
else:
    st.sidebar.error("❌ Groq API Key Missing")
    st.stop()

# -------------------------------------------------------
# Document Path
# -------------------------------------------------------

pdf_path = Path("data") / "HRPolicy.pdf"

if not pdf_path.exists():
    st.error("HRPolicy.pdf not found inside data folder.")
    st.stop()

# -------------------------------------------------------
# Document Service
# -------------------------------------------------------

st.header("📄 Document Processing")

document_service = DocumentService()

documents, chunks = document_service.process_document(
    str(pdf_path)
)

st.success(f"Loaded Documents : {len(documents)}")

st.success(f"Generated Chunks : {len(chunks)}")

with st.expander("Preview Chunk"):

    st.write(chunks[0].page_content)

    st.json(chunks[0].metadata)

# -------------------------------------------------------
# Vector Service
# -------------------------------------------------------

st.header("🧠 Embedding & Vector Database")

vector_service = VectorService()

embedding_model = vector_service.get_embedding_model()

vector = embedding_model.embed_query(
    chunks[0].page_content
)

st.success("Embedding Model Loaded")

st.write("Embedding Dimension :", len(vector))

db = vector_service.build_vector_store(chunks)

st.success("Vector Database Created")

collection = db.get()

st.write("Stored Chunks :", len(collection["documents"]))

# -------------------------------------------------------
# Retriever
# -------------------------------------------------------

retriever = RetrieverService(db)

# -------------------------------------------------------
# Chat Service
# -------------------------------------------------------

chat_service = ChatService()

# -------------------------------------------------------
# RAG Service
# -------------------------------------------------------

rag_service = RAGService(
    retriever=retriever,
    chat_service=chat_service
)

# -------------------------------------------------------
# Ask Questions
# -------------------------------------------------------

st.header("💬 Ask Questions")

question = st.text_input(
    "Ask anything about the uploaded document..."
)

if question:

    with st.spinner("Searching Knowledge Base..."):

        answer, sources = rag_service.ask(question)

        retrieved_docs = retriever.similarity_search(question)

    st.subheader("🤖 AI Answer")

    st.success(answer)

    st.subheader("📚 Sources")

    for source in sources:
        st.write(f"📄 {source}")

    with st.expander("Retrieved Chunks"):

        st.success(
            f"{len(retrieved_docs)} Chunk(s) Retrieved"
        )

        for i, doc in enumerate(retrieved_docs):

            st.markdown(f"### Chunk {i+1}")

            st.write(doc.page_content)

            st.json(doc.metadata)

            st.divider()

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.markdown("---")

st.caption(
    "Enterprise Knowledge Assistant | LangChain • HuggingFace • ChromaDB • Groq"
)