import os
from embed import create_vector_store
from utils import extract_text_from_pdf, chunk_text, process_pdf
from retriever import retrieve_chunks

# Step 1 & 2: Load PDF + Chunk
PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.pdf")

if not os.path.exists(PDF_PATH):
    print(f" PDF not found at {PDF_PATH}. Please add a test.pdf to the backend folder.")
    exit()

chunks = process_pdf(PDF_PATH)
print(f" {len(chunks)} chunks ready\n")

# Step 3: Create Vector Store
print(" Embedding and saving to vector store...")
create_vector_store(chunks, filename="test.pdf")
print("Vector store created\n")

#  Step 4: Retrieve
query = "Give the Summary of document" 
print(f"🔍 Querying: '{query}'")
results = retrieve_chunks(query)

print(f"\n Top {len(results)} chunks retrieved:\n")
for i, doc in enumerate(results):
    print(f"--- Chunk {i+1} | Source: {doc.metadata['source']} ---")
    print(doc.page_content[:300])
    print()