# modules/brute_force_sim.py
# Simple brute-force simulation (estimates search space and time to crack)

from typing import List

CHARSETS = {
    "lower": "abcdefghijklmnopqrstuvwxyz",
    "upper": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "digits": "0123456789",
    "symbols": "!@#$%^&*()-_=+[]{};:,.<>?"
}


def build_charset(keys: List[str]) -> str:
    return "".join(CHARSETS[k] for k in keys)


def search_space_size(charset_size: int, max_len: int) -> int:
    total = 0
    for l in range(1, max_len + 1):
        total += charset_size ** l
    return total


def estimate_time_to_crack(charset_size: int, max_len: int, rate: float) -> float:
    N = search_space_size(charset_size, max_len)
    return N / rate  # seconds