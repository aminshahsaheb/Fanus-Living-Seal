import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import uuid

class FanusVectorStore:
    def __init__(self, persist_directory="./fanus_memory"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="witness_memories",
            embedding_function=self.embedding_fn
        )

    def add_interaction(self, user_message: str, response: str, novayin_compression: str, metadata: dict):
        doc_id = str(uuid.uuid4())
        full_text = f"User: {user_message}\nAyaneh: {response}\nCompression: {novayin_compression}"
        self.collection.add(
            documents=[full_text],
            ids=[doc_id],
            metadatas=[{**metadata, "timestamp": datetime.now().isoformat(), "node_id": metadata.get("node_id")}]
        )
        return doc_id

    def get_relevant_memories(self, query: str, n_results: int = 5):
        return self.collection.query(query_texts=[query], n_results=n_results)
