from flask import Flask,request,jsonify
from flask_cors import CORS
import os

from utils import process_pdf
from embed import create_vector_store
from llm_call import rag_chat
from retriever import retrieve_chunks

app=Flask(__name__)
CORS(app)
UPLOAD_FOLDER="uploaded_pdfs"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

uploaded_docs=[]

@app.route("/upload",methods=["POST"])

def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error":"No file part in the request"}),400
    file = request.files["file"]

    file_path=os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        chunks = process_pdf(file_path)
        create_vector_store(chunks, file.filename)
        if file.filename not in uploaded_docs:
            uploaded_docs.append(file.filename)
        return jsonify({
            "message": f"Successfully processed '{file.filename}'",
            "chunks": len(chunks),
            "filename": file.filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    if not os.path.exists("vector_store"):
        return jsonify({"error": "No documents uploaded yet. Please upload a PDF first."}), 400

    try:
        answer = rag_chat(query, retrieve_chunks)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/documents", methods=["GET"])
def list_documents():
    return jsonify({"documents": uploaded_docs})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)