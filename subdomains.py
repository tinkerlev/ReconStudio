# subdomains.py

"""
Module: subdomains.py

Description:
This module performs deep subdomain enumeration for a given target domain using three different techniques:

1. DNS brute-force with a predefined wordlist.
2. Certificate transparency scraping via crt.sh.
3. Passive enumeration using the hackertarget.com API.

Each discovered subdomain is validated with an A record DNS lookup to confirm its existence.

Outputs:
- Prints all discovered and resolved subdomains to the console.
- Saves results to a TXT file in the 'data/' directory.
- Displays a summary including total findings and script runtime.

Usage:
This module is intended to be imported and used via the ReconStudio toolkit.
To run manually for testing, wrap the call to `get_subdomains(domain)` in a main block.

Dependencies:
- requests
- socket
- time
- os
- json
- urllib.parse.quote

Limitations:
- Currently only resolves A records.
- Uses a static wordlist; future updates may include dynamic input.
- Public APIs may rate-limit frequent queries.

"""

import socket
import os
import requests
import json
import time
from urllib.parse import quote

def get_subdomains(domain):
    os.makedirs("data", exist_ok=True)
    print(f"[*] Enumerating subdomains for: {domain}")
    start_time = time.time()

    found = set()

    # 1. DNS brute-force
    print("[*] Running DNS brute-force...")
    wordlist = ["www", "mail", "ftp", "admin", "test", "dev", "vpn", "api", "cpanel"]
    for sub in wordlist:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            print(f"[+] Found via brute-force: {subdomain} -> {ip}")
            found.add(subdomain)
        except socket.gaierror:
            continue

    # 2. crt.sh scraping
    print("[*] Querying crt.sh...")
    try:
        url = f"https://crt.sh/?q=%25.{quote(domain)}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            entries = response.json()
            for entry in entries:
                name_value = entry.get("name_value")
                if name_value:
                    for item in name_value.split("\n"):
                        if domain in item:
                            found.add(item.strip())
    except Exception as e:
        print(f"[!] crt.sh failed: {e}")

    # 3. hackertarget API
    print("[*] Querying hackertarget.com API...")
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().splitlines()
            for line in lines:
                parts = line.split(",")
                if len(parts) == 2:
                    found.add(parts[0].strip())
    except Exception as e:
        print(f"[!] hackertarget API failed: {e}")

    # Final resolution
    print("[*] Resolving found subdomains...")
    results = []
    for sub in sorted(found):
        try:
            ip = socket.gethostbyname(sub)
            print(f"[✓] {sub} -> {ip}")
            results.append({"subdomain": sub, "ip": ip})
        except socket.gaierror:
            continue

    # Save to TXT file
    txt_path = f"data/subdomains_{domain}.txt"
    with open(txt_path, "w") as f:
        for entry in results:
            f.write(f"{entry['subdomain']} -> {entry['ip']}\n")
    print(f"[✓] Subdomains saved to: {txt_path}")

    # Summary
    print("\n--- Subdomain Summary ---")
    print(f"  Total found: {len(found)}")
    print(f"  Resolved to IP: {len(results)}")
    print(f"  Runtime: {round(time.time() - start_time, 2)} seconds")

    return results