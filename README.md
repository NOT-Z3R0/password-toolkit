# Password Policy Testing & Credential Security Assessment Toolkit

## Description

Educational lab project to study how passwords are stored, attacked, and audited.  
This toolkit provides a controlled environment to understand password cracking techniques, how credentials are stored, and how security teams can reinforce authentication mechanisms.

This project is for ethical, lab-only use to understand evasion techniques and improve defensive authentication security.

GitHub Repository:  
https://github.com/NOT-Z3R0/password-toolkit

## Features

- **Dictionary Generator**  
  - Generate custom wordlists based on names, DOB, and common patterns  
  - Apply mutation rules (leet‑speak, uppercase variations, appended/prepended numbers)  

- **Hash Extraction Module**  
  - Parse Linux `/etc/shadow` style files  
  - Parse Windows NTLM‑style hash files (offline, lab only)  
  - Identify hashing algorithms (MD5, SHA‑256, SHA‑512, NTLM, etc.)  

- **Brute‑Force Simulator**  
  - Simulate brute‑force cracking attempts  
  - Support incremental mode (a–z, A–Z, 0–9, symbols)  
  - Provide estimated time‑to‑crack metrics  

- **Password Strength Analyzer**  
  - Check complexity requirements (length, character classes)  
  - Estimate entropy and detect pattern‑based weaknesses  
  - Provide improvement recommendations and severity rating  

- **Report Generation**  
  - Summary of weak passwords found  
  - Brute‑force simulation results  
  - Recommended password policies and mitigation steps  

## Installation

```bash
git clone https://github.com/NOT-Z3R0/password-toolkit.git
cd password-toolkit

# (Optional) Create a virtual environment:
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies:
pip install -r requirements.txt
```

## Usage

### Generate dictionary

```bash
python main.py generate-dictionary --names ansh makwana --dob 07022003 --output wordlists/demo_dict.txt
```

### Parse hash files

Linux shadow sample:

```bash
python main.py extract-hashes --linux-shadow sample_data/shadow_sample.txt --output-json reports/hashes.json
```

Windows NTLM sample:

```bash
python main.py extract-hashes --windows-ntlm sample_data/ntlm_hashes.txt --output-json reports/hashes.json
```

Combined:

```bash
python main.py extract-hashes --linux-shadow sample_data/shadow_sample.txt --windows-ntlm sample_data/ntlm_hashes.txt --output-json reports/hashes.json
```

### Analyze passwords

```bash
python main.py analyze-passwords \
  --passwords "Ansh@2003" "password123" "qwerty" "A9#kL2$mNp" \
  --dictionary wordlists/demo_dict.txt \
  --output-json reports/analysis.json
```

### Brute‑force simulation

```bash
python main.py simulate-bruteforce \
  --charset-keys lower upper digits symbols \
  --max-len 8 \
  --rate 1e8 \
  --output-json reports/bruteforce.json
```

### Full audit (end-to-end)

```bash
python main.py full-audit \
  --passwords "Ansh@2003" "password123" "qwerty" "A9#kL2$mNp" \
  --names ansh makwana \
  --dob 07022003 \
  --output-dir reports
```

Reports are saved to:

- `reports/audit_report.json`  
- `reports/audit_report.md`  

## Ethics and legal notice

This toolkit is only for educational purposes in a controlled lab environment.  
Do not use it against real user accounts, production systems, or any system you do not own or have explicit permission to test.

Always follow your local laws and your organization’s security policies.  
The author is not responsible for any misuse of this project.