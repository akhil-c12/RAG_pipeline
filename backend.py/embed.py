from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH="vector_store"

def create_vector_store(chunks):
    embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store=FAISS.from_texts(texts=chunks,embedding=embeddings)
    os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
    vector_store.save_local(FAISS_INDEX_PATH)
    return vector_store

