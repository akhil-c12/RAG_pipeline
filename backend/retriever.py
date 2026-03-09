from embed import load_vector_store
import os

vector_store=None

def get_vector_store():
    global vector_store
    if vector_store is None:
        if not os.path.exists("vector_store"):
            raise FileNotFoundError("Vector store not found. Please upload a PDF first.")
        vector_store = load_vector_store()
    return vector_store

def get_retriever(k=5):
    vs = get_vector_store()
    retriever = vs.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    return retriever

def retrieve_chunks(query: str, k=5):
    if not os.path.exists("vector_store"):
        raise FileNotFoundError("Vector store not found. Please upload a PDF first.")
    retriever = get_retriever(k)
    docs = retriever.invoke(query)
    return docs