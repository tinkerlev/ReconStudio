# main.py

"""
Main entry point for ReconStudio - A modular website reconnaissance toolkit.

This script ties together all modules:
- Subdomain enumeration
- WHOIS lookup
- theHarvester passive collection
- Report generation in multiple formats

Usage:
    python3 main.py <target_domain> [--subdomains] [--whois] [--harvest] [-o output.json]

If no modules are selected, all will run by default.
"""

import argparse
import os
import time
import json
import logging

from modules import subdomains, whois_info, theharvester, report_generator

def run_recon(target, output_path, do_subdomains, do_harvest, do_whois):
    logging.info(f"Starting Recon on: {target}")
    print(f"[+] Starting Recon on: {target}\n")

    data = {"target": target}
    start = time.time()

    if do_subdomains:
        print("[*] Collecting subdomains...")
        subdomains_list = subdomains.get_subdomains(target)
        data["subdomains"] = subdomains_list
        logging.info(f"Collected {len(subdomains_list)} subdomains")
    else:
        data["subdomains"] = []

    if do_harvest:
        print("[*] Running theHarvester module...")
        harvest_data = theharvester.run_harvest(target)
        data["theharvester"] = harvest_data
        logging.info("theHarvester module completed")
    else:
        data["theharvester"] = {}

    if do_whois:
        print("[*] Performing WHOIS lookup...")
        whois_data = whois_info.get_whois(target)
        data["whois"] = whois_data
        logging.info("WHOIS lookup completed")
    else:
        data["whois"] = {}

    try:
        json.dumps(data)
    except Exception as e:
        print(f"[!] Failed to serialize data: {e}")
        logging.error(f"Failed to serialize data: {e}")
        exit(1)

    print("[*] Generating report...")
    report_generator.generate_report(data, output_path)
    logging.info(f"Report saved to {output_path}.*")
    print("\n--- Recon Summary ---")
    print(f"  Subdomains found: {len(data['subdomains'])}")
    print(f"  Emails/domains harvested: {len(data['theharvester'].get('emails', []) if isinstance(data['theharvester'], dict) else 0)}")
    print(f"  Report base path: {output_path}.*")
    print(f"  Total time: {round(time.time() - start, 2)} seconds")
    logging.info("Recon completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ReconStudio - Website Intelligence Toolkit")
    parser.add_argument("target", help="Target domain to scan (e.g. example.com)")
    parser.add_argument("-o", "--output", default="data/output", help="Base path to save the report")
    parser.add_argument("--subdomains", action="store_true", help="Collect subdomains")
    parser.add_argument("--harvest", action="store_true", help="Run theHarvester module")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(message)s'
    )

    run_recon(
        target=args.target,
        output_path=args.output,
        do_subdomains=args.subdomains or not (args.subdomains or args.harvest or args.whois),
        do_harvest=args.harvest or not (args.subdomains or args.harvest or args.whois),
        do_whois=args.whois or not (args.subdomains or args.harvest or args.whois)
    )