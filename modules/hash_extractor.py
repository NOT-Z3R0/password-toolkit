# modules/hash_extractor.py
# Parse Linux shadow and Windows NTLM-style hash files (offline, lab only)

import re
from pathlib import Path

HASH_PATTERNS = {
    r'^\$1\$': 'MD5',
    r'^\$2a\$|^\$2b\$|^\$2y\$': 'bcrypt',
    r'^\$5\$': 'SHA-256',
    r'^\$6\$': 'SHA-512',
}


def detect_linux_hash_type(hash_field: str) -> str:
    for pattern, name in HASH_PATTERNS.items():
        if re.match(pattern, hash_field):
            return name
    if re.fullmatch(r'[0-9a-fA-F]{32}', hash_field):
        return 'MD5 (unsalted)'
    if re.fullmatch(r'[0-9a-fA-F]{64}', hash_field):
        return 'SHA-256 (unsalted?)'
    return 'unknown'


def parse_shadow_file(shadow_path: str):
    entries = []
    for line in Path(shadow_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(":")
        if len(parts) < 2:
            continue
        username, hash_field = parts[0], parts[1]
        if hash_field in ["*", "!", "!!", ""]:
            continue  # locked / no password
        algo = detect_linux_hash_type(hash_field)
        entries.append({
            "username": username,
            "hash": hash_field,
            "algo": algo,
            "os": "Linux"
        })
    return entries


def parse_ntlm_file(ntlm_path: str):
    entries = []
    for line in Path(ntlm_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Format: domain\username:rid:lmhash:nthash:::
        parts = line.split(":")
        if len(parts) < 4:
            continue
        user_part = parts[0]
        username = user_part.split("\\")[-1]
        nt_hash = parts[3]
        # skip empty or blank LM/NT
        if not nt_hash or nt_hash == "aad3b435b51404eeaad3b435b51404ee":
            continue
        entries.append({
            "username": username,
            "hash": nt_hash,
            "algo": "NTLM",
            "os": "Windows"
        })
    return entries