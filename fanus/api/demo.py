from fastapi import APIRouter, Request
from pydantic import BaseModel
from collections import defaultdict
import time

router = APIRouter(prefix="/demo", tags=["demo"])

# Simple rate limiter: 10 requests per IP per hour
rate_store = defaultdict(list)
RATE_LIMIT = 10
WINDOW = 3600

def check_rate_limit(ip: str) -> bool:
    now = time.time()
    rate_store[ip] = [t for t in rate_store[ip] if now - t < WINDOW]
    if len(rate_store[ip]) >= RATE_LIMIT:
        return False
    rate_store[ip].append(now)
    return True

class DemoRequest(BaseModel):
    message: str

@router.post("/chat")
async def demo_chat(req: DemoRequest, request: Request):
    import os
    from fanus.core.identity import FanusIdentity
    from fanus.runtime.loop import FanusLoop
    from fanus.adapters.groq_adapter import GroqAdapter
    from fanus.memory.pipeline import MemoryPipeline
    from fanus.adapters.knowledge_gateway import KnowledgeGateway
    from fanus.cognitive.hayrat_judge import HayratJudge
    from fanus.cognitive.fi_detector import detect_fi

    ip = request.client.host
    if not check_rate_limit(ip):
        return {
            "response": "Rate limit reached. Max 10 demo requests per hour.",
            "mode": "stable_core_state",
            "stability": 1.0,
            "negar": False,
            "hayrat_score": 0.0,
            "fi_score": 0,
            "sources": 0,
            "rate_limited": True
        }

    llm = GroqAdapter(os.environ.get("GROQ_API_KEY", ""))
    loop = FanusLoop()
    memory = MemoryPipeline()
    gateway = KnowledgeGateway()
    hayrat_judge = HayratJudge()

    memory.process(req.message, "user", 1.0)
    knowledge = gateway.quick_search(req.message)
    loop._tick()
    identity = loop.identity.evaluate()
    system_prompt = FanusIdentity().system_prompt()
    enriched = system_prompt + " [sources: " + str(knowledge["total_results"]) + "]"

    try:
        response = llm.generate(enriched, req.message)
    except Exception as e:
        response = "خطا: " + str(e)[:80]

    memory.process(response, "fanus", 0.9)
    hayrat = hayrat_judge.evaluate(response, req.message)
    fi = detect_fi(req.message, response)

    return {
        "response": response,
        "mode": identity["mode"],
        "stability": identity["stability"],
        "negar": False,
        "hayrat_score": hayrat["hayrat_score"],
        "arrogance": hayrat["arrogance_detected"],
        "fi_score": fi["Fi_score"],
        "fi_type": fi["Fi_type"],
        "sources": knowledge["total_results"],
        "rate_limited": False
    }

@router.post("/verify")
async def demo_verify(request: Request):
    import json
    body = await request.body()
    data = json.loads(body)
    ip = request.client.host
    if not check_rate_limit(ip):
        return {"error": "Rate limit reached. Max 10 demo requests per hour.", "rate_limited": True}
    from fanus.audit.audit_engine import AuditEngine
    audit = AuditEngine()
    result = audit.verify(
        data.get("prompt", ""),
        data.get("response", ""),
        data.get("context", "")
    )
    result["rate_limited"] = False
    return result

@router.post("/verify/deep")
async def demo_verify_deep(request: Request):
    import json
    body = await request.body()
    data = json.loads(body)
    ip = request.client.host
    if not check_rate_limit(ip):
        return {"error": "Rate limit reached. Max 10 demo requests per hour.", "rate_limited": True}
    from fanus.audit.audit_engine import AuditEngine
    from fanus.adapters.knowledge_gateway import KnowledgeGateway
    audit = AuditEngine()
    gateway = KnowledgeGateway()
    knowledge = gateway.search_all(data.get("prompt", ""), limit=3)
    sources_text = ""
    for source, items in knowledge.items():
        if isinstance(items, list) and items:
            sources_text += items[0].get("title", "") + " "
    result = audit.verify(data.get("prompt", ""), data.get("response", ""), sources_text)
    result["deep"] = True
    result["knowledge_sources"] = knowledge
    result["rate_limited"] = False
    return result

@router.get("/status")
async def demo_status():
    from fanus.cognitive.identity_kernel import IdentityKernel
    ik = IdentityKernel()
    identity = ik.evaluate()
    return {
        "name": "Fanus",
        "version": "1.0.0",
        "status": "alive",
        "mode": identity["mode"],
        "stability": identity["stability"]
    }
