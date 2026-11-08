def scan_ports(subdomains):
    if not subdomains:
        return
    
    targets = subdomains[:10] 
    print(f"\n[*] Starting Nmap scan on first 10 subdomains...")
    
    with open("targets.txt", "w") as f:
        f.write("\n".join(targets))
        
    # Added -Pn here to skip host discovery (ping check) and just scan ports
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
        
        for sub in subdomains[:20]:
            f.write(f"- {sub}\n")
            
        if os.path.exists("nmap_results.txt"):
            f.write("\n## Nmap Scan Results\n")
            with open("nmap_results.txt", "r") as nmap_file:
                # Read the entire file and find lines with Ports
                for line in nmap_file:
                    if "Ports:" in line:
                        f.write(f"```text\n{line.strip()}\n```\n")
                        
    print(f"[+] Report generated: {filename}")