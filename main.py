# main.py
# Password Policy Testing Toolkit - CLI entry point

import argparse
import json
from pathlib import Path

from modules.dictionary_generator import generate_dictionary
from modules.hash_extractor import parse_shadow_file, parse_ntlm_file
from modules.password_analyzer import analyze_password
from modules.brute_force_sim import build_charset, estimate_time_to_crack
from modules.report_generator import generate_report


def load_dictionary(path):
    if not path:
        return None
    return set(
        line.strip().lower()
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def main():
    parser = argparse.ArgumentParser(
        description="Password Policy Testing Toolkit (lab use only)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # generate-dictionary
    p_dict = sub.add_parser("generate-dictionary", help="Generate password dictionary")
    p_dict.add_argument("--names", nargs="+", required=True, help="Names to base dictionary on")
    p_dict.add_argument("--dob", default=None, help="Date of birth (e.g. 07022003)")
    p_dict.add_argument("--output", required=True, help="Output file path for wordlist")

    # extract-hashes
    p_hash = sub.add_parser("extract-hashes", help="Parse Linux shadow / Windows NTLM files")
    p_hash.add_argument("--linux-shadow", default=None, help="Path to Linux shadow file")
    p_hash.add_argument("--windows-ntlm", default=None, help="Path to NTLM hashes file")
    p_hash.add_argument("--output-json", default="reports/hashes.json", help="Output JSON file")

    # analyze-passwords
    p_analyze = sub.add_parser("analyze-passwords", help="Analyze password strength")
    p_analyze.add_argument("--passwords", nargs="+", required=True, help="Passwords to analyze")
    p_analyze.add_argument("--dictionary", default=None, help="Path to dictionary file")
    p_analyze.add_argument("--output-json", default="reports/analysis.json", help="Output JSON file")

    # simulate-bruteforce
    p_bf = sub.add_parser("simulate-bruteforce", help="Simulate brute-force cracking")
    p_bf.add_argument("--charset-keys", nargs="+", default=["lower", "digits"],
                      help="Charset keys: lower, upper, digits, symbols")
    p_bf.add_argument("--max-len", type=int, default=6, help="Max password length")
    p_bf.add_argument("--rate", type=float, default=1e8, help="Guesses per second")
    p_bf.add_argument("--output-json", default="reports/bruteforce.json", help="Output JSON file")

    # full-audit
    p_full = sub.add_parser("full-audit", help="Run full audit (dictionary + analysis + report)")
    p_full.add_argument("--passwords", nargs="+", required=True, help="Passwords to analyze")
    p_full.add_argument("--names", nargs="+", default=[], help="Names for dictionary")
    p_full.add_argument("--dob", default=None, help="Date of birth for dictionary")
    p_full.add_argument("--output-dir", default="reports", help="Output directory for reports")

    args = parser.parse_args()

    if args.cmd == "generate-dictionary":
        generate_dictionary(args.names, args.output, dob=args.dob)
        print(f"[+] Dictionary written to {args.output}")

    elif args.cmd == "extract-hashes":
        entries = []
        if args.linux_shadow:
            entries += parse_shadow_file(args.linux_shadow)
        if args.windows_ntlm:
            entries += parse_ntlm_file(args.windows_ntlm)

        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        print(f"[+] Hash entries written to {args.output_json}")

    elif args.cmd == "analyze-passwords":
        dictionary = load_dictionary(args.dictionary)
        results = [analyze_password(pw, dictionary) for pw in args.passwords]

        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"[+] Analysis written to {args.output_json}")

    elif args.cmd == "simulate-bruteforce":
        charset = build_charset(args.charset_keys)
        C = len(charset)
        time_sec = estimate_time_to_crack(C, args.max_len, args.rate)

        result = {
            "charset_keys": args.charset_keys,
            "charset_size": C,
            "max_len": args.max_len,
            "rate": args.rate,
            "time_seconds": time_sec
        }

        Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"[+] Brute-force simulation written to {args.output_json}")

    elif args.cmd == "full-audit":
        # 1. Generate dictionary from names + DOB
        dict_path = "wordlists/custom_dict.txt"
        Path("wordlists").mkdir(parents=True, exist_ok=True)
        generate_dictionary(args.names, dict_path, dob=args.dob)
        dictionary = load_dictionary(dict_path)

        # 2. Analyze given passwords
        analysis_results = [analyze_password(pw, dictionary) for pw in args.passwords]

        # 3. Brute-force simulation (example config)
        charset = build_charset(["lower", "upper", "digits", "symbols"])
        C = len(charset)
        time_sec = estimate_time_to_crack(C, 8, 1e8)
        brute_results = {
            "charset_size": C,
            "max_len": 8,
            "rate": 1e8,
            "time_seconds": time_sec
        }

        # 4. Hash summary (placeholder; can be extended later)
        hash_summary = {
            "total_hashes": 0,
            "linux": 0,
            "windows": 0
        }

        # 5. Generate report
        j, md = generate_report(analysis_results, brute_results, hash_summary, args.output_dir)
        print(f"[+] Report JSON: {j}")
        print(f"[+] Report Markdown: {md}")


if __name__ == "__main__":
    main()