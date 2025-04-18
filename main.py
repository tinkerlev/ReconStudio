# main.py

"""
ReconStudio - Advanced Website Intelligence Toolkit

ReconStudio is a modular and extensible reconnaissance tool designed for cybersecurity professionals, ethical hackers, and students. It allows deep intelligence gathering from public-facing domains in a customizable, scriptable, and user-friendly way.

Modules Included:
- Subdomain Enumeration: Passive and brute-force discovery of subdomains.
- WHOIS Analysis: Collects registrant and creation data from global WHOIS records.
- Email & Host Harvesting: Integration with theHarvester to collect emails, hosts, and more.
- Report Generator: Output results in various formats (JSON, TXT, HTML, PDF).

Key Features:
- Run specific modules or all by default
- Supports API-based enrichment (e.g. Hunter.io)
- Output customization and path selection
- CLI arguments for automation and scripting
- Progress bar, error logging, and runtime measurement

Usage:
    python3 main.py <target_domain> [--subdomains] [--whois] [--harvest] \
                     [-o output_base] [--format pdf|json|txt|html] [--config apis.conf]

If no modules are selected, all will run by default.
"""

import argparse
import os
import time
import json
import logging
import re
from tqdm import tqdm
from colorama import init, Fore, Style

from modules import subdomains, whois_info, theharvester, report_generator

init()  # Initialize colorama

CONFIG = {
    'timeout': 30,
    'max_retries': 3,
    'user_agent': 'ReconStudio/1.0',
    'rate_limit': 1.0  # requests per second
}

def setup_logging(output_dir):
    """Configure logging with rotation."""
    log_file = os.path.join(output_dir, 'recon.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def validate_domain(domain):
    """Validate domain name format."""
    pattern = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    return bool(re.match(pattern, domain.lower()))

def validate_report_format(format_str):
    """Validate the report format."""
    valid_formats = ['json', 'txt', 'html', 'pdf']
    return format_str.lower() in valid_formats

def validate_output_path(path):
    """Validate and create output directory if needed."""
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        return False

def check_dependencies():
    """Check if all required tools are installed."""
    try:
        import whois
        import fpdf
        import jinja2
        return True
    except ImportError as e:
        print(f"{Fore.RED}[!] Missing dependency: {e.name}{Style.RESET_ALL}")
        print("Please run: pip install -r requirements.txt")
        return False

def print_summary(data, output_path, report_format, start_time):
    """Print detailed scan summary."""
    print(f"\n{Fore.GREEN}--- Recon Summary ---{Style.RESET_ALL}")
    print(f"  Target: {data['target']}")
    print(f"  Subdomains found: {len(data['subdomains'])}")
    print(f"  Emails harvested: {len(data['theharvester'].get('emails', []))}")
    print(f"  Hosts discovered: {len(data['theharvester'].get('hosts', []))}")
    print(f"  Report saved as: {output_path}.{report_format}")
    print(f"  Total time: {round(time.time() - start_time, 2)} seconds")

def rate_limit(delay=1.0):
    """Simple rate limiting decorator."""
    def decorator(func):
        last_call = [0.0]
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < delay:
                time.sleep(delay - elapsed)
            result = func(*args, **kwargs)
            last_call[0] = time.time()
            return result
        return wrapper
    return decorator

def run_recon(target, output_path, do_subdomains, do_harvest, do_whois, report_format=None, config_path=None):
    try:
        logging.info(f"Starting Recon on: {target}")
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Starting Recon on: {target}\n")
        data = {"target": target}
        start = time.time()

        modules_to_run = sum([do_subdomains, do_harvest, do_whois])
        with tqdm(total=modules_to_run, desc="Modules completed") as pbar:

            if do_subdomains:
                print("[*] Collecting subdomains...")
                try:
                    subdomains_list = subdomains.get_subdomains(target)
                    data["subdomains"] = subdomains_list
                    logging.info(f"Collected {len(subdomains_list)} subdomains")
                except Exception as e:
                    logging.error(f"Subdomain enumeration failed: {e}")
                    data["subdomains"] = []
                pbar.update(1)
            else:
                data["subdomains"] = []

            if do_harvest:
                print("[*] Running theHarvester module...")
                try:
                    harvest_data = theharvester.run_harvest(target, config_path)
                    data["theharvester"] = harvest_data
                    logging.info("theHarvester module completed")
                except Exception as e:
                    logging.error(f"theHarvester failed: {e}")
                    data["theharvester"] = {}
                pbar.update(1)
            else:
                data["theharvester"] = {}

            if do_whois:
                print("[*] Performing WHOIS lookup...")
                try:
                    whois_data = whois_info.get_whois(target)
                    data["whois"] = whois_data
                    logging.info("WHOIS lookup completed")
                except ConnectionError:
                    logging.error("Network connection error during WHOIS lookup")
                    data["whois"] = {}
                except TimeoutError:
                    logging.error("WHOIS lookup timed out")
                    data["whois"] = {}
                except Exception as e:
                    logging.error(f"WHOIS lookup failed: {e}")
                    data["whois"] = {}
                pbar.update(1)
            else:
                data["whois"] = {}

        try:
            json.dumps(data)
        except Exception as e:
            print(f"[!] Failed to serialize data: {e}")
            logging.error(f"Failed to serialize data: {e}")
            exit(1)

        if not report_format:
            print("[?] Choose report format: (json / txt / html / pdf)")
            report_format = input("Format: ").strip().lower()

        if not validate_report_format(report_format):
            print(f"[!] Invalid report format. Choose from: json, txt, html, pdf")
            exit(1)

        print("[*] Generating report...")
        report_generator.generate_report(data, output_path, report_format)
        logging.info(f"Report saved to {output_path}.{report_format}")

        print_summary(data, output_path, report_format, start)
        logging.info("Recon completed.")

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
        logging.warning("Scan interrupted by user")
        return
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")
        return

if __name__ == "__main__":
    if not check_dependencies():
        exit(1)

    parser = argparse.ArgumentParser(description="ReconStudio - Website Intelligence Toolkit")
    parser.add_argument("target", help="Target domain to scan (e.g. example.com)")
    parser.add_argument("-o", "--output", default="data/output", help="Base path to save the report")
    parser.add_argument("--subdomains", action="store_true", help="Collect subdomains")
    parser.add_argument("--harvest", action="store_true", help="Run theHarvester module")
    parser.add_argument("--whois", action="store_true", help="Perform WHOIS lookup")
    parser.add_argument("--format", help="Report output format: json, txt, html, pdf")
    parser.add_argument("--config", help="Path to API configuration file for theHarvester")
    args = parser.parse_args()

    if not validate_domain(args.target):
        print("[!] Invalid domain format")
        exit(1)

    if not validate_output_path(args.output):
        print("[!] Invalid output path")
        exit(1)

    setup_logging("data")

    run_recon(
        target=args.target,
        output_path=args.output,
        do_subdomains=args.subdomains or not (args.subdomains or args.harvest or args.whois),
        do_harvest=args.harvest or not (args.subdomains or args.harvest or args.whois),
        do_whois=args.whois or not (args.subdomains or args.harvest or args.whois),
        report_format=args.format,
        config_path=args.config
    )