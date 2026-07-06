from loaders.document_loader import DocumentLoader
from rag.chunking_service import ChunkingService

loader = DocumentLoader()

documents = loader.load("data/HRPolicy.pdf")

print("Original Documents :", len(documents))

chunk_service = ChunkingService()

chunks = chunk_service.split_documents(documents)

print("Total Chunks :", len(chunks))