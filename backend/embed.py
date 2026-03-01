from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

EMBEDDING_MODEL="sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX_PATH="vector_store"

def create_vector_store(chunks,filename):
    embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store=FAISS.from_texts(texts=chunks,embedding=embeddings,metadatas=[{"source":filename}for _ in chunks])
    if os.path.exists(FAISS_INDEX_PATH):
        existing_store=FAISS.load_local(FAISS_INDEX_PATH,embeddings,allow_dangerous_deserialization=True)
        existing_store.merge_from(vector_store)
        existing_store.save_local(FAISS_INDEX_PATH)
        return existing_store
    else:
        os.makedirs(FAISS_INDEX_PATH,exist_ok=True)
        vector_store.save_local(FAISS_INDEX_PATH)
        return vector_store

def load_vector_store():
    embeddings=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

