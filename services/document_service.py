from pathlib import Path

from loaders.document_loader import DocumentLoader
from rag.chunking_service import ChunkingService


class DocumentService:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = ChunkingService()

    def process_document(self, file_path):

        docs = self.loader.load(file_path)

        chunks = self.chunker.split_documents(docs)

        return docs, chunks

    def process_directory(self, directory):

        all_documents = []

        all_chunks = []

        for file in Path(directory).iterdir():

            if file.is_file():

                docs = self.loader.load(str(file))

                chunks = self.chunker.split_documents(docs)

                all_documents.extend(docs)

                all_chunks.extend(chunks)

        return all_documents, all_chunks