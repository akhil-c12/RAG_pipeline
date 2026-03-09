import requests
from retriever import retrieve_chunks
def rag_chat(query,retriever):
    docs=retriever(query)
    
    context="\n\n".join([doc.page_content for doc in docs])
    
    prompt=f"""
You are a helpful AI assistant.

Use ONLY the context below to answer.
If the answer is not in the context, say "I don't know."
Context:
{context}
Question:

{query}
Answer:
"""
    response=requests.post(
     "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "model": "google/gemma-3-4b",
            "messages": [
                {"role": "system", "content": "You are a precise AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
)

    return response.json()["choices"][0]["message"]["content"]
    