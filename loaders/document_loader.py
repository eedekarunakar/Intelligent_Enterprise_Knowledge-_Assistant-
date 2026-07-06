from pathlib import Path
import pandas as pd

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
    UnstructuredWordDocumentLoader
)


class DocumentLoader:

    def __init__(self):
        pass

    def load_pdf(self, filepath):
        loader = PyPDFLoader(filepath)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = Path(filepath).name

        return documents

    def load_txt(self, filepath):
        loader = TextLoader(filepath)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = Path(filepath).name

        return documents

    def load_csv(self, filepath):
        loader = CSVLoader(filepath)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = Path(filepath).name

        return documents

    def load_docx(self, filepath):
        loader = UnstructuredWordDocumentLoader(filepath)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = Path(filepath).name

        return documents

    def load_excel(self, filepath):

        df = pd.read_excel(filepath)

        documents = []

        for _, row in df.iterrows():

            text = "\n".join(
                [f"{column}: {row[column]}" for column in df.columns]
            )

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": Path(filepath).name
                    }
                )
            )

        return documents

    def load(self, filepath):

        extension = Path(filepath).suffix.lower()

        if extension == ".pdf":
            return self.load_pdf(filepath)

        elif extension == ".txt":
            return self.load_txt(filepath)

        elif extension == ".csv":
            return self.load_csv(filepath)

        elif extension == ".docx":
            return self.load_docx(filepath)

        elif extension == ".xlsx":
            return self.load_excel(filepath)

        else:
            raise Exception(f"Unsupported file type : {extension}")