cat > ~/Desktop/Fanus-Living-Seal/fanus-v2/run_pipeline.py << 'EOF'
from perception.fi_engine import FIEngine
from judgment.drift_engine import DriftEngine
from control.decision_engine import DecisionEngine
from memory.state_store import StateStore
from memory.ledger import Ledger
from datetime import datetime

# مقداردهی اولیه
fi_engine = FIEngine()
drift_engine = DriftEngine()
decision_engine = DecisionEngine()
state_store = StateStore()
ledger = Ledger()

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

# ذخیره وضعیت فعلی در StateStore
state_store.update("last_fi", fi)
state_store.update("last_drift", drift)
state_store.update("last_decision", decision)
state_store.update("last_timestamp", str(datetime.now()))

# ثبت رکورد در دفتر کل (Ledger)
ledger.add_entry({
    "fi": fi,
    "drift": drift,
    "decision": decision,
    "input_text": text
})

# نمایش خروجی
print("FI =", fi)
print("DRIFT =", drift)
print("DECISION =", decision)
print("\n--- آخرین ۳ رکورد دفتر کل ---")
for entry in ledger.get_last_n(3):
    print(f"  {entry['timestamp']} | FI={entry['fi']} | {entry['decision']}")
EOF
