from fastapi import APIRouter
from pydantic import BaseModel
from fanus.audit.audit_engine import AuditEngine
from fanus.adapters.knowledge_gateway import KnowledgeGateway
from fanus.api.auth import verify_api_key
from fastapi import Depends

router = APIRouter(prefix="/verify", tags=["verify"])

audit = AuditEngine()
gateway = KnowledgeGateway()


class VerifyRequest(BaseModel):
    prompt: str
    response: str
    context: str = ""


class VerifyDeepRequest(BaseModel):
    prompt: str
    response: str


@router.post("")
def verify(req: VerifyRequest, _: bool = Depends(verify_api_key)):
    result = audit.verify(req.prompt, req.response, req.context)
    return result


@router.post("/deep")
def verify_deep(req: VerifyDeepRequest, _: bool = Depends(verify_api_key)):
    knowledge = gateway.search_all(req.prompt, limit=3)
    sources_text = ""
    for source, items in knowledge.items():
        if isinstance(items, list) and items:
            sources_text += items[0].get("title", "") + " "
    result = audit.verify(req.prompt, req.response, sources_text)
    result["deep"] = True
    result["knowledge_sources"] = knowledge
    return result
