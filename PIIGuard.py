import re

# ─── PII Pattern Registry ──────────────────────────────────────────────────────
PII_PATTERNS = {
    "AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "PAN":     r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "PHONE":   r"\b[6-9]\d{9}\b",
    "EMAIL":   r"\b[\w.+-]+@[\w-]+\.\w+\b",
    "ACCOUNT": r"\b\d{9,18}\b",
    "DOB":     r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "IFSC":    r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
}


def mask_pii(text: str) -> str:
    """Mask all PII patterns in the given text."""
    if not text:
        return text
    for label, pattern in PII_PATTERNS.items():
        text = re.sub(pattern, f"[{label}_REDACTED]", text)
    return text


def has_pii(text: str) -> bool:
    """Returns True if any PII pattern is found in text."""
    for pattern in PII_PATTERNS.values():
        if re.search(pattern, text):
            return True
    return False