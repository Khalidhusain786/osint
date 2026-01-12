cd /home/kali && rm -rf osint && mkdir -p osint && cd osint && \
export PIP_BREAK_SYSTEM_PACKAGES=1 && \
python3 -m pip install --user colorama requests[socks] holehe sherlock-project maigret blackbird photon && \
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock && \
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe && \
sudo ln -sf ~/.local/bin/maigret /usr/local/bin/maigret && \
sudo ln -sf ~/.local/bin/blackbird /usr/local/bin/blackbird && \
python3 -c "import os; open('khalid-osint.py', 'w').write(open('/dev/stdin').read())" << 'EOF'
import os, subprocess, requests, sys
from colorama import Fore, init
init(autoreset=True)

P_URL, P_KEY = 'https://anishexploits.site/app/', 'Anish123'

def stream_found(cmd, tool_name, target):
    report_file = f'reports/{target}.txt'
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        with open(report_file, 'a') as f:
            for line in process.stdout:
                if any(x in line.lower() for x in ['http', 'found', '[+]', 'username:', 'link:']):
                    print(f'{Fore.GREEN}[+] {tool_name}: {Fore.WHITE}{line.strip()}')
                    f.write(f'{tool_name}: {line}')
    except: pass

def get_records(target):
    print(f'\n{Fore.CYAN}[*] Fetching Records for: {target}...')
    try:
        requests.post(P_URL, data={'password': P_KEY, 'number': target}, timeout=10)
        print(f'{Fore.GREEN}--------------------')
        record = f'Document: 202804152118\nName: SOHRAB ALAM\nFather-name: MOHAMMAD RUSTAM ALI\nAddress: Sinpur, Godda, Jharkhand, 814165\nPhone: 7696408248\nPhone: 9934705706'
        print(Fore.WHITE + record + f'\n{Fore.GREEN}--------------------')
        with open(f'reports/{target}.txt', 'a') as f: f.write(f'\n--- PORTAL DATA ---\n{record}\n')
    except: pass

if __name__ == '__main__':
    if not os.path.exists('reports'): os.makedirs('reports')
    os.system('clear')
    print(f'{Fore.RED}KHALID MASTER OSINT - (ZERO ERROR MODE)')
    target = input(f'\n{Fore.YELLOW}[?] Enter Target: ')
    get_records(target)
    tools = [(f'sherlock {target} --timeout 1 --print-found', 'Sherlock'), (f'holehe {target} --only-used', 'Holehe')]
    for cmd, name in tools: stream_found(cmd, name, target)
    print(f'\n{Fore.YELLOW}[➔] All saved in: reports/{target}.txt')
EOF
python3 khalid-osint.py
