from fastapi import FastAPI
import chromadb
import ollama
import uuid

app = FastAPI()
client = chromadb.PersistentClient(path="./db")
collection = client.get_collection("docs")

@app.get("/")
def welcome():
    return {"message":"Welcome to FastAPI"}

@app.post("/query")
def queryChroma(query: str):
    results = collection.query(query_texts=[query], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""
    
    answer = ollama.generate(
        model="tinyllama",
        prompt=f"""
        Context:
        {context}
        
        
        Question:
        {query}
        
        Answer clearly and precisely:
        """
    )
    
    return {"answer": answer["response"]}

@app.post("/add")
def addKnowledge(text: str):
    collection.add(documents=[text], ids=[uuid.UUID])
    return {"status":"ok"}