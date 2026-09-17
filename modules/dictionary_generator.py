# modules/dictionary_generator.py
# Basic dictionary generator with simple mutations

from pathlib import Path

LEET_MAP = str.maketrans({
    "a": "@",
    "e": "3",
    "i": "1",
    "o": "0",
    "s": "$",
    "t": "7",
})

COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "password123", "letmein", "welcome", "admin", "iloveyou",
    "test", "test123", "guest", "root", "user"
]

KEYBOARD_PATTERNS = ["qwerty", "qazwsx", "123456", "1qaz2wsx", "asdfgh"]


def apply_leet(word: str) -> str:
    return word.translate(LEET_MAP)


def mutate_word(word: str):
    variants = set()
    w = word.lower()

    # base forms
    variants.add(w)
    variants.add(w.capitalize())
    variants.add(w.upper())

    # leet speak
    variants.add(apply_leet(w))
    variants.add(apply_leet(w).capitalize())

    # append numbers
    for n in ["", "1", "12", "123", "2023", "2024", "2025", "2026"]:
        variants.add(w + n)
        variants.add(apply_leet(w) + n)

    # prepend numbers
    for n in ["1", "12", "123"]:
        variants.add(n + w)

    # common suffixes
    for s in ["!", "@", "#", "$", "123", "2023", "2024", "2025", "2026"]:
        variants.add(w + s)
        variants.add(w.capitalize() + s)

    return variants


def generate_base_words(names, dob=None):
    words = set()

    for n in names:
        words.add(n.lower())
        words.add(n.capitalize())

    if dob:
        dob_str = str(dob).replace("-", "").replace("/", "")
        for n in names:
            base = n.lower()
            words.add(base + dob_str)
            words.add(base + dob_str[:4])
            words.add(base + dob_str[-4:])
            words.add(base.capitalize() + dob_str)
            words.add(base.capitalize() + dob_str[:4])
            words.add(base.capitalize() + dob_str[-4:])

    # add common passwords and patterns
    words.update(p.lower() for p in COMMON_PASSWORDS)
    words.update(p.lower() for p in KEYBOARD_PATTERNS)

    return list(words)


def generate_dictionary(names, output_path: str, dob=None):
    base_words = generate_base_words(names, dob)
    all_words = set()

    for w in base_words:
        all_words |= mutate_word(w)

    # clean up
    all_words = {w for w in all_words if w and len(w) <= 32}

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(sorted(all_words)), encoding="utf-8")