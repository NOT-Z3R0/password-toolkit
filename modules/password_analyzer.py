# modules/password_analyzer.py
# Password strength analyzer with basic entropy and pattern checks

import math
import re

COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "password123", "letmein", "welcome", "admin", "iloveyou",
    "test", "test123", "guest", "root", "user"
]

KEYBOARD_PATTERNS = ["qwerty", "qazwsx", "123456", "1qaz2wsx", "asdfgh"]


def has_repeats(pw: str) -> bool:
    return bool(re.search(r"(.)\1\1", pw))


def has_sequence(pw: str) -> bool:
    pw_lower = pw.lower()
    for pat in KEYBOARD_PATTERNS:
        if pat in pw_lower:
            return True
    if re.search(r"(012|123|234|345|456|567|678|789)", pw):
        return True
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)", pw_lower):
        return True
    return False


def effective_charset_size(pw: str) -> int:
    size = 0
    if re.search(r"[a-z]", pw):
        size += 26
    if re.search(r"[A-Z]", pw):
        size += 26
    if re.search(r"\d", pw):
        size += 10
    if re.search(r"[^a-zA-Z0-9]", pw):
        size += 32
    return max(size, 1)


def entropy_bits(pw: str) -> float:
    L = len(pw)
    C = effective_charset_size(pw)
    return L * math.log2(C)


def analyze_password(pw: str, dictionary=None):
    issues = []
    recommendations = []
    score = 100

    if len(pw) < 8:
        issues.append("Too short (<8 characters).")
        recommendations.append("Use at least 12–16 characters.")
        score -= 20
    elif len(pw) < 12:
        issues.append("Length is moderate; 12+ recommended.")
        score -= 5

    classes = {
        "lower": bool(re.search(r"[a-z]", pw)),
        "upper": bool(re.search(r"[A-Z]", pw)),
        "digit": bool(re.search(r"\d", pw)),
        "symbol": bool(re.search(r"[^a-zA-Z0-9]", pw)),
    }
    class_count = sum(classes.values())
    if class_count < 3:
        issues.append("Not enough character classes.")
        recommendations.append("Mix upper, lower, digits, and symbols.")
        score -= 15

    if has_repeats(pw):
        issues.append("Contains repeated characters.")
        recommendations.append("Avoid repeated characters like 'aaa' or '111'.")
        score -= 10

    if has_sequence(pw):
        issues.append("Contains predictable sequences or keyboard patterns.")
        recommendations.append("Avoid sequences like '123', 'abc', 'qwerty'.")
        score -= 10

    pw_lower = pw.lower()
    if dictionary:
        if pw_lower in dictionary:
            issues.append("Found in custom dictionary (predictable).")
            recommendations.append("Avoid using names, DOB, or common patterns.")
            score -= 20

    if pw_lower in COMMON_PASSWORDS:
        issues.append("Found in common password list.")
        recommendations.append("Do not use common passwords.")
        score -= 25

    H = entropy_bits(pw)
    if H < 40:
        issues.append(f"Low entropy ({H:.1f} bits).")
        recommendations.append("Increase length and randomness.")
        score -= 15
    elif H < 60:
        issues.append(f"Moderate entropy ({H:.1f} bits).")
        score -= 5

    score = max(0, score)
    if score >= 80:
        severity = "low"
    elif score >= 50:
        severity = "medium"
    else:
        severity = "high"

    return {
        "password": pw,
        "length": len(pw),
        "entropy_bits": round(H, 2),
        "score": score,
        "severity": severity,
        "issues": issues,
        "recommendations": recommendations
    }