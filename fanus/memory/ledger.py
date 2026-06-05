class Ledger:
    def __init__(self):
        self.records = []
    def log(self, entry: dict):
        self.records.append(entry)
