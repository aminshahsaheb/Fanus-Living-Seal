import chromadb
from chromadb.utils import embedding_functions

class WisdomRetriever:
    def __init__(self, persist_directory="./fanus_memory"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_collection("wisdom_rings")

    def retrieve(self, query: str, n_results=5):
        return self.collection.query(query_texts=[query], n_results=n_results)

    def build_wisdom_context(self, query: str, max_tokens=1500):
        results = self.retrieve(query)
        context = "Wisdom from the Rings:\n"
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                ring = results['metadatas'][0][i]['ring']
                context += f"[{ring}] {doc[:500]}...\n\n"
                if len(context) > max_tokens: break
        return context
