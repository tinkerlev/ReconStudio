# theharvester.py

"""
Module: theharvester.py

Description:
This module integrates with theHarvester tool to passively collect emails, subdomains, hosts, and related information
from public sources. It supports both basic and extended (API-based) harvesting modes.

Features:
- Automatically detects OS and warns if run on unsupported platforms (e.g., native Windows)
- Allows optional usage of API keys for enhanced harvesting (e.g., Hunter.io, Shodan)
- Prompts user for API config path and verifies its existence
- Executes theHarvester using subprocess and parses the resulting JSON output
- Cleans up old output files if present
- Measures and prints total runtime to the console

Flags used:
- -d <domain>: Target domain to enumerate
- -b all: Use all available sources
- -f <filename>: Output file prefix
- -v: Verbose mode
- -s 0: Start index
- -l 100: Limit number of results
- -c <config>: Path to configuration file with API keys (optional)

Outputs:
- Prints discovery results to the console
- Returns structured data from parsed theHarvester JSON output
- Provides error handling for subprocess issues and output parsing

Usage:
This module is intended to be called by the ReconStudio toolkit via `run_harvest(domain)`.

Dependencies:
- subprocess
- shutil
- json
- os
- platform
- time

Limitations:
- Requires theHarvester to be installed and in PATH
- API enhancements require valid API keys
- Output file expected at <filename>.json
"""

import subprocess
import json
import shutil
import os
import platform
import time

os.makedirs("data", exist_ok=True)

def run_harvest(domain):
    start_time = time.time()
    print(f"[*] Harvesting data using theHarvester for domain: {domain}")

    if platform.system().lower() == "windows":
        print("[!] theHarvester may not run natively on Windows. Consider using WSL or Linux.")

    if shutil.which("theHarvester") is None:
        print("[!] theHarvester is not installed on your system.")
        print("[i] You can install it from: https://github.com/laramies/theHarvester")
        print("[i] Please install theHarvester to enable this module.")
        duration = round(time.time() - start_time, 2)
        print(f"[!] theHarvester finished with errors in {duration} seconds")
        return {}

    use_api = input("[?] Do you want to use APIs for extended results (e.g. Hunter.io)? (y/n): ").strip().lower()
    api_keys_path = None

    if use_api == 'y':
        while True:
            api_keys_path = input("[?] Enter the path to your API keys configuration file (or leave blank to skip): ").strip()
            if not api_keys_path:
                print("[!] No API key file provided. Proceeding without API enhancements.")
                api_keys_path = None
                break
            elif not os.path.isfile(api_keys_path):
                print(f"[!] File not found: {api_keys_path}")
                retry = input("[?] Would you like to enter a different path? (y/n): ").strip().lower()
                if retry != 'y':
                    print("[!] Proceeding without API enhancements.")
                    api_keys_path = None
                    break
            else:
                break

    output_format = "json"
    output_file = f"data/theharvester_{domain}.{output_format}"

    if os.path.exists(output_file + ".json"):
        os.remove(output_file + ".json")

    command = [
        "theHarvester",
        "-d", domain,
        "-b", "all",
        "-f", output_file,
        "-v",
        "-s", "0",
        "-l", "100"
    ]

    if api_keys_path:
        command += ["-c", api_keys_path]

    try:
        subprocess.run(command, check=True)
        with open(output_file + ".json", "r") as f:
            results = json.load(f)
            duration = round(time.time() - start_time, 2)
            print(f"[✓] theHarvester completed in {duration} seconds")
            return results

    except subprocess.CalledProcessError as e:
        print(f"[!] theHarvester failed to run: {e}")
    except FileNotFoundError:
        print(f"[!] Output file {output_file}.json not found. Check if theHarvester ran successfully.")
    except json.JSONDecodeError:
        print("[!] Failed to parse theHarvester output. Is the file valid JSON?")

    duration = round(time.time() - start_time, 2)
    print(f"[!] theHarvester finished with errors in {duration} seconds")
    return {}