import chromadb

# Use the new client creation method (no Settings needed unless you're customizing storage)
client = chromadb.PersistentClient(path=".chromadb")

collection = client.get_or_create_collection("chat_history")

def store_interaction(user_input, system_response):
    collection.add(
        documents=[system_response],
        metadatas=[{"user_input": user_input}],
        ids=[str(hash(user_input))]
    )

def get_all_chats():
    results = collection.get()
    return list(zip(results['metadatas'], results['documents']))
