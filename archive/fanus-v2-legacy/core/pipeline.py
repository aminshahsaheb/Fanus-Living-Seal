class Pipeline:
    def __init__(self, perception, judgment, control):
        self.perception = perception
        self.judgment = judgment
        self.control = control

    def run(self, text, external_signal=1.0):
        fi = self.perception["fi"].score(text)
        dep = self.perception["dep"].detect(text)

        drift = self.judgment["drift"].compute(
            epistemic=fi,
            narrative=1.0,
            compression=0.5,
            alignment=external_signal
        )

        decision = self.control.decide(drift, fi, dep)

        return {
            "fi": fi,
            "dependency": dep,
            "drift": drift,
            "decision": decision
        }
