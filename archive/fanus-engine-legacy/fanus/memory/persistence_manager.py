from .vector_store import FanusVectorStore
from .cycle_compressor import CycleCompressor
from .ledger import Ledger

class PersistenceManager:
    def __init__(self, novayin_generator):
        self.vector_store = FanusVectorStore()
        self.compressor = CycleCompressor(novayin_generator)
        self.ledger = Ledger()
        self.current_threshold_question = None

    async def end_cycle(self, session_transcript: list, node_id: str) -> dict:
        compression_result = await self.compressor.compress_cycle(session_transcript)
        self.vector_store.add_interaction(
            user_message=session_transcript[-1]["content"] if session_transcript else "",
            response="",
            novayin_compression=compression_result["compression_text"],
            metadata={"node_id": node_id}
        )
        self.ledger.record_interaction(
            user_msg="",
            ayaneh_response="",
            compression=compression_result["compression_text"]
        )
        return compression_result
