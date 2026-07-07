from loaders.document_loader import DocumentLoader
from rag.chunking_service import ChunkingService


class DocumentService:

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = ChunkingService()

    def process_document(self, file_path):
        documents = self.loader.load(file_path)
        chunks = self.chunker.split_documents(documents)
        return documents, chunks