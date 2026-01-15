from fastapi import FastAPI, Depends
import chromadb
import ollama
import uuid
from functools import lru_cache
import config
from typing import Annotated

app = FastAPI()
client = chromadb.PersistentClient(path="./db")
collection = client.get_collection("docs")

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/")
def welcome():
    return {"message":"Welcome to FastAPI"}

@app.post("/query")
def queryChroma(query: str, settings: Annotated[config.Settings, Depends(get_settings)]):
    results = collection.query(query_texts=[query], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""
    
    answer = ollama.generate(
        model=settings.model_name,
        prompt=f"\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer clearly and precisely:"
    )
    
    return {"answer": answer["response"]}

@app.post("/add")
def addKnowledge(text: str):
    collection.add(documents=[text], ids=[str(uuid.UUID)])
    return {"status":"ok"}