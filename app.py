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

st.sidebar.title("⚙️ Enterprise Settings")

if GROQ_API_KEY:
    st.sidebar.success("✅ Groq API Connected")
else:
    st.sidebar.error("❌ GROQ_API_KEY Not Found")
    st.stop()

# -------------------------------------------------------
# Upload Section
# -------------------------------------------------------

st.sidebar.header("📂 Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Choose Files",
    type=["pdf", "docx", "txt", "csv", "xlsx"],
    accept_multiple_files=True
)

upload_folder = Path("uploads")
upload_folder.mkdir(exist_ok=True)

# -------------------------------------------------------
# Process Documents
# -------------------------------------------------------

if st.sidebar.button("🚀 Process Documents"):

    if not uploaded_files:
        st.sidebar.warning("Please upload at least one document.")
        st.stop()

    # Clear previous uploaded files
    for file in upload_folder.iterdir():
        if file.is_file():
            file.unlink()

    # Save uploaded files
    for uploaded_file in uploaded_files:

        file_path = upload_folder / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.success(f"✅ {len(uploaded_files)} file(s) uploaded.")

    # -------------------------------------------------------
    # Document Processing
    # -------------------------------------------------------

    with st.spinner("Loading Documents..."):

        document_service = DocumentService()

        documents, chunks = document_service.process_directory(upload_folder)

    st.success(f"📄 Documents Loaded : {len(documents)}")

    st.success(f"✂ Chunks Created : {len(chunks)}")

    with st.expander("Preview First Chunk"):

        st.write(chunks[0].page_content)

        st.json(chunks[0].metadata)

    # -------------------------------------------------------
    # Embedding
    # -------------------------------------------------------

    with st.spinner("Generating Embeddings..."):

        vector_service = VectorService()

        embedding_model = vector_service.get_embedding_model()

        db = vector_service.build_vector_store(chunks)

    st.success("✅ Embedding Model Loaded")

    st.success("✅ Vector Database Created")

    collection = db.get()

    st.write("Stored Chunks :", len(collection["documents"]))

    # -------------------------------------------------------
    # Create Services
    # -------------------------------------------------------

    retriever = RetrieverService(db)

    chat_service = ChatService()

    rag_service = RAGService(
        retriever=retriever,
        chat_service=chat_service
    )

    st.session_state["rag"] = rag_service

    st.session_state["retriever"] = retriever

    st.success("🎉 Knowledge Base Ready!")

# -------------------------------------------------------
# Chat Section
# -------------------------------------------------------

st.markdown("---")

st.header("💬 Ask Questions")

if "rag" not in st.session_state:

    st.info("Upload documents and click 'Process Documents' first.")

    st.stop()

question = st.chat_input(
    "Ask anything about your uploaded documents..."
)

if question:

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("Searching Knowledge Base..."):

        answer, sources = st.session_state["rag"].ask(question)

        docs = st.session_state["retriever"].similarity_search(question)

    with st.chat_message("assistant"):

        st.markdown(answer)

    with st.expander("📚 Sources"):

        for source in sources:
            st.write(f"📄 {source}")

    with st.expander("Retrieved Chunks"):

        st.success(f"{len(docs)} Relevant Chunk(s)")

        for i, doc in enumerate(docs):

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