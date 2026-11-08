def scan_ports(subdomains, original_domain):
    # If no subdomains, scan the original domain itself
    if not subdomains:
        print(f"[!] No subdomains found. Scanning the main domain: {original_domain}")
        targets = [original_domain]
    else:
        # Taking the first 10 subdomains
        targets = subdomains[:10] 
        
    print(f"\n[*] Starting Nmap scan on: {', '.join(targets)}")
    
    with open("targets.txt", "w") as f:
        f.write("\n".join(targets))
        
    cmd = "nmap -iL targets.txt -p 80,443,22,21 -T4 -Pn -oG nmap_results.txt"
    print("[*] Nmap is running... Please wait.")
    
    run_command(cmd)
    print("[+] Nmap scan complete. Results saved in nmap_results.txt")

def main():
    parser = argparse.ArgumentParser(description="ReconX - OSINT Automation Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    args = parser.parse_args()

    print("========================================")
    print("      ReconX - OSINT Automation         ")
    print("========================================")

    subdomains = find_subdomains(args.domain)
    
    # Pass both subdomains and original domain to scan_ports
    scan_ports(subdomains, args.domain)
    
    # Generate report either way
    generate_report(args.domain, subdomains)