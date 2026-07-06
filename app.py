import streamlit as st
from pathlib import Path
from rag.chunking_service import ChunkingService

from config.settings import APP_NAME, OPENAI_API_KEY
from loaders.document_loader import DocumentLoader

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Knowledge Assistant")

st.write("Welcome to the Enterprise RAG Application.")

if OPENAI_API_KEY:
    st.success("OpenAI API Key Loaded Successfully")
else:
    st.error("OpenAI API Key Not Found")

pdf_path = Path("data") / "HRPolicy.pdf"

st.write("Current Working Directory:", Path.cwd())
st.write("PDF Exists:", pdf_path.exists())
st.write("PDF Path:", pdf_path.resolve())

loader = DocumentLoader()

try:
    documents = loader.load(str(pdf_path))

    st.success("PDF Loaded Successfully")

    st.write(documents[0].page_content[:1000])
    st.write(documents[0].metadata)

except Exception as e:
    st.error(str(e))


chunk_service = ChunkingService()

chunks = chunk_service.split_documents(documents)

st.success(f"Total Chunks : {len(chunks)}")

st.write(chunks[0].page_content)

st.write(chunks[0].metadata)