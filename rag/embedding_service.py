from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):

        self.embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def get_embedding_model(self):
        return self.embedding