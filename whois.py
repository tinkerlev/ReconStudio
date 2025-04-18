# whois_info.py

"""
Module: whois_info.py

Description:
This module performs a WHOIS lookup for a given domain and extracts relevant registration data.
It uses the Python 'whois' package to collect domain information such as registrar, creation date,
expiration date, and name servers.

Features:
- Lightweight and simple WHOIS lookup
- Cleans and formats raw WHOIS data
- Returns structured dictionary output
- Measures runtime and prints it to the console
- Saves result to a TXT file

Usage:
This module is intended to be used as part of the ReconStudio toolkit.
It can also be tested independently by calling `get_whois(domain)` or running from the CLI:

    python3 whois_info.py example.com

Dependencies:
- python-whois
- time

Limitations:
- Some domains may not return complete WHOIS data
- WHOIS servers may rate-limit repeated queries
- Requires internet access
- Saves results to a TXT file under data/
"""

import whois
import os
import time

def get_whois(domain):
    if os.name == 'nt':
        print("[!] Note: WHOIS results may vary on Windows systems. Consider using WSL or Linux for consistency.")
    print(f"[*] Performing WHOIS lookup for: {domain}")
    start_time = time.time()

    try:
        info = whois.whois(domain)

        result = {
            "domain_name": info.domain_name,
            "registrar": info.registrar,
            "creation_date": str(info.creation_date),
            "expiration_date": str(info.expiration_date),
            "name_servers": info.name_servers,
            "status": info.status,
            "emails": info.emails
        }

        duration = round(time.time() - start_time, 2)
        print(f"[✓] WHOIS completed in {duration} seconds")

        # Save result to TXT file
        os.makedirs("data", exist_ok=True)
        txt_path = f"data/whois_{domain}.txt"
        with open(txt_path, "w") as f:
            for key, value in result.items():
                f.write(f"{key}: {value}\n")
        print(f"[✓] WHOIS data saved to: {txt_path}")

        return result

    except Exception as e:
        duration = round(time.time() - start_time, 2)
        print(f"[!] WHOIS lookup failed after {duration} seconds: {e}")
        return {}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 whois_info.py <domain>")
        exit(1)
    get_whois(sys.argv[1])