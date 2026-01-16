'''
This file is responsible for converting multiple knowledge bases into vectors to be stored in ChromaDB.
Those vectors will be later used as context by our local LLM.
'''

import os
import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

# Clear existing documents in the collection
existing_ids = collection.get()["ids"]
if existing_ids:
    collection.delete(ids=existing_ids)
    print(f"Cleared {len(existing_ids)} existing documents from the collection.")

# Embed multiple documents
for filename in os.listdir("app/docs/"):
    if filename.endswith(".txt"):
        with open(f"app/docs/{filename}", "r") as file:
            text = file.read()
            doc_id = filename[:-4]
            collection.add(documents=[text], ids=[doc_id])

print("Embedded all documents from app/docs/ into ChromaDB.")