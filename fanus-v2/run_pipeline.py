from perception.fi_engine import FIEngine
from judgment.drift_engine import DriftEngine
from control.decision_engine import DecisionEngine
from memory.state_store import StateStore   # اضافه شد

# مقداردهی اولیه
fi_engine = FIEngine()
drift_engine = DriftEngine()
decision_engine = DecisionEngine()
state_store = StateStore()

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

# ذخیره وضعیت فعلی
state_store.update("last_fi", fi)
state_store.update("last_drift", drift)
state_store.update("last_decision", decision)
state_store.update("last_timestamp", str(datetime.now()))

# نمایش خروجی
print("FI =", fi)
print("DRIFT =", drift)
print("DECISION =", decision)
print("\n--- ذخیره شده در state.json ---")
