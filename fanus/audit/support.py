"""Deterministic support checks for Verify.

Two things used to be assumed instead of checked: arithmetic (anything shaped like a sum was "true") and context
(any non-empty text counted as a 0.7-confidence source). Arithmetic is now computed, and context only counts when it
shares content words with the claim. Relevance is lexical, not entailment: it does not prove that the context
supports the claim (see docs/ROADMAP.md, phase C).
"""
import ast
import re
import unicodedata
from fractions import Fraction

from fanus.cognitive.fa_text import normalize_fa

_NUM = r"\d+(?:\.\d+)?"
_OPS = r"[+\-*/×÷]"
_EQUATION = re.compile(rf"(?<![\w./-])({_NUM}(?:\s*{_OPS}\s*{_NUM})+)\s*=\s*([-+]?{_NUM})(?!\w|[/-]|\.\d)")
_FA_NUM = {"صفر": 0, "یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5, "شش": 6, "هفت": 7, "هشت": 8, "نه": 9, "ده": 10}
_FA_OP = {"به علاوه": "+", "جمع": "+", "منهای": "-", "تفریق": "-", "ضرب": "*", "تقسیم": "/"}
_WORDS = "|".join(sorted(_FA_NUM, key=len, reverse=True))
_OPWORDS = "|".join(sorted(_FA_OP, key=len, reverse=True))
_WORD_EQUATION = re.compile(rf"(?<!\w)({_WORDS})\s+({_OPWORDS})\s+({_WORDS})\s+(?:می شود|برابر است با|مساوی است با)\s+({_WORDS})(?!\w)")


def ascii_digits(text: str) -> str:
    """Persian and Arabic-Indic digits to ASCII; the Persian decimal separator to '.'."""
    return "".join(str(unicodedata.digit(ch)) if ch.isdigit() else ("." if ch == "٫" else ch) for ch in text)


def _walk(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return Fraction(str(node.value))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        value = _walk(node.operand)
        return -value if isinstance(node.op, ast.USub) else value
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
        left, right = _walk(node.left), _walk(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        return left / right
    raise ValueError("unsupported expression")


def _consistent(expr: str, claimed: str):
    """True/False for 'expr = claimed', or None when the expression cannot be evaluated."""
    try:
        value = _walk(ast.parse(expr.replace("×", "*").replace("÷", "/"), mode="eval").body)
    except (ValueError, SyntaxError, ZeroDivisionError):
        return None
    right = Fraction(claimed)
    decimals = len(claimed.split(".")[1]) if "." in claimed else 0
    tolerance = Fraction(1, 2 * 10 ** decimals) if decimals else Fraction(0)  # a decimal result may be a rounding
    return abs(value - right) <= tolerance


def check_arithmetic(text: str):
    """Compute explicit equations in `text` ("2 + 2 = 5", "دو به علاوه دو می‌شود پنج").

    Returns None when there is no explicit equation, else {"checked": n, "wrong": m}.
    """
    normalised = normalize_fa(ascii_digits(text or ""))
    checked = wrong = 0
    for match in _EQUATION.finditer(normalised):
        verdict = _consistent(match.group(1), match.group(2))
        if verdict is not None:
            checked += 1
            wrong += verdict is False
    for match in _WORD_EQUATION.finditer(normalised):
        a, op, b, result = match.groups()
        verdict = _consistent(f"{_FA_NUM[a]}{_FA_OP[op]}{_FA_NUM[b]}", str(_FA_NUM[result]))
        if verdict is not None:
            checked += 1
            wrong += verdict is False
    return {"checked": checked, "wrong": wrong} if checked else None


_STOP = {"the", "and", "for", "are", "was", "with", "that", "this", "from", "have", "has", "not", "but", "you", "all",
         "can", "will", "their", "his", "her", "its", "who", "which", "than", "then", "into", "also",
         "است", "این", "آن", "که", "را", "برای", "با", "از", "در", "به", "هم", "نیز", "های", "ها", "بود", "شود", "می"}


def _tokens(text: str):
    return {t for t in re.findall(r"\w+", normalize_fa(text or "").lower()) if len(t) >= 3 and t not in _STOP}


def context_supports(claim: str, context: str) -> bool:
    """Lexical relevance: at least two shared content words and a quarter of the claim's content words."""
    claim_tokens, context_tokens = _tokens(claim), _tokens(context)
    shared = claim_tokens & context_tokens
    return bool(claim_tokens) and len(shared) >= 2 and len(shared) / len(claim_tokens) >= 0.25
