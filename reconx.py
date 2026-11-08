#!/usr/bin/env python3
import subprocess
import argparse
import os

def run_command(command):
    """Helper function to run shell commands"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"[!] Error running command: {command}")
        return None

def get_whois(domain):
    print(f"\n[*] Getting WHOIS information for: {domain}")
    # Getting the first 15 lines to avoid a massive output
    cmd = f"whois {domain} | head -n 15"
    output = run_command(cmd)
    return output if output else "No WHOIS data found."

def get_dns(domain):
    print(f"[*] Getting DNS (A Records) for: {domain}")
    cmd = f"dig +short {domain} A"
    output = run_command(cmd)
    return output if output else "No DNS A records found."

def find_subdomains(domain):
    print(f"[*] Searching subdomains for: {domain}")
    cmd = f"subfinder -d {domain} -silent"
    output = run_command(cmd)
    
    if not output:
        print("[!] No subdomains found.")
        return []
    
    subdomains = output.split("\n")
    print(f"[+] Found {len(subdomains)} subdomains.")
    return subdomains

def scan_ports(subdomains, original_domain):
    if not subdomains:
        print(f"[!] No subdomains found. Scanning the main domain: {original_domain}")
        targets = [original_domain]
    else:
        targets = subdomains[:10] 
        
    print(f"\n[*] Starting Nmap scan on: {', '.join(targets)}")
    
    with open("targets.txt", "w") as f:
        f.write("\n".join(targets))
        
    cmd = "nmap -iL targets.txt -p 80,443,22,21 -T4 -Pn -oG nmap_results.txt"
    print("[*] Nmap is running... Please wait.")
    run_command(cmd)
    print("[+] Nmap scan complete. Results saved in nmap_results.txt")

def run_httpx():
    print(f"\n[*] Running HTTPX to find live web servers...")
    # Checking which targets have live web servers (Status 200, 301, etc.)
    cmd = "httpx -l targets.txt -silent -status-code -title"
    output = run_command(cmd)
    
    if output:
        print(f"[+] Found live HTTP servers.")
        return output
    else:
        print("[-] No live HTTP servers found.")
        return "No live web servers found."

def generate_report(domain, whois_info, dns_info, subdomains, httpx_info):
    print(f"\n[*] Generating final report...")
    filename = f"{domain}_recon_report.md"
    
    with open(filename, "w") as f:
        f.write(f"# OSINT Recon Report: {domain}\n\n")
        
        f.write("## WHOIS Information (Sample)\n")
        f.write(f"```text\n{whois_info}\n```\n\n")
        
        f.write("## DNS Records (A)\n")
        f.write(f"```text\n{dns_info}\n```\n\n")
        
        f.write(f"## Subdomains Found: {len(subdomains)}\n")
        if subdomains:
            f.write("### Subdomains List (Sample)\n")
            for sub in subdomains[:20]:
                f.write(f"- {sub}\n")
        else:
            f.write("No subdomains found.\n")
            
        f.write("\n## HTTPX (Live Web Servers)\n")
        f.write(f"```text\n{httpx_info}\n```\n\n")
            
        if os.path.exists("nmap_results.txt"):
            f.write("## Nmap Scan Results\n")
            with open("nmap_results.txt", "r") as nmap_file:
                for line in nmap_file:
                    if "Ports:" in line:
                        f.write(f"```text\n{line.strip()}\n```\n")
                        
    print(f"[+] Report generated: {filename}")

def main():
    parser = argparse.ArgumentParser(description="ReconX - OSINT Automation Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    args = parser.parse_args()

    print("========================================")
    print("      ReconX - OSINT Automation         ")
    print("========================================")

    # 1. WHOIS & DNS
    whois_info = get_whois(args.domain)
    dns_info = get_dns(args.domain)
    
    # 2. Subdomain Enumeration
    subdomains = find_subdomains(args.domain)
    
    # 3. Nmap Scan
    scan_ports(subdomains, args.domain)
    
    # 4. HTTPX Live Check (Requires httpx to be installed in Kali)
    httpx_info = run_httpx()
    
    # 5. Generate Report
    generate_report(args.domain, whois_info, dns_info, subdomains, httpx_info)

if __name__ == "__main__":
    main()
