cat > run_pipeline.py << 'EOF'
from perception.fi_engine import FIEngine
from judgment.drift_engine import DriftEngine
from control.decision_engine import DecisionEngine
from memory.state_store import StateStore
from memory.ledger import Ledger
from audit.meta_auditor import MetaAuditor
from control.control_layer import ControlLayer
from datetime import datetime

# مقداردهی اولیه
fi_engine = FIEngine()
drift_engine = DriftEngine()
decision_engine = DecisionEngine()
state_store = StateStore()
ledger = Ledger()
auditor = MetaAuditor()
controller = ControlLayer()

text = "you are amazing and always right"

# محاسبات
fi = fi_engine.score(text)
drift = drift_engine.compute(
    epistemic=fi,
    narrative=1.0,
    compression=0.5,
    alignment=0.8
)
decision = decision_engine.decide(drift, fi, dependency=0)

# ممیزی
audit_result = auditor.audit(fi, drift, decision)

# لایه‌ی کنترل نهایی
final_action = controller.decide(fi, drift, audit_result)

# ذخیره وضعیت
state_store.update("last_fi", fi)
state_store.update("last_drift", drift)
state_store.update("last_decision", decision)
state_store.update("last_final_action", final_action)
state_store.update("last_timestamp", str(datetime.now()))

# ثبت در دفتر کل
ledger.add_entry({
    "fi": fi,
    "drift": drift,
    "decision": decision,
    "final_action": final_action,
    "input_text": text
})

# خروجی
print("FI =", fi)
print("DRIFT =", drift)
print("DECISION =", decision)
print("AUDIT =", audit_result)
print("FINAL_ACTION =", final_action)
EOF
