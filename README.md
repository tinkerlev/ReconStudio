# 🚀 ReconStudio - Modular Website Intelligence Toolkit

<p align="center">
  <img src="https://img.shields.io/badge/Bash-Toolkit-black?style=flat-square&logo=gnubash"/>
  <img src="https://img.shields.io/badge/Nmap-FullScan-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/OSINT-Passive-green?style=flat-square"/>
  <img src="https://img.shields.io/badge/Red%20Team-Offensive-important?style=flat-square"/>
  <img src="https://img.shields.io/badge/Recon-Phase1-critical?style=flat-square&logo=airplayaudio"/>
  <img src="https://img.shields.io/badge/Service-Version%20Detection-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Curl-Manual%20Testing-black?style=flat-square&logo=curl"/>
  <img src="https://img.shields.io/badge/No-Frameworks-success?style=flat-square"/>
  <img src="https://img.shields.io/badge/Ethical-Use%20Only-green?style=flat-square"/>
</p>

**ReconStudio** is a modular, extensible reconnaissance tool built for **cybersecurity researchers, penetration testers, and ethical hackers**. It automates the process of collecting intelligence on public-facing web domains, with support for subdomains, WHOIS, passive data harvesting, and report generation in multiple formats.

> ⚠️ For **authorized and educational use only**. Do **not** run this tool on domains you do not have permission to test.

---

## 📚 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Report Formats](#-report-formats)
- [Sample Output](#-sample-output)
- [Security Considerations](#-security-considerations)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [Tests](#-tests)
- [Author](#-author)

---

## ✨ Features

- ✅ Subdomain enumeration using multiple techniques
- ✅ WHOIS lookup with error handling
- ✅ Passive data collection via `theHarvester`
- ✅ Choose between **PDF**, **HTML**, **TXT**, or **JSON** reports
- ✅ Input validation and rate limiting
- ✅ Smart CLI with logging, colored output, and progress bars
- ✅ Graceful error handling and dependency checks
- ✅ Aמג more

---

## 💾 Installation

### 1. Clone the repository:
```bash
git clone https://github.com/tinkerlev/ReconStudio.git
cd ReconStudio
```

### 2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Install system dependencies:

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-whois
```

#### Windows:
> Make sure `python` is in your system path and run:
```bash
pip install python-whois
```

### 4. Install `theHarvester`:
```bash
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip install -r requirements/base.txt
python3 theHarvester.py -h
```

---

## ⚙️ Usage

### Run full scan with default settings:
```bash
python3 main.py example.com
```

### Run specific modules:
```bash
python3 main.py example.com --subdomains --whois --harvest -o data/example
```

### Select report format from CLI:
```bash
python3 main.py example.com --format pdf
```

### Use custom API config file (for `theHarvester`):
```bash
python3 main.py example.com --config path/to/apis.conf
```

---

## 📾 Report Formats

| Format | Description | Output |
|--------|-------------|--------|
| `json` | Machine-readable | `example.json` |
| `txt`  | Plain text | `example.txt` |
| `html` | Styled HTML | `example.html` |
| `pdf`  | Printable | `example.pdf` |

> You can choose format interactively if not passed via `--format`.

---

## 📸 Sample Terminal Output
```
[+] Starting Recon on: example.com
[*] Collecting subdomains...
[✓] Collected 22 subdomains
[*] Running theHarvester...
[*] Performing WHOIS lookup...
[*] Generating report...
[✓] Report saved to: data/example.pdf

--- Recon Summary ---
  Target: example.com
  Subdomains found: 22
  Emails harvested: 5
  Hosts discovered: 3
  Total time: 8.3 seconds
```

---

## 🔒 Security Considerations

- Respects rate-limiting between requests
- Supports API token configuration
- Designed for safe use on authorized targets only
- Avoids excessive scanning or intrusive payloads

---

## 🥪 Tests

```bash
python -m pytest tests/
pytest --cov=./
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing dependency | Run: `pip install -r requirements.txt` |
| WHOIS timeout | Check network or reduce rate |
| JSON parse error | Verify `theHarvester` ran successfully |
| Output not saved | Ensure output path is valid and writable |

---

## 🤝 Contributing

We welcome contributions!

1. Fork the repo
2. Create a new branch: `git checkout -b my-feature`
3. Commit changes: `git commit -m 'add feature'`
4. Push and open a pull request

---

## 👨‍💻 Author

Built with ❤️ by [Loai Deeb](https://www.linkedin.com/in/loai-deeb/)  
🔗 GitHub: [tinkerlev](https://github.com/tinkerlev/ReconStudio)

---

**Stay ethical — and keep exploring 🔍💻**
