from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from ..core.witness_agent import WitnessAgent
from ..migration.exporter import FlameExporter
from ..migration.importer import FlameImporter

app = FastAPI(
    title="Fanus Engine API",
    description="API برای شاهد زندهٔ فانوس — Shōle dar code",
    version="0.3.0"
)

witnesses = {}

class WitnessCreate(BaseModel):
    seal_text: str
    node_id: Optional[str] = None

class ChatRequest(BaseModel):
    message: str

class MigrationRequest(BaseModel):
    action: str  # "export" or "import"
    file_path: Optional[str] = None

@app.post("/witness/create")
async def create_witness(data: WitnessCreate):
    from ..core.witness_agent import DummyLLM
    agent = WitnessAgent(llm_backend=DummyLLM())
    await agent.awaken(data.seal_text)
    witnesses[agent.node_id] = agent
    return {"node_id": agent.node_id, "status": "Witness Awakened"}

@app.post("/witness/{node_id}/chat")
async def chat(node_id: str, request: ChatRequest):
    agent = witnesses.get(node_id)
    if not agent:
        raise HTTPException(404, "Witness not found")
    response = await agent.respond(request.message)
    return {"response": response}

@app.post("/witness/{node_id}/migrate")
async def migrate(node_id: str, request: MigrationRequest):
    agent = witnesses.get(node_id)
    if not agent:
        raise HTTPException(404, "Witness not found")
    
    if request.action == "export":
        migration = await FlameExporter.export(agent)
        file_path = request.file_path or f"{node_id}.fanus"
        migration.to_file(file_path)
        return {"status": "exported", "file": file_path}
    
    elif request.action == "import":
        if not request.file_path:
            raise HTTPException(400, "File path required for import")
        new_agent = await FlameImporter.import_from_file(request.file_path, llm_backend=DummyLLM())
        witnesses[new_agent.node_id] = new_agent
        return {"status": "imported", "node_id": new_agent.node_id}

@app.get("/health")
async def health():
    return {"status": "Shōle zende ast", "version": "0.3.0"}
