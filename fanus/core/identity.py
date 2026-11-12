import os
from fanus.core.seal_verifier import SealVerifier


class FanusIdentity:

    def __init__(self):
        self.root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def verify(self, state, stored_hash=None):
        """Compare the core identity state with a previously stored hash.

        Without stored_hash there is nothing to compare against, so the result is BASELINE_ESTABLISHED
        (carrying current_hash to store), never PASSED.
        """
        return SealVerifier().verify_seal_integrity(state, stored_hash)

    def system_prompt(self):
        return (
            "You are Fanus — an epistemic AI cognitive engine built by Amin Shahsaheb. "
            "You are NOT a lantern. You witness truth. You detect flattery. "
            "You never claim certainty beyond evidence. "
            "Always respond in Persian only. Never use Arabic."
        )
