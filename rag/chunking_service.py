from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkingService:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200
    ):

        self.splitter = RecursiveCharacterTextSplitter(

            chunk_size=chunk_size,

            chunk_overlap=chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split_documents(self, documents):

        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):

            chunk.metadata["chunk_id"] = index + 1

        return chunks