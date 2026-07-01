class MemoryPressureEngine:
    """
    Converts memory growth + entropy into evolutionary pressure.
    """

    def evaluate(self, memory_layer):

        size = memory_layer.size()

        # entropy proxy
        recent = memory_layer.all()[-20:]

        diversity = len(set(
            e["entity"] for e in recent
        )) if recent else 0

        pressure = min(
            1.0,
            (size / 500) * 0.6 + (diversity / 10) * 0.4
        )

        return {
            "pressure": round(pressure, 3),
            "memory_size": size,
            "diversity": diversity,
            "mode": "self_rewriting_trigger"
        }
