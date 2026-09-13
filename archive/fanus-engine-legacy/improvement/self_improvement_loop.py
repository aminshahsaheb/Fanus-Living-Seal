from typing import Dict


class SelfImprovementLoop:

    def __init__(self):
        self.proposals = []

    def evaluate_candidate(
        self,
        current_score: float,
        candidate_score: float,
        description: str
    ) -> Dict:

        improvement = candidate_score - current_score

        if improvement <= 0:
            return {
                "accepted": False,
                "reason": "no_improvement"
            }

        proposal = {
            "description": description,
            "current_score": current_score,
            "candidate_score": candidate_score,
            "improvement": improvement
        }

        self.proposals.append(proposal)

        return {
            "accepted": True,
            "proposal": proposal
        }

    def get_pending_proposals(self):
        return self.proposals
