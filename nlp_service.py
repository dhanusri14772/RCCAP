import spacy
nlp = spacy.load("en_core_web_sm")
BANNED_TERMS = ["guaranteed", "cheapest", "best price"]
MAX_DISCOUNT = 80  

def run_nlp_checks(text: str) -> dict:
    issues: list[str] = []

    lower = text.lower()
    for term in BANNED_TERMS:
        if term in lower:
            issues.append(f"Contains banned term: '{term}'")

    doc = nlp(text)
    for token in doc:
        word = token.text.strip()
        if word.endswith("%"):
            try:
                val = int(word.strip("%"))
                if val > MAX_DISCOUNT:
                    issues.append(f"Unrealistic discount: {val}%")
            except ValueError:
                continue

    return {"passed": len(issues) == 0, "issues": issues}


if __name__ == "__main__":
    print(run_nlp_checks("Save 90% guaranteed now!"))
