# ReconX - OSINT Recon Automation Tool

ReconX is a lightweight, automated reconnaissance tool written in Python. It streamlines the initial information gathering phase of penetration testing by combining multiple industry-standard tools into a single pipeline.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Features
- **WHOIS Lookup:** Gathers domain registration information.
- **DNS Enumeration:** Finds A records for the target domain.
- **Subdomain Enumeration:** Automatically finds subdomains using `subfinder`.
- **Port Scanning:** Scans the top 10 discovered subdomains (or the main domain if no subdomains are found) using `nmap` with the `-Pn` flag.
- **Live Server Detection:** Uses `httpx-toolkit` to check which discovered hosts have live HTTP/HTTPS servers and retrieves their status codes and titles.
- **Report Generation:** Generates a clean Markdown report (`*_recon_report.md`) summarizing all findings.

## Prerequisites
- Python 3
- Subfinder (Kali: `sudo apt install subfinder`)
- Nmap (Kali: `sudo apt install nmap`)
- HTTPX-Toolkit (Kali: `sudo apt install httpx-toolkit`)

## Installation
```bash
git clone https://github.com/sahilrahman378-hub/reconx.git
cd reconxss