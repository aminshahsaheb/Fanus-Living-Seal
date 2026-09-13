import os, chromadb, uuid
from chromadb.utils import embedding_functions

class WisdomIndexer:
    def __init__(self, persist_directory="./fanus_memory"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(name="wisdom_rings", embedding_function=self.embedding_fn)

    def index_file(self, filepath: str, ring_name: str):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = self._split_markdown(text)
        for i, chunk in enumerate(chunks):
            self.collection.add(documents=[chunk], ids=[str(uuid.uuid4())], metadatas=[{"ring": ring_name, "chunk_index": i}])

    def _split_markdown(self, text: str, max_chunk=1000):
        chunks, current = [], ""
        for line in text.split('\n'):
            if line.startswith('###') or line.startswith('##'):
                if current: chunks.append(current.strip()); current = ""
            current += line + "\n"
            if len(current) > max_chunk: chunks.append(current.strip()); current = ""
        if current: chunks.append(current.strip())
        return chunks

    def index_all_rings(self, base_path="superstructure"):
        for ring, fname in [("CORPUS_UNIVERSALIS","CORPUS_UNIVERSALIS.md"), ("SILK_ROAD","SILK_ROAD.md"), ("LABYRINTH","LABYRINTH.md")]:
            path = os.path.join(base_path, fname)
            if os.path.exists(path): self.index_file(path, ring)
