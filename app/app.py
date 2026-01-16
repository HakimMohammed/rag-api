from fastapi import FastAPI
import chromadb
import ollama
import uuid
import logging
import os

app = FastAPI()
client = chromadb.PersistentClient(path="./db")
collection = client.get_collection("docs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

MODEL_NAME = os.getenv("MODEL_NAME", "tinyllama")
logging.info(f"Using Model: {MODEL_NAME}")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
ollama_client = ollama.Client(host=OLLAMA_HOST)

use_mock = os.getenv("MOCK_MODE", "1") == "1"
logging.info(f"Mock Mode Activated: {use_mock}")

@app.get("/")
def welcome():
    return {"message":"Welcome to FastAPI"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/query")
def queryChroma(query: str):

    logging.info(f"/query asked: {query}")

    results = collection.query(query_texts=[query], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""
    
    if use_mock:
        return {"answer": context}
    else:
        try:
            answer = ollama_client.generate(
                model=MODEL_NAME,
                prompt=f"\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer clearly and precisely:"
            )

            return {"answer": answer["response"]}
        except Exception as e:
            return {"error": str(e)}

@app.post("/add")
def addKnowledge(text: str):
    """Add new content to the knowledge base dynamically."""
    
    logging.info(f"/add received new information: {text}")
    
    try:
        id = str(uuid.uuid4())
        collection.add(documents=[text], ids=[id])
        
        return {
            "status": "success",
            "message": "Knowledge Base has been updated",
            "id": id
        }
        
    except Exception as e:
        return {
            "status": "error", "message": str(e)
        }