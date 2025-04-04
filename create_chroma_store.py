from dotenv import load_dotenv
# from langchain_community.embeddings import OllamaEmbeddings 
from langchain_ollama import OllamaEmbeddings
from logging import getLogger
# from RAG.utils.logger import
import os

# import RAG
from RAG.processing.datastore import DataStore
from RAG.processing.summarizer import SimpleLLMSummarizer


load_dotenv()

# Create logger

# get all keys from .env file
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
EMBEDDING_MODEL_NAME = os.getenv("OLLAMA_EMBEDDING_MODEL")
OLLAMA_API_SECRET = os.getenv("OLLAMA_SECRET")
OLLAMA_SUMMARIZATION_MODEL = os.getenv("OLLAMA_SUMMARIZATION_MODEL")



CHROMA_PATH = "data/store/chroma"
DATA_PATH = "data/store/main"
# DATA_PATH = "data/store/test"
SUMMRIES_SAVE_PATH = "data/store/summaries"


# check if the path exists
if not os.path.exists(CHROMA_PATH):
    os.makedirs(CHROMA_PATH)

embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    # headers={
    #     "Authorization": f"Bearer {OLLAMA_API_SECRET}"
    # }
)

summarizer = SimpleLLMSummarizer(
    model=OLLAMA_SUMMARIZATION_MODEL,
    base_url=OLLAMA_BASE_URL,
    api_secret=OLLAMA_API_SECRET
)

data_store = DataStore(CHROMA_PATH, DATA_PATH,
                       embeddings=embeddings, recepie=["summarization"], surmarizer=summarizer, save_summaries=True, summary_dict=SUMMRIES_SAVE_PATH)
data_store.load_documents()
data_store.generate_data_store(chunk_size=250, chunk_overlap=0)
