import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fanus.core.identity import FanusIdentity
from fanus.runtime.loop import FanusLoop
from fanus.adapters.groq_adapter import GroqAdapter
from fanus.memory.pipeline import MemoryPipeline
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.cognitive.orchestrator import CognitiveOrchestrator
from fanus.cognitive.negar_detector import NegarDetector

from fanus.api.knowledge import router as knowledge_router
from fanus.api.reasoning import router as reasoning_router
app = FastAPI(title="Fanus API", version="1.0.0")

app.include_router(knowledge_router)
app.include_router(reasoning_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = FanusIdentity().system_prompt()
loop = FanusLoop()
llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
memory = MemoryPipeline()
gateway = KnowledgeGateway()
orchestrator = CognitiveOrchestrator()
negar = NegarDetector()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"name": "Fanus", "version": "1.0.0", "status": "alive"}

@app.get("/status")
def status():
    identity = loop.identity.evaluate()
    return {
        "mode": identity["mode"],
        "stability": identity["stability"],
        "safety": not loop.hard_guard.locked,
        "memory_size": memory.ledger.size()
    }

@app.post("/chat")
def chat(req: ChatRequest):
    memory.process(req.message, "user", 1.0)
    knowledge = gateway.quick_search(req.message)
    loop._tick()
    identity = loop.identity.evaluate()
    enriched = SYSTEM_PROMPT + " [sources: " + str(knowledge["total_results"]) + "]"
    try:
        response = llm.generate(enriched, req.message)
    except Exception as e:
        response = "error: " + str(e)[:100]
    memory.process(response, "fanus", 0.9)
    negar_result = negar.analyze(response)
    return {
        "response": response,
        "mode": identity["mode"],
        "stability": identity["stability"],
        "negar": negar_result["is_negar"],
        "sources": knowledge["total_results"]
    }

@app.get("/memory")
def get_memory():
    return {"ledger": memory.ledger.get_all()[-10:]}

@app.get("/goals")
def get_goals():
    return {"goals": orchestrator.goals.active()}
