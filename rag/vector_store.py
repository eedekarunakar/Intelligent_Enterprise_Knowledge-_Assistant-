from langchain_chroma import Chroma

from config.settings import (
    CHROMA_DB_PATH,
    COLLECTION_NAME
)


class VectorStore:

    def __init__(self, embedding_model):

        self.embedding_model = embedding_model

        self.vector_db = None

    def create_vector_store(self, chunks):

        self.vector_db = Chroma.from_documents(

            documents=chunks,

            embedding=self.embedding_model,

            collection_name=COLLECTION_NAME,

            persist_directory=CHROMA_DB_PATH

        )

        return self.vector_db

    def load_vector_store(self):

        self.vector_db = Chroma(

            collection_name=COLLECTION_NAME,

            embedding_function=self.embedding_model,

            persist_directory=CHROMA_DB_PATH

        )

        return self.vector_db