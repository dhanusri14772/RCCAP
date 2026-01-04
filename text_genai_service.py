import re
from typing import List

BANNED_TERMS = ["guaranteed", "cheapest", "best price"]
MAX_DISCOUNT = 80


def _strip_banned_phrases(text: str) -> str:
    lower = text.lower()
    for term in BANNED_TERMS:
        if term in lower:
            text = re.sub(term, "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def _cap_discounts(text: str) -> str:
    def repl(m):
        val = int(m.group(1))
        if val > MAX_DISCOUNT:
            return f"{MAX_DISCOUNT}%"
        return m.group(0)

    return re.sub(r"(\d+)%", repl, text)


def enhance_copy(raw_copy: str, brief: str) -> dict:
    """
    Local 'GenAI-style' enhancer:
    - cleans banned phrases
    - caps unrealistic discounts
    - generates 2–3 styled variants
    """
    base = _cap_discounts(_strip_banned_phrases(raw_copy))

    options: List[str] = []

    options.append(base)

    options.append(f"{base} – {brief.split('.')[0].strip()}")

    options.append(f"{base}. Shop now in Tesco stores.")

    cleaned = []
    seen = set()
    for o in options:
        o = o.strip()
        if o and o not in seen:
            seen.add(o)
            cleaned.append(o)

    return {"options": cleaned[:3] or [raw_copy]}
