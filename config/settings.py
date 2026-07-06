from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

APP_NAME = "Enterprise Knowledge Assistant"

CHROMA_DB_PATH = "chroma_db"

UPLOAD_FOLDER = "uploads"

DATA_FOLDER = "data"

EMBEDDING_MODEL = "text-embedding-3-small"

COLLECTION_NAME = "enterprise_documents"

