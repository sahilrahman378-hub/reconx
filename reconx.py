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

def find_subdomains(domain):
    print(f"\n[*] Searching subdomains for: {domain}")
    cmd = f"subfinder -d {domain} -silent"
    output = run_command(cmd)
    
    if not output:
        print("[!] No subdomains found.")
        return []
    
    subdomains = output.split("\n")
    print(f"[+] Found {len(subdomains)} subdomains.")
    return subdomains

def scan_ports(subdomains):
    if not subdomains:
        return
    
    # Taking the first 10 subdomains to make the scan faster
    targets = subdomains[:10] 
    print(f"\n[*] Starting Nmap scan on first 10 subdomains...")
    
    # Saving the domains to a text file
    with open("targets.txt", "w") as f:
        f.write("\n".join(targets))
        
    # Nmap command: added -Pn to skip ping and force scan
    cmd = "nmap -iL targets.txt -p 80,443,22,21 -T4 -Pn -oG nmap_results.txt"
    print("[*] Nmap is running... Please wait.")
    
    run_command(cmd)
    print("[+] Nmap scan complete. Results saved in nmap_results.txt")

def generate_report(domain, subdomains):
    print(f"\n[*] Generating final report...")
    filename = f"{domain}_recon_report.md"
    
    with open(filename, "w") as f:
        f.write(f"# OSINT Recon Report: {domain}\n\n")
        f.write(f"**Total Subdomains Found:** {len(subdomains)}\n\n")
        f.write("## Subdomains List (Sample)\n")
        
        # Showing the first 20 in the report
        for sub in subdomains[:20]:
            f.write(f"- {sub}\n")
            
        if os.path.exists("nmap_results.txt"):
            f.write("\n## Nmap Scan Results\n")
            with open("nmap_results.txt", "r") as nmap_file:
                # Reading the whole file to find lines with Ports
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

    subdomains = find_subdomains(args.domain)
    
    if subdomains:
        scan_ports(subdomains)
        generate_report(args.domain, subdomains)

if __name__ == "__main__":
    main()