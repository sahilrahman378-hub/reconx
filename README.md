# ReconX - OSINT Recon Automation Tool

ReconX is a lightweight, automated reconnaissance tool written in Python. It combines `subfinder` and `nmap` to streamline the initial information gathering phase of penetration testing.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features
- **Subdomain Enumeration:** Automatically finds subdomains using `subfinder`.
- **Port Scanning:** Scans the top 10 discovered subdomains (or the main domain if no subdomains are found) using `nmap` with `-Pn` flag.
- **Report Generation:** Generates a clean Markdown report (`*_recon_report.md`) summarizing the findings.

## Prerequisites
- Python 3
- Subfinder (Kali: `sudo apt install subfinder`)
- Nmap (Kali: `sudo apt install nmap`)

## Installation
```bash
git clone https://github.com/sahilrahman378-hub/reconx.git
cd reconx