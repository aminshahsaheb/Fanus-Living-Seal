from fastapi import APIRouter
from pydantic import BaseModel
from fanus.cognitive.contradiction_detector import ContradictionDetector
from fanus.cognitive.question_generator import QuestionGenerator
from fanus.cognitive.negar_detector import NegarDetector

router = APIRouter(prefix="/reason", tags=["reasoning"])

detector = ContradictionDetector()
generator = QuestionGenerator()
negar = NegarDetector()

class AnalyzeRequest(BaseModel):
    text: str

class ContradictRequest(BaseModel):
    claim_a: str
    claim_b: str
    source_a: str = "unknown"
    source_b: str = "unknown"

class HypothesizeRequest(BaseModel):
    topic: str
    belief_type: str = "HYPOTHESIS"
    confidence: float = 0.7

@router.post("/analyze")
def analyze(req: AnalyzeRequest):
    negar_result = negar.analyze(req.text)
    return {
        "negar": negar_result["is_negar"],
        "negar_score": negar_result["negar_score"],
        "flattery_score": negar_result["flattery_score"],
        "overconfidence_score": negar_result["overconfidence_score"]
    }

@router.post("/contradict")
def contradict(req: ContradictRequest):
    result = detector.check(req.claim_a, req.claim_b, req.source_a, req.source_b)
    return result

@router.post("/hypothesize")
def hypothesize(req: HypothesizeRequest):
    result = generator.generate(req.topic, req.belief_type, req.confidence)
    return result

@router.get("/stats")
def stats():
    return {
        "contradictions": detector.stats(),
        "questions": generator.stats(),
        "negar": negar.stats()
    }
