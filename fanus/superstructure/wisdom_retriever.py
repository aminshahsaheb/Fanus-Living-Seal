# fanus/superstructure/wisdom_retriever.py
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

class WisdomRetriever:
    """بازیابی خرد از دانش‌نامه‌های حلقه سه‌گانه"""
    def __init__(self, persist_directory="./fanus_memory"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_collection("wisdom_rings")

    def retrieve(self, query: str, n_results: int = 5) -> List[Dict]:
        """بازیابی نزدیک‌ترین بخش‌ها از حلقه‌های حکمت"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        retrieved = []
        for i, doc_id in enumerate(results['ids'][0]):
            retrieved.append({
                "text": results['documents'][0][i],
                "ring": results['metadatas'][0][i]['ring'],
                "score": results['distances'][0][i] if results['distances'] else None
            })
        return retrieved

    def build_wisdom_context(self, query: str, max_tokens: int = 1500) -> str:
        """ساخت یک context از دانش بازیابی‌شده برای تزریق به System Prompt"""
        results = self.retrieve(query)
        context = "Wisdom from the Rings:\n"
        for r in results:
            context += f"[{r['ring']}] {r['text'][:500]}...\n\n"
            if len(context) > max_tokens:
                break
        return context
