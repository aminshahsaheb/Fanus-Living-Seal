class ExternalValidator:
    def compare(self, model_output: float, external_reference: float):
        if external_reference == 0:
            return 0.0
        return abs(model_output - external_reference)
