# ReconStudio - Modular Website Intelligence Toolkit

![License](https://img.shields.io/github/license/tinkerlev/ReconStudio)  
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)  
![Last Commit](https://img.shields.io/github/last-commit/tinkerlev/ReconStudio)

**ReconStudio** is a lightweight, modular, and beginner-friendly reconnaissance tool designed for ethical hackers, students, and cybersecurity researchers.
It helps automate the process of gathering intelligence on websites using subdomain enumeration, WHOIS lookups, email harvesting, and comprehensive report generation in various formats.

> ⚠️ **For educational and authorized use only. Do not run this tool on domains you do not have permission to test.**

---

## 📚 Table of Contents
- [🧠 What does ReconStudio do?](#-what-does-reconstudio-do)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📝 Report Formats](#-report-formats)
- [📸 Sample Output](#-sample-output-terminal)
- [🔐 Security and Limitations](#-security-and-limitations)
- [🧪 Tests](#-tests)
- [🛠 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)
- [🙋 About the Author](#-about-the-author)
- [📬 Questions or Feedback?](#-questions-or-feedback)

---

## 🧠 What does ReconStudio do?
- Finds subdomains using DNS brute force and passive APIs
- Collects WHOIS data (registrar, creation date, etc.)
- Harvests emails and subdomains using [theHarvester](https://github.com/laramies/theHarvester)
- Generates reports in **JSON**, **TXT**, **HTML**, or **PDF** formats
- Measures runtime and provides clear CLI feedback

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/tinkerlev/ReconStudio.git
cd ReconStudio
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

> The `requirements.txt` file lists all the Python libraries needed to run ReconStudio smoothly.
> 
> **Why is it important?**
> - ✅ Install all dependencies in one step
> - 🔁 Makes your project reproducible for others
> - 🔒 Optional: You can lock versions like `jinja2==3.1.2`
> - 📦 It's a best practice in every Python-based repository

### 3. Install system dependencies
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip python3-whois

# Windows
# Install Python 3.6+ from python.org
# Use PowerShell to install pip packages or WSL for Linux-based support
```

### 4. Required tools
- `theHarvester` (must be installed and accessible in PATH)
- `fpdf` (for PDF reports)
- `jinja2` (for HTML reports)
- `python-whois`

---

## 🚀 Usage

### Basic usage:
```bash
python3 main.py example.com
```
This will run **all modules by default** and prompt for a report format.

### Select modules manually:
```bash
python3 main.py example.com --subdomains --harvest --whois -o data/myreport
```

### Available flags:
| Flag           | Description                        |
|----------------|------------------------------------|
| `--subdomains` | Run subdomain enumeration          |
| `--harvest`    | Run theHarvester collection        |
| `--whois`      | Run WHOIS lookup                   |
| `-o`           | Output base path for the report    |

---

## 📝 Report Formats
When prompted, you can choose the format to export the results:

### [1] JSON
- Machine-readable
- Good for integrations
- Saved as `output.json`

### [2] TXT
- Human-readable with section headers
- Simple and lightweight
- Saved as `output.txt`

### [3] HTML
- Easy to read in browser
- Uses a styled HTML template (with `jinja2`)
- Saved as `output.html`

### [4] PDF
- Printable format with basic layout
- Uses `fpdf`
- Saved as `output.pdf`

---

## 📸 Sample Output (Terminal)
```
[+] Starting Recon on: example.com
[*] Collecting subdomains...
[✓] www.example.com -> 93.184.216.34
[*] Running theHarvester module...
[*] Performing WHOIS lookup...
[✓] Report saved to: data/output.json
--- Recon Summary ---
  Subdomains found: 10
  Emails/domains harvested: 7
  Report base path: data/output.*
  Total time: 12.8 seconds
```

---

## 🔐 Security and Limitations
- 🔁 Use rate limiting when querying external services
- 🔑 Support for API tokens (e.g., Hunter.io, Shodan)
- ⚠️ Use responsibly and only with explicit permission

---

## 🧪 Tests
```bash
# Run unit tests
python -m pytest tests/

# Run coverage tests
pytest --cov=./
```

---

## 🛠 Troubleshooting
- 🔒 Permission denied errors on first run? Use `chmod +x main.py` or run as admin
- 📦 Missing package errors? Re-check `pip install -r requirements.txt`
- 🖥 OS compatibility issues? Consider running under Linux/WSL for full support

---

## 🤝 Contributing
We welcome contributions! Here's how to get started:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/something`)
3. Add tests for your changes
4. Commit and push your code
5. Open a pull request with clear documentation

---

## 🙋 About the Author

ReconStudio was created by [Loai Deeb](https://www.linkedin.com/in/loai-deeb/), a cybersecurity lecturer and ethical hacking enthusiast who builds practical tools for real-world training and research.

GitHub Repository: [ReconStudio](https://github.com/tinkerlev/ReconStudio)

Feel free to contribute, fork, or suggest improvements!

---

## 📬 Questions or Feedback?
Open an issue on GitHub or connect with the author.

---

Stay ethical — and keep exploring 💻🔍