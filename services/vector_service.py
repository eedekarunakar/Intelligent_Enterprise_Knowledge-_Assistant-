from rag.embedding_service import EmbeddingService
from rag.vector_store import VectorStore


class VectorService:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.embedding_model = self.embedding_service.get_embedding_model()

    def build_vector_store(self, chunks):
        vector_store = VectorStore(self.embedding_model)
        return vector_store.create_vector_store(chunks)

    def get_embedding_model(self):
        return self.embedding_model