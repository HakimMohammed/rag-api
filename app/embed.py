'''
This file is responsible for converting our txt file into vectors to be stored in ChromaDB.
Those vectors will be later used as context by our local LLM.
'''

import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

with open("app/k8s.txt", "r") as file:
    text = file.read()

collection.add(documents=[text], ids=["k8s"])

print("Embedding stored in chroma")