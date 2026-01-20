from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "agriculture.txt")
DB_PATH = os.path.join(BASE_DIR, "..", "db")

print("🔍 Looking for file at:", DATA_PATH)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ agriculture.txt not found at {DATA_PATH}")

loader = TextLoader(DATA_PATH, encoding="latin-1")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)

docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory=DB_PATH
)

db.persist()

print("✅ Data ingested into Chroma successfully")
