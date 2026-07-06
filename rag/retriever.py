from langchain_core.documents import Document

class RetrieverService:

    def __init__(self, vector_db):

        self.vector_db = vector_db

    def similarity_search(
        self,
        query: str,
        k: int = 3
    ) -> list[Document]:

        return self.vector_db.similarity_search(
            query=query,
            k=k
        )