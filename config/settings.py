from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

APP_NAME = "Enterprise Knowledge Assistant"

CHROMA_DB_PATH = "chroma_db"

UPLOAD_FOLDER = "uploads"

DATA_FOLDER = "data"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

COLLECTION_NAME = "enterprise_documents"

