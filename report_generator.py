# report_generator.py

"""
Module: report_generator.py

Description:
This module generates a report from the collected reconnaissance data.
It allows the user to choose between output formats: JSON, HTML, PDF, or TXT.

Features:
- Supports multiple output formats
- Saves reports to the 'data/' directory
- Displays save path confirmation to the user

Usage:
Call generate_report(data, output_path) where data is a dictionary
and output_path is the base file path without extension.

Dependencies:
- json
- os
- time
- jinja2 (for HTML)
- fpdf (for PDF)

Limitations:
- PDF requires the 'fpdf' package
- HTML requires the 'jinja2' package and a basic template
"""

import os
import json
import time

from fpdf import FPDF
from jinja2 import Template

def generate_report(data, output_path):
    os.makedirs("data", exist_ok=True)
    print("[*] Choose output format: [1] JSON, [2] TXT, [3] HTML, [4] PDF")
    choice = input("Enter option number: ").strip()
    start = time.time()

    if choice == '1':
        with open(output_path + ".json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"[✓] Report saved to: {output_path}.json")

    elif choice == '2':
        with open(output_path + ".txt", "w") as f:
            for section, content in data.items():
                f.write(f"[{section.upper()}]\n")
                f.write(f"{json.dumps(content, indent=2)}\n\n")
        print(f"[✓] Report saved to: {output_path}.txt")

    elif choice == '3':
        html_template = Template("""
        <html>
        <head><title>Recon Report</title></head>
        <body>
        <h1>ReconStudio Report</h1>
        {% for section, content in data.items() %}
            <h2>{{ section }}</h2>
            <pre>{{ content | tojson(indent=2) }}</pre>
        {% endfor %}
        </body>
        </html>
        """)
        html_content = html_template.render(data=data)
        with open(output_path + ".html", "w") as f:
            f.write(html_content)
        print(f"[✓] Report saved to: {output_path}.html")

    elif choice == '4':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Recon Report", ln=True, align='C')
        for section, content in data.items():
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt=section.upper(), ln=True)
            pdf.set_font("Arial", size=10)
            lines = json.dumps(content, indent=2).split("\n")
            for line in lines:
                pdf.multi_cell(0, 10, txt=line)
        pdf.output(output_path + ".pdf")
        print(f"[✓] Report saved to: {output_path}.pdf")

    else:
        print("[!] Invalid option. No report was generated.")

    print(f"[✓] Report generation completed in {round(time.time() - start, 2)} seconds")