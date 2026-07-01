"""
==========================================================
FANUS SAFETY SIGNAL BUS
==========================================================

Central safety communication layer.

==========================================================
"""

class SafetySignalBus:

    def __init__(self):
        self.events = []

    def emit(self, signal):
        self.events.append(signal)
        return signal

    def latest(self):
        return self.events[-1] if self.events else None
