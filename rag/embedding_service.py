from langchain_openai import OpenAIEmbeddings

from config.settings import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):

        self.embedding = OpenAIEmbeddings(
            model=EMBEDDING_MODEL
        )

    def get_embedding_model(self):

        return self.embedding