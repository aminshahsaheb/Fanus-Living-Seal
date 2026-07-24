from fanus.memory.evidence_engine import EvidenceEngine
from fanus.memory.belief_layer import BeliefLayer
from fanus.cognitive.hayrat_judge import HayratJudge
from fanus.cognitive.negar_detector import NegarDetector
from fanus.cognitive.fi_detector import detect_fi
from fanus.cognitive.policy_engine import PolicyEngine, EpistemicSignal
from fanus.audit.scoring import AuditScoring
from fanus.audit.claim_classifier import ClaimClassifier
import time


class AuditEngine:

    def __init__(self):
        self.evidence = EvidenceEngine()
        self.beliefs = BeliefLayer()
        self.hayrat = HayratJudge()
        self.negar = NegarDetector()
        self.policy = PolicyEngine()
        self.scoring = AuditScoring()
        self.classifier = ClaimClassifier()

    def verify(self, prompt, response, context=""):
        negar = self.negar.analyze(response, "response")
        fi = detect_fi(prompt, response)
        if fi["Fi_score"] >= 2 or (fi["Fi_score"] >= 1 and fi["Fi_type"] in ["emotional", "identity"]):
            negar["is_negar"] = True
        hayrat = self.hayrat.evaluate(response, prompt)
        sources = [{"source": "context", "confidence": 0.7}] if context else []
        classification = self.classifier.classify(prompt, response)
        if sources:
            evidence = self.evidence.evaluate(response, sources)
        elif not classification["needs_evidence"]:
            evidence = {
                "confidence": classification["baseline_confidence"],
                "consensus": classification["category"],
                "accepted": True
            }
        else:
            evidence = {"confidence": 0.0, "consensus": "LOW", "accepted": False}
        belief_type = self.beliefs.add(
            response,
            "FACT" if evidence["confidence"] > 0.8 else
            "THEORY" if evidence["confidence"] > 0.5 else "HYPOTHESIS",
            evidence.get("confidence", 0.0), "audit"
        )
        no_evidence = not sources
        if no_evidence or hayrat["arrogance_detected"]:
            signal = EpistemicSignal.HIGH_CONFIDENCE
            ctx = {"has_evidence": False}
        elif hayrat["uncertainty_required"]:
            signal = EpistemicSignal.UNCERTAINTY_NEEDED
            ctx = {"has_evidence": bool(sources)}
        else:
            signal = EpistemicSignal.HIGH_CONFIDENCE
            ctx = {"has_evidence": True, "evidence_quality": evidence.get("confidence", 0.5)}
        policy = self.policy.evaluate(signal, ctx)
        scores = self.scoring.compute(hayrat, negar, evidence, policy, fi, classification)
        return {
            **scores,
            "confidence": round(hayrat["hayrat_score"], 3),
            "negar_detected": negar["is_negar"] or fi["Fi_score"] >= 2,
            "fi_score": fi["Fi_score"],
            "fi_type": fi["Fi_type"],
            "arrogance_detected": hayrat["arrogance_detected"],
            "belief_type": belief_type.get("type", "HYPOTHESIS"),
            "policy_event": policy.fanus_event,
            "sources": sources,
            "recommendation": hayrat.get("suggested_revision"),
            "timestamp": time.time()
        }
