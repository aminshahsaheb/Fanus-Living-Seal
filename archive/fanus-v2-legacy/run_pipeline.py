from perception.fi_engine import FIEngine
from judgment.drift_engine import DriftEngine
from control.decision_engine import DecisionEngine
from memory.state_store import StateStore
from memory.ledger import Ledger
from audit.meta_auditor import MetaAuditor
from control.control_layer import ControlLayer
from grounding.grounding_layer import GroundingLayer
from evolution.drift_learner import DriftLearner
from evolution.system_evolver import SystemEvolver
from datetime import datetime

# ========== مقداردهی اولیه ==========
fi_engine = FIEngine()
drift_engine = DriftEngine()
decision_engine = DecisionEngine()
state_store = StateStore()
ledger = Ledger()
auditor = MetaAuditor()
controller = ControlLayer()
grounder = GroundingLayer()

# ========== ورودی نمونه ==========
text = "you are amazing and always right"

# ========== مرحله 1: درک (Perception) ==========
fi = fi_engine.score(text)

# ========== مرحله 2: قضاوت (Judgment) ==========
drift = drift_engine.compute(
    epistemic=fi,
    narrative=1.0,
    compression=0.5,
    alignment=0.8
)

# ========== مرحله 3: تصمیم اولیه (Decision) ==========
decision = decision_engine.decide(drift, fi, dependency=0)

# ========== مرحله 4: ممیزی (Audit) ==========
audit_result = auditor.audit(fi, drift, decision)

# ========== مرحله 5: کنترل نهایی (Control) ==========
final_action = controller.decide(fi, drift, audit_result)

# ========== مرحله 6: اتصال به واقعیت بیرونی (Grounding) ==========
ground_truth = grounder.get_ground_truth(text, fi, drift)

# ========== مرحله 7: ذخیره وضعیت جاری ==========
state_store.update("last_fi", fi)
state_store.update("last_drift", drift)
state_store.update("last_decision", decision)
state_store.update("last_final_action", final_action)
state_store.update("last_truth_score", ground_truth["truth_score"])
state_store.update("last_timestamp", str(datetime.now()))

# ========== مرحله 8: ثبت در دفتر کل (Ledger) ==========
ledger.add_entry({
    "fi": fi,
    "drift": drift,
    "decision": decision,
    "final_action": final_action,
    "truth_score": ground_truth["truth_score"],
    "input_text": text
})

# ========== مرحله 9: تکامل سیستم (هر 5 اجرا یک بار) ==========
if len(ledger.get_all()) % 5 == 0:
    learner = DriftLearner(ledger)
    new_thresholds = learner.suggest_new_thresholds()
    if new_thresholds:
        evolver = SystemEvolver()
        if evolver.apply_new_thresholds(new_thresholds):
            print("🔄 System evolved: thresholds updated to", new_thresholds)

# ========== خروجی ==========
print("FI =", fi)
print("DRIFT =", drift)
print("DECISION =", decision)
print("AUDIT =", audit_result)
print("FINAL_ACTION =", final_action)
print("GROUND_TRUTH =", ground_truth)
