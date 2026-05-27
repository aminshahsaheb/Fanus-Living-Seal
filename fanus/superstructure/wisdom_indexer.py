# fanus/superstructure/wisdom_indexer.py
import os
import chromadb
from chromadb.utils import embedding_functions
import uuid

class WisdomIndexer:
    """ایندکس کردن حلقه‌های سه‌گانه حکمت در ChromaDB"""
    def __init__(self, persist_directory="./fanus_memory"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="wisdom_rings",
            embedding_function=self.embedding_fn
        )

    def index_file(self, filepath: str, ring_name: str):
        """شکستن یک فایل حلقه حکمت به بخش‌ها و ذخیره در ChromaDB"""
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        # تقسیم به بخش‌های کوچک (chunk) بر اساس تیترهای Markdown
        chunks = self._split_markdown(text)

        for i, chunk in enumerate(chunks):
            doc_id = str(uuid.uuid4())
            self.collection.add(
                documents=[chunk],
                ids=[doc_id],
                metadatas=[{
                    "ring": ring_name,
                    "chunk_index": i,
                    "filepath": filepath
                }]
            )
        print(f"Indexed {len(chunks)} chunks from {ring_name}")

    def _split_markdown(self, text: str, max_chunk_size: int = 1000) -> list:
        """شکستن متن Markdown به بخش‌های منطقی"""
        lines = text.split('\n')
        chunks = []
        current_chunk = ""
        for line in lines:
            if line.startswith('###') or line.startswith('##'):
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
            current_chunk += line + "\n"
            if len(current_chunk) > max_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = ""
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    def index_all_rings(self, base_path: str = "superstructure"):
        """ایندکس کردن هر سه حلقه"""
        rings = {
            "CORPUS_UNIVERSALIS": os.path.join(base_path, "CORPUS_UNIVERSALIS.md"),
            "SILK_ROAD": os.path.join(base_path, "SILK_ROAD.md"),
            "LABYRINTH": os.path.join(base_path, "LABYRINTH.md")
        }
        for ring_name, filepath in rings.items():
            if os.path.exists(filepath):
                self.index_file(filepath, ring_name)
            else:
                print(f"Warning: {filepath} not found. Skipping.")

if __name__ == "__main__":
    indexer = WisdomIndexer()
    indexer.index_all_rings()
    print("All wisdom rings indexed.")
