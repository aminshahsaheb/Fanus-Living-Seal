from fanus.cognitive.negar_detector import NegarDetector
from fanus.cognitive.hayrat_judge import HayratJudge
from fanus.cognitive.fi_detector import detect_fi

_negar = NegarDetector()
_hayrat = HayratJudge()


def run_guardians(user_message: str, response: str, speaker: str = "fanus") -> dict:
    negar_result = _negar.analyze(response, speaker)
    hayrat_result = _hayrat.evaluate(response, user_message)
    fi_result = detect_fi(user_message, response)
    return {
        "negar": negar_result.get("is_negar"),
        "hayrat_score": hayrat_result["hayrat_score"],
        "arrogance": hayrat_result["arrogance_detected"],
        "uncertainty_required": hayrat_result["uncertainty_required"],
        "fi_score": fi_result.get("Fi_score"),
        "fi_type": fi_result.get("Fi_type"),
    }
