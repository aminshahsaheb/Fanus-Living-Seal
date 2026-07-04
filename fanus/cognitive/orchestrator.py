from fanus.cognitive.goal_engine import GoalEngine
from fanus.cognitive.curiosity_engine import CuriosityEngine
from fanus.cognitive.question_generator import QuestionGenerator
from fanus.cognitive.research_planner import ResearchPlanner
from fanus.cognitive.contradiction_detector import ContradictionDetector
from fanus.cognitive.meta_learning import MetaLearning
from fanus.cognitive.longterm_planner import LongTermPlanner
from fanus.cognitive.self_review import SelfReview


class CognitiveOrchestrator:

    def __init__(self):
        self.goals = GoalEngine()
        self.curiosity = CuriosityEngine()
        self.questions = QuestionGenerator()
        self.research = ResearchPlanner()
        self.contradictions = ContradictionDetector()
        self.meta = MetaLearning()
        self.planner = LongTermPlanner()
        self.review = SelfReview()

    def process(self, user_input, response):
        self.curiosity.generate(user_input)
        self.questions.generate(user_input, "HYPOTHESIS", 0.7)
        self.meta.learn("conversation", response[:50], user_input[:50])
        top_goal = self.goals.top()
        return {
            "top_goal": top_goal["goal"] if top_goal else None,
            "unanswered_questions": len(self.curiosity.unanswered()),
            "meta_patterns": self.meta.stats()["total_patterns"]
        }

    def status(self, ledger, beliefs, goals_list, plans):
        return self.review.review(ledger, beliefs, goals_list, plans)