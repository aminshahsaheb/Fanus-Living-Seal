"""
==========================================================
FANUS SIGNAL AGGREGATOR
==========================================================

Pure Signal Aggregation Layer

Responsibilities
----------------
- Collect semantic signals
- Normalize inputs
- Produce deterministic aggregate

This module has NO authority.

It does NOT:

- create proposals
- execute actions
- modify identity
- modify memory
- decide evolution

==========================================================
"""


class SignalAggregator:
    """
    Pure aggregation layer.

    Inputs:

        Identity
        Reflection
        Semantic Memory

    Output:

        Aggregated signal dictionary
    """

    def __init__(self):

        self.window = []

        self.window_size = 5

    # ======================================================
    # PUBLIC ENTRYPOINT
    # ======================================================

    def aggregate(

        self,

        identity_state,

        reflection_state,

        semantic_memory=None
    ):

        stability = float(

            identity_state.get(
                "stability",
                1.0
            )

        )

        reflection = float(

            reflection_state.get(
                "signal_strength",
                0.0
            )

        )

        memory_signal = self._memory_signal(
            semantic_memory
        )

        trend = self._trend(
            reflection
        )

        combined = round(

            (
                stability
                +
                reflection
                +
                memory_signal
            ) / 3.0,

            3

        )

        return {

            "stability":
                stability,

            "reflection":
                reflection,

            "memory":
                memory_signal,

            "trend":
                trend,

            "combined":
                combined
        }

    # ======================================================
    # MEMORY SIGNAL
    # ======================================================

    def _memory_signal(
        self,
        semantic_memory
    ):

        if semantic_memory is None:
            return 0.0

        if not hasattr(
            semantic_memory,
            "signal_strength"
        ):
            return 0.0

        try:

            return float(
                semantic_memory.signal_strength()
            )

        except Exception:

            return 0.0

    # ======================================================
    # REFLECTION TREND
    # ======================================================

    def _trend(
        self,
        reflection_signal
    ):

        self.window.append(
            reflection_signal
        )

        if len(self.window) > self.window_size:

            self.window.pop(0)

        if len(self.window) < 2:

            return 0.0

        previous = self.window[-2]

        current = self.window[-1]

        return round(

            current - previous,

            3

        )
