import streamlit as st
from pathlib import Path

from config.settings import APP_NAME, GROQ_API_KEY
from loaders.document_loader import DocumentLoader
from rag.chunking_service import ChunkingService
from rag.embedding_service import EmbeddingService
from rag.vector_store import VectorStore
from rag.retriever import RetrieverService

# -------------------------------------------------------
# Streamlit Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Knowledge Assistant")

st.markdown("---")

# -------------------------------------------------------
# API Key Validation
# -------------------------------------------------------

if GROQ_API_KEY:
    st.success("✅ Groq API Key Loaded Successfully")
else:
    st.error("❌ Groq API Key Not Found")
    st.stop()

# -------------------------------------------------------
# Load PDF
# -------------------------------------------------------

pdf_path = Path("data") / "HRPolicy.pdf"

st.subheader("Step 1 : Document Loading")

st.write("Current Working Directory")

st.code(str(Path.cwd()))

st.write("PDF Exists :", pdf_path.exists())

if not pdf_path.exists():

    st.error("HRPolicy.pdf not found inside data folder")

    st.stop()

loader = DocumentLoader()

documents = loader.load(str(pdf_path))

st.success(f"Loaded {len(documents)} Document(s)")

# Preview

with st.expander("Document Preview"):

    st.write(documents[0].page_content[:1000])

    st.write(documents[0].metadata)

# -------------------------------------------------------
# Chunking
# -------------------------------------------------------

st.subheader("Step 2 : Chunking")

chunk_service = ChunkingService()

chunks = chunk_service.split_documents(documents)

st.success(f"Total Chunks Created : {len(chunks)}")

with st.expander("Chunk Preview"):

    st.write(chunks[0].page_content)

    st.write(chunks[0].metadata)

# -------------------------------------------------------
# Embedding Model
# -------------------------------------------------------

st.subheader("Step 3 : Embedding Model")

embedding_service = EmbeddingService()

embedding_model = embedding_service.get_embedding_model()

st.success("Embedding Model Loaded Successfully")

vector = embedding_model.embed_query(
    chunks[0].page_content
)

st.write("Embedding Dimension :", len(vector))

# -------------------------------------------------------
# ChromaDB
# -------------------------------------------------------

st.subheader("Step 4 : Vector Database")

vector_store = VectorStore(embedding_model)

db = vector_store.create_vector_store(chunks)

st.success("Vector Database Created Successfully")

collection = db.get()

st.write(
    "Stored Documents :",
    len(collection["documents"])
)

# -------------------------------------------------------
# Retriever
# -------------------------------------------------------

st.subheader("Step 5 : Semantic Search")

retriever = RetrieverService(db)

question = st.text_input(
    "Ask your question"
)

if question:

    results = retriever.similarity_search(question)

    st.success(f"{len(results)} Relevant Documents Found")

    for index, doc in enumerate(results):

        st.markdown(f"## Result {index+1}")

        st.write(doc.page_content)

        st.write(doc.metadata)

        st.divider()