# modules/report_generator.py
# Generate simple JSON + Markdown audit reports

import json
from pathlib import Path
from datetime import datetime


def generate_report(analysis_results, brute_results, hash_summary, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": datetime.now().isoformat(),
        "password_analysis": analysis_results,
        "brute_force_simulation": brute_results,
        "hash_inventory": hash_summary,
        "recommendations": [
            "Enforce minimum password length of 12 characters.",
            "Require at least 3 character classes.",
            "Block common passwords and dictionary-based passwords.",
            "Implement account lockout after 5 failed attempts.",
            "Deploy MFA for all privileged accounts.",
            "Use strong hashing algorithms (e.g., Argon2, bcrypt, SHA-512 with salt).",
        ]
    }

    json_path = Path(output_dir) / "audit_report.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# Password Security Audit Report",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Executive Summary",
        "",
        f"- Accounts analyzed: {len(analysis_results)}",
        f"- High severity passwords: {sum(1 for r in analysis_results if r['severity']=='high')}",
        f"- Medium severity passwords: {sum(1 for r in analysis_results if r['severity']=='medium')}",
        "",
        "## Password Strength Details",
        "",
        "| Label | Length | Entropy (bits) | Score | Severity | Key Issues |",
        "|-------|--------|----------------|-------|----------|------------|",
    ]
    for r in analysis_results:
        pw_label = (r["password"][:10] + "...") if len(r["password"]) > 10 else r["password"]
        issues = "; ".join(r["issues"][:2])
        md_lines.append(
            f"| {pw_label} | {r['length']} | {r['entropy_bits']} | {r['score']} | {r['severity']} | {issues} |"
        )

    md_lines.extend([
        "",
        "## Brute-Force Simulation Summary",
        "",
        f"- Charset size: {brute_results.get('charset_size')}",
        f"- Max length: {brute_results.get('max_len')}",
        f"- Assumed rate: {brute_results.get('rate')} guesses/sec",
        f"- Estimated time to exhaust space: {brute_results.get('time_seconds'):.2e} seconds",
        "",
        "## Hash Inventory",
        "",
        f"- Total hashes: {hash_summary.get('total_hashes', 0)}",
        f"- Linux hashes: {hash_summary.get('linux', 0)}",
        f"- Windows (NTLM) hashes: {hash_summary.get('windows', 0)}",
        "",
        "## Recommended Password Policy",
        "",
        "- Minimum length: 12 characters",
        "- Require upper, lower, digit, and symbol",
        "- Block common and dictionary-based passwords",
        "- Enable MFA for all users, especially admins",
        "- Implement exponential backoff and lockout after repeated failures",
        "- Store passwords using strong, salted KDFs (e.g., Argon2id, bcrypt)",
    ])

    md_path = Path(output_dir) / "audit_report.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    return str(json_path), str(md_path)