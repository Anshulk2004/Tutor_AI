from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
import os

def setup_rag():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    knowledge_base_path = os.path.join(os.path.dirname(__file__), "db/knowledge_base.json")
    with open(knowledge_base_path, "r") as f:
        documents = json.load(f)
    texts = [doc["content"] for doc in documents]
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store

def retrieve_context(query, vector_store):
    results = vector_store.similarity_search(query, k=3)
    return "\n".join([res.page_content for res in results])