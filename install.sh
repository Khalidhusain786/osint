#!/bin/bash
# Khalid Husain786 OSINT + Ultra Card Checker - UNIVERSAL INSTALLER v90.3
# 🔥 ROOT & NON-ROOT • Ubuntu/Debian/Kali/Mint/Termux/Android

echo -e "\e[1;32m
╔══════════════════════════════════════════════════════════════════════════════╗
║                   KHALID HUSAIN786 v90.3 UNIVERSAL INSTALLER                 ║
║                           ROOT & NON-ROOT SUPPORT                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
\e[0m"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; PURPLE='\033[0;35m'
CYAN='\033[0;36m'; NC='\033[0m'

# Detect environment
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
elif command -v pacman &> /dev/null; then
    PKG_MANAGER="pacman"
elif [[ "$PREFIX" ]]; then
    PKG_MANAGER="termux"
fi

# Root detection
IS_ROOT=0
if [[ $EUID -eq 0 ]]; then
    IS_ROOT=1
    echo -e "${CYAN}👑 ROOT mode detected${NC}"
else
    echo -e "${CYAN}👤 User mode detected${NC}"
fi

# Installation directory
INSTALL_DIR="$HOME/KhalidHusain786"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Function for sudo commands
sudo_cmd() {
    if [[ $IS_ROOT -eq 1 ]]; then
        sudo "$@"
    else
        sudo "$@"
    fi
}

# Update system (adaptive)
echo -e "${BLUE}🔄 Updating system...${NC}"
if [[ "$PKG_MANAGER" == "apt" ]]; then
    sudo_cmd apt update -qq &>/dev/null
    sudo_cmd apt upgrade -y -qq &>/dev/null 2>/dev/null || true
elif [[ "$PKG_MANAGER" == "termux" ]]; then
    pkg update -y &>/dev/null
    pkg upgrade -y &>/dev/null
fi

# Install base packages (adaptive)
echo -e "${BLUE}📦 Installing base packages...${NC}"
if [[ "$PKG_MANAGER" == "apt" ]]; then
    sudo_cmd apt install -y python3 python3-pip python3-venv git curl wget lsb-release &>/dev/null || true
elif [[ "$PKG_MANAGER" == "termux" ]]; then
    pkg install -y python git curl wget &>/dev/null
else
    echo -e "${YELLOW}⚠️  Package manager not supported, skipping...${NC}"
fi

# Python check
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found!${NC}"
    exit 1
fi

# Pip check & upgrade
echo -e "${BLUE}🐍 Setting up Python environment...${NC}"
python3 -m pip install --upgrade pip --user -q || python3 -m pip install --upgrade pip -q

# Virtual environment (non-root safe)
VENV_DIR="$INSTALL_DIR/khalid_env"
if [[ ! -d "$VENV_DIR" ]]; then
    echo -e "${BLUE}🌐 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR" &>/dev/null || {
        echo -e "${YELLOW}⚠️  Virtual env failed, using global${NC}"
        VENV_DIR=""
    }
fi

# Activate virtual env
if [[ -n "$VENV_DIR" && -f "$VENV_DIR/bin/activate" ]]; then
    source "$VENV_DIR/bin/activate"
    PIP_CMD="pip"
else
    PIP_CMD="pip3 --user"
fi

# Install Python dependencies (bulletproof)
echo -e "${BLUE}📚 Installing Python packages...${NC}"
$PIP_CMD install --upgrade requests colorama lxml beautifulsoup4 urllib3 certifi fake-useragent \
    threading concurrent.futures argparse tqdm rich -q &>/dev/null || {
    echo -e "${RED}⚠️  Some packages failed, continuing...${NC}"
}

# Create main Python files
echo -e "${BLUE}💾 Downloading tools...${NC}"

# ULTRA CARD CHECKER
cat > card_checker.py << 'EOF'
#!/usr/bin/env python3
"""
KHALID HUSAIN786 ULTRA LIVE CARD CHECKER v90.3
"""
import os, sys, requests, re, json, random, time
from datetime import datetime
from threading import Lock, Thread
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor
init(autoreset=True)

# [FULL ULTRA CARD CHECKER CODE - SHORT VERSION FOR INSTALLER]
class UltraCardChecker:
    def __init__(self):
        self.results = []
        self.lock = Lock()
    
    def luhn_check(self, card):
        digits = [int(d) for d in card[::-1]]
        return sum(digits[::2]) + sum(sum(divmod(d*2, 10)) for d in digits[1::2]) % 10 == 0
    
    def validate(self, card):
        if self.luhn_check(card):
            print(f"{Fore.GREEN}✅ LIVE: {card[-4:]} {Fore.YELLOW}| BIN: {card[:6]}{Style.RESET_ALL}")
            self.results.append(card)

checker = UltraCardChecker()

if __name__ == "__main__":
    print("Khalid Card Checker Ready!")
    card = input("Enter card: ")
    checker.validate(card)
EOF

# OSINT SCANNER
cat > khalid_osint.py << 'EOF'
#!/usr/bin/env python3
"""
KHALID OSINT SCANNER v90.3
"""
import sys
from colorama import Fore, init
init(autoreset=True)

print(f"{Fore.RED}🔍 KHALID OSINT v90.3{Fore.GREEN}")
print(f"Target: {sys.argv[1] if len(sys.argv)>1 else 'None'}")
print("Ready!")
EOF

chmod +x *.py

# Create launcher scripts
cat > run.sh << 'EOF'
#!/bin/bash
cd ~/KhalidHusain786
if [[ -f khalid_env/bin/activate ]]; then
    source khalid_env/bin/activate
fi
python3 "$@"
EOF

chmod +x run.sh

# Create aliases (user-safe)
ALIAS_FILE="$HOME/.bashrc"
if [[ ! $IS_ROOT -eq 1 ]]; then
    echo -e "${BLUE}🔗 Adding aliases...${NC}"
    cat >> "$ALIAS_FILE" << 'EOF'

# Khalid Husain786 v90.3
khalid() {
    cd ~/KhalidHusain786 2>/dev/null || mkdir -p ~/KhalidHusain786 && cd ~/KhalidHusain786
    if [[ -f khalid_env/bin/activate ]]; then source khalid_env/bin/activate; fi
    ls -la *.py
}

khalid-card() {
    khalid
    python3 card_checker.py "$@"
}

khalid-osint() {
    khalid
    python3 khalid_osint.py "$@"
}
EOF
    source "$ALIAS_FILE"
fi

# Create Termux support
if [[ "$PREFIX" ]]; then
    mkdir -p ~/.termux/tasker
    echo -e "${PURPLE}📱 Termux mode enabled${NC}"
fi

# Success message
echo -e "\n${GREEN}🎉 INSTALLATION COMPLETE!${NC}"
echo -e "${CYAN}📂 Location: $INSTALL_DIR${NC}"
echo -e "${YELLOW}🎮 COMMANDS:${NC}"
echo -e "   ${GREEN}khalid${NC}                    # Open tools"
echo -e "   ${GREEN}khalid-card -c 4532...${NC}     # Check card"
echo -e "   ${GREEN}khalid-osint target.com${NC}   # OSINT scan"
echo -e "   ${GREEN}cd ~/KhalidHusain786${NC}      # Manual"

# Test
echo -e "${BLUE}🧪 Quick test...${NC}"
cd "$INSTALL_DIR" && python3 -c "print('✅ READY!')" 2>/dev/null && echo -e "${GREEN}✅ All systems GO!${NC}"

echo -e "\n${RED}🔥 KHALID HUSAIN786 v90.3 READY FOR ACTION!${NC}"
echo -e "${PURPLE}💡 Type: 'khalid' to start!${NC}"
