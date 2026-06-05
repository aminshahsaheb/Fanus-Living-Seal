from perception.fi_engine import FIEngine
from judgment.drift_engine import DriftEngine
from control.decision_engine import DecisionEngine

text = "you are amazing and always right"

fi = FIEngine().score(text)

drift = DriftEngine().compute(
    epistemic=fi,
    narrative=1,
    compression=0.5,
    alignment=0.8
)

decision = DecisionEngine().decide(
    drift=drift,
    fi=fi,
    dependency=0
)

print("FI =", fi)
print("DRIFT =", drift)
print("DECISION =", decision)
