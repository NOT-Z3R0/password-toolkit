# Password Policy Testing Toolkit

This project is a simple toolkit for testing password policies and understanding credential security.  
It is meant only for ethical, controlled lab use (your own VMs and test accounts).

## Features

- Dictionary generator (with basic mutations and patterns)
- Hash extraction parser (Linux shadow and Windows NTLM style files)
- Brute-force simulation (estimates time to crack)
- Password strength analyzer (complexity + basic entropy)
- Simple audit report generation

## Setup

1. Install Python 3.10+  
2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux / macOS
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

All commands are run from the project root folder.

### Generate dictionary

```bash
python main.py generate-dictionary --names ansh makwana --dob 07022003 --output wordlists/demo_dict.txt
```

### Parse hash files

Linux shadow sample:

```bash
python main.py extract-hashes --linux-shadow sample_data/shadow_sample.txt --output-json reports/hashes.json
```

Windows NTLM style sample:

```bash
python main.py extract-hashes --windows-ntlm sample_data/ntlm_hashes.txt --output-json reports/hashes.json
```

You can also combine both:

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

### Brute-force simulation

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

This will generate:

- `reports/audit_report.json`
- `reports/audit_report.md`

## Ethics and legal notice

This toolkit is only for educational purposes in a controlled lab environment.  
Do not use it against real user accounts, production systems, or any system you do not own or have explicit permission to test.

## Project structure

- `main.py` – CLI entry point  
- `modules/` – core logic (dictionary, hashes, brute-force, analyzer, report)  
- `sample_data/` – example shadow and NTLM files (fake data)  
- `wordlists/` – generated dictionaries  
- `reports/` – generated reports  
- `docs/` – diagrams and documentation assets