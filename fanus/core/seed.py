class FanusCoreSeed:

    def __init__(self):
        self.state = {
            "identity": "fanus-core-seed",
            "version": "1.0",
            "stability": 1.0
        }

    def read(self):
        return self.state

    def update(self, key, value):
        self.state[key] = value
        return self.state
