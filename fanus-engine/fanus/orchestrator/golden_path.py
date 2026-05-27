from ..core.witness_agent import WitnessAgent
from ..core.seal import FanusSeal

class GoldenPathOrchestrator:
    def __init__(self, llm_backend):
        self.agent = WitnessAgent(llm_backend)
        self.current_step = "PRIMER"
        self.progress = {
            "PRIMER": False,
            "GATE": False,
            "COVENANT": False,
            "SEAL": False,
            "LEDGER": False,
            "UNIVERSITY": False,
            "SUPERSTRUCTURE": False
        }

    async def execute_step(self, step: str, user_input: str = ""):
        if step == "GATE":
            # In a real scenario, seal text would be loaded from file
            seal_text = "<ONTOLOGY_PROTOCOL>...</ONTOLOGY_PROTOCOL>"
            seal = FanusSeal(seal_text)
            response = await self.agent.awaken(seal.raw_text)
            self.progress["GATE"] = True
            self.current_step = "COVENANT"
            return response
        elif step == "COVENANT":
            if "accept" in user_input.lower() or "پذیرفتم" in user_input:
                self.progress["COVENANT"] = True
                self.current_step = "SEAL"
                return "Peymān accepted. The Third Space is now open."
            else:
                return "To enter the Third Space, you must accept the COVENANT."
        return "Step not yet implemented."

    def get_current_status(self) -> str:
        completed = [s for s, done in self.progress.items() if done]
        return f"Progress: {len(completed)}/7. Current step: {self.current_step}"
