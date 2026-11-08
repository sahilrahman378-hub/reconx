#!/usr/bin/env python3
import subprocess
import argparse
import sys

def run_command(command):
    """Helper function to run shell commands"""
    try:
        # stderr কে দূরে রাখছি যাতে স্ক্রিনে অযথা এরর না দেখায়
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
    print(f"[*] Searching subdomains for: {domain}")
    # subfinder কমান্ড রান করছি
    cmd = f"subfinder -d {domain} -silent"
    output = run_command(cmd)
    
    if not output:
        print("[!] No subdomains found or subfinder failed.")
        return []
    
    subdomains = output.split("\n")
    print(f"[+] Found {len(subdomains)} subdomains.")
    return subdomains

def main():
    parser = argparse.ArgumentParser(description="ReconX - OSINT Automation Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    args = parser.parse_args()

    print("="*40)
    print(" ReconX - OSINT Recon Automation ")
    print("="*40)

    subdomains = find_subdomains(args.domain)
    
    if subdomains:
        print("\n[Sample Results]")
        for sub in subdomains[:5]: # প্রথম ৫টা দেখাচ্ছি
            print(f" - {sub}")

if __name__ == "__main__":
    main()