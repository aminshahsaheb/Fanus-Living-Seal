class Validator:
    def check(self, value: float, threshold: float):
        return {
            "value": value,
            "pass": value <= threshold
        }
