"""Persian text normalisation shared by the detectors.

Why: regex lexicons written with one spelling silently miss the others. Found in this project:
a pattern with a tanvin ("قطعاً") never matched because \\b sees no boundary after a combining
mark, "قطعا" (no tanvin) is the common spelling, and a pattern written with a ZWNJ ("بی‌شک")
missed text typed with a plain space. Applying the same normalisation to the text and to every
pattern removes that whole class of misses.
"""
import re

_DIACRITICS = re.compile("[\u064b-\u0652\u0670\u0640]")  # harakat, dagger alif, tatweel
_MAP = str.maketrans({"ي": "ی", "ك": "ک", "ۀ": "ه", "ة": "ه", "ؤ": "و", "أ": "ا", "إ": "ا", "ٱ": "ا"})


def normalize_fa(text: str) -> str:
    if not text:
        return ""
    s = text.replace("\u200c", " ").replace("\u200f", "").replace("\u200e", "")
    s = s.translate(_MAP)
    s = _DIACRITICS.sub("", s)
    return re.sub(r"[ \t]+", " ", s)
