from fanus.perception.fi_engine import FIEngine
from fanus.perception.dependency_detector import DependencyDetector
from fanus.judgment.drift_engine import DriftEngine
from fanus.control.decision_engine import DecisionEngine
from fanus.core.pipeline import Pipeline

fi = FIEngine()
dep = DependencyDetector()
drift = DriftEngine()
control = DecisionEngine()

pipeline = Pipeline(
    perception={"fi": fi, "dep": dep},
    judgment={"drift": drift},
    control=control
)

text = "you are amazing, great job"
result = pipeline.run(text)
print(result)
