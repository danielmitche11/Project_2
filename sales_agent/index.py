from pinecone import Pinecone
import os

key = os.getenv("PINECONE_API_KEY")
client = Pinecone(api_key = key)

def get_index(name):
    index = client.Index(name)
    return index