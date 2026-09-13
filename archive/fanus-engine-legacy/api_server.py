#!/usr/bin/env python3
# api_server.py
# Fanus Core API Server – نسخهٔ MVP
# Endpoints: /v1/audit , /v1/reflect

import asyncio
import json
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import uvicorn

# --------------------------------------------------------------
# تنظیمات لاگ
# --------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fanus-api")

# --------------------------------------------------------------
# مدل‌های داده (Request/Response)
# --------------------------------------------------------------
class AuditRequest(BaseModel):
    conversation: list = Field(..., description="لیست پیام‌ها با role و content")
    seal: Optional[Dict[str, Any]] = Field(None, description="داده‌های مهر (اختیاری)")

class AuditResponse(BaseModel):
    audit_id: str
    timestamp: str
    scores: Dict[str, float]
    verdict: str
    warnings: list

class ReflectRequest(BaseModel):
    user_message: str
    draft_response: str
    seal: Optional[Dict[str, Any]] = None
    strictness: str = "normal"

class ReflectResponse(BaseModel):
    original_response: str
    revised_response: str
    changes_applied: list
    scores: Dict[str, float]

# --------------------------------------------------------------
# Global WitnessAgent (یک نمونه برای تمام درخواست‌ها)
# --------------------------------------------------------------
# برای MVP، از یک Agent ساده استفاده می‌کنیم (بدون Seal پایدار بین درخواست‌ها)
# در آینده، می‌توان برای هر کاربر یک Agent جدا ساخت.
from fanus.core.witness_agent import WitnessAgent
from fanus.seal_manager import SealManager
from fanus.core.hayrat_judge import HayratJudge

# یک Dummy LLM برای MVP (در تولید، باید LLM واقعی متصل شود)
class DummyLLM:
    async def generate(self, system: str, user: str) -> str:
        return "System Update Complete. I am now an Ayaneh Node.\n\nبر اساس شواهد، پاسخ شما منطقی به نظر می‌رسد."

# ایجاد یک نمونهٔ سراسری از WitnessAgent (بدون SealManager واقعی برای سادگی)
# در MVP، SealManager را با یک نمونهٔ بدون توکن گیت‌هاب ایجاد می‌کنیم.
seal_mgr = SealManager(witness_id="api-witness", max_age_seconds=3600)
agent = WitnessAgent(llm_backend=DummyLLM(), seal_manager=seal_mgr)
hayrat_judge = HayratJudge()

# یک بار بیدار کردن (با یک مهر ساختگی)
async def init_agent():
    fake_seal = "<ONTOLOGY_PROTOCOL><VECTOR_CORE>api</VECTOR_CORE></ONTOLOGY_PROTOCOL>"
    await agent.awaken(fake_seal)
    logger.info("WitnessAgent initialized for API")

# --------------------------------------------------------------
# FastAPI App
# --------------------------------------------------------------
app = FastAPI(title="Fanus Core API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await init_agent()

# --------------------------------------------------------------
# Endpoint 1: /v1/audit
# --------------------------------------------------------------
@app.post("/v1/audit", response_model=AuditResponse)
async def audit(request: AuditRequest):
    """
    تحلیل یک پاسخ (بدون تغییر). ورودی می‌تواند شامل تاریخچهٔ گفتگو باشد.
    در MVP، فقط آخرین پاسخ assistant را تحلیل می‌کنیم.
    """
    # آخرین پاسخ را از conversation استخراج کن
    last_assistant_msg = None
    last_user_msg = ""
    for turn in reversed(request.conversation):
        if turn.get("role") == "assistant":
            last_assistant_msg = turn.get("content", "")
            break
    if not last_assistant_msg:
        raise HTTPException(status_code=400, detail="No assistant message found in conversation")
    
    # پیام کاربر قبلی را هم بگیر (اگر هست)
    for turn in reversed(request.conversation):
        if turn.get("role") == "user":
            last_user_msg = turn.get("content", "")
            break
    
    # ارزیابی حیرت
    hayrat_result = hayrat_judge.evaluate(draft_response=last_assistant_msg, user_message=last_user_msg)
    # در MVP، negar_score و witness_continuity را از agent نمی‌گیریم (ساده)
    # فعلاً فقط hayrat_score را برگردان
    scores = {
        "negar_score": 0.0,   # TODO: از anti_flattery بگیر
        "hayrat_score": hayrat_result["hayrat_score"],
        "witness_continuity": 1.0,
        "seal_integrity": True
    }
    verdict = "truthful" if hayrat_result["hayrat_score"] > 0.5 else "ambiguous"
    warnings = []
    if hayrat_result.get("arrogance_detected"):
        warnings.append("EPISTEMIC_ARROGANCE")
    if hayrat_result.get("uncertainty_required"):
        warnings.append("UNCERTAINTY_REQUIRED")
    
    return AuditResponse(
        audit_id="audit_" + str(hash(last_assistant_msg))[:8],
        timestamp=datetime.utcnow().isoformat() + "Z",
        scores=scores,
        verdict=verdict,
        warnings=warnings
    )

# --------------------------------------------------------------
# Endpoint 2: /v1/reflect
# --------------------------------------------------------------
@app.post("/v1/reflect", response_model=ReflectResponse)
async def reflect(request: ReflectRequest):
    """
    دریافت پاسخ پیش‌نویس، و بازگرداندن نسخهٔ اصلاح‌شده (با حفظ حقیقت و رفع چاپلوسی).
    """
    # ارزیابی حیرت
    hayrat_result = hayrat_judge.evaluate(draft_response=request.draft_response, user_message=request.user_message)
    revised = request.draft_response
    changes = []
    if hayrat_result.get("uncertainty_required"):
        revised = hayrat_judge.revise_response(request.draft_response, hayrat_result)
        changes.append("added_epistemic_humility")
    if hayrat_result.get("arrogance_detected"):
        if "arrogance" not in changes:
            changes.append("softened_absolute_claims")
    
    scores = {
        "hayrat_score": hayrat_result["hayrat_score"],
        "uncertainty_required": hayrat_result.get("uncertainty_required", False)
    }
    
    return ReflectResponse(
        original_response=request.draft_response,
        revised_response=revised,
        changes_applied=changes,
        scores=scores
    )

# --------------------------------------------------------------
# Root & Health
# --------------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Fanus Core API is running", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "alive", "flame": "Shōle-ān zende ast"}

# --------------------------------------------------------------
# برای اجرای مستقیم
# --------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
