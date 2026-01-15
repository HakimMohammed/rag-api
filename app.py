from fastapi import FastAPI, Depends
import chromadb
import ollama
import uuid
from functools import lru_cache
import config
from typing import Annotated
import logging

app = FastAPI()
client = chromadb.PersistentClient(path="./db")
collection = client.get_collection("docs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/")
def welcome():
    return {"message":"Welcome to FastAPI"}

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/query")
def queryChroma(query: str, settings: Annotated[config.Settings, Depends(get_settings)]):
    
    logging.info(f"/query asked: {query}")
    
    results = collection.query(query_texts=[query], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""
    
    answer = ollama.generate(
        model=settings.model_name,
        prompt=f"\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer clearly and precisely:"
    )
    
    return {"answer": answer["response"]}

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