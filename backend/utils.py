import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)
    return chunks

def process_pdf(file_path):
    print(f"Extracting text from {file_path}...")
    text = extract_text_from_pdf(file_path)
    print(f"Chunking text...")
    chunks = chunk_text(text)
    print(f"Done! Extracted {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # Construct path to the PDF relative to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "document.pdf")

    if os.path.exists(pdf_path):
        chunks = process_pdf(pdf_path)
        for i, chunk in enumerate(chunks):
            print(f"\n--- Chunk {i+1} ---\n{chunk}")
    else:
        print(f"Error: '{pdf_path}' not found. Please ensure 'document.pdf' is in the same directory as the script.")