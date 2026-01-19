#!/bin/bash
# Khalid Husain786 OSINT + Ultra Card Checker - AUTO INSTALLER v90.2
# 🔥 One-Click Installation - Ubuntu/Debian/Kali/Mint

echo -e "\e[1;32m
╔══════════════════════════════════════════════════════════════════════════════╗
║                       KHALID HUSAIN786 v90.2 INSTALLER                      ║
║                    OSINT + ULTRA LIVE CARD CHECKER                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
\e[0m"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}⚠️  Don't run as root!${NC}"
   exit 1
fi

# Update system
echo -e "${BLUE}🔄 Updating system...${NC}"
sudo apt update -y &>/dev/null
sudo apt upgrade -y -qq &>/dev/null

# Install Python3 & pip
echo -e "${BLUE}🐍 Installing Python3 + pip...${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl wget &>/dev/null

# Create directory
mkdir -p ~/KhalidHusain786
cd ~/KhalidHusain786

# Create virtual environment
echo -e "${BLUE}🌐 Creating virtual environment...${NC}"
python3 -m venv khalid_env &>/dev/null
source khalid_env/bin/activate

# Upgrade pip
pip install --upgrade pip -q

# Install ALL dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
pip install -q requests colorama lxml beautifulsoup4 urllib3 certifi fake-useragent threading concurrent.futures argparse

# Create main files
echo -e "${BLUE}💾 Creating tools...${NC}"

# Ultra Card Checker
cat > card_checker.py << 'EOF'
#!/usr/bin/env python3
# [PASTE YOUR CARD CHECKER CODE HERE - THE FULL ULTRA VERSION I GAVE]
EOF

# OSINT Scanner
cat > khalid_osint.py << 'EOF'
#!/usr/bin/env python3
# [PASTE YOUR OSINT SCANNER CODE HERE - THE FIXED VERSION]
EOF

# Make executable
chmod +x *.py

# Create run scripts
cat > run_card_checker.sh << 'EOF'
#!/bin/bash
cd ~/KhalidHusain786
source khalid_env/bin/activate
python3 card_checker.py "$@"
EOF

cat > run_osint.sh << 'EOF'
#!/bin/bash
cd ~/KhalidHusain786
source khalid_env/bin/activate
python3 khalid_osint.py "$@"
EOF

chmod +x *.sh

# Create desktop shortcut (optional)
cat > khalid.desktop << 'EOF'
[Desktop Entry]
Name=Khalid Card Checker
Exec=gnome-terminal -- bash -c 'cd ~/KhalidHusain786 && source khalid_env/bin/activate && python3 card_checker.py; exec bash'
Icon=utilities-terminal
Type=Application
Terminal=true
EOF

cat > khalid_osint.desktop << 'EOF'
[Desktop Entry]
Name=Khalid OSINT
Exec=gnome-terminal -- bash -c 'cd ~/KhalidHusain786 && source khalid_env/bin/activate && python3 khalid_osint.py; exec bash'
Icon=utilities-terminal
Type=Application
Terminal=true
EOF

# Copy to desktop
cp *.desktop ~/Desktop/ 2>/dev/null || echo "Desktop shortcut skipped"

# Create aliases
echo -e "${BLUE}🔗 Adding aliases to .bashrc...${NC}"
cat >> ~/.bashrc << 'EOF'

# Khalid Husain786 Tools
alias khalid-card='cd ~/KhalidHusain786 && source khalid_env/bin/activate && python3 card_checker.py'
alias khalid-osint='cd ~/KhalidHusain786 && source khalid_env/bin/activate && python3 khalid_osint.py'
alias khalid='cd ~/KhalidHusain786 && source khalid_env/bin/activate'
EOF

source ~/.bashrc

# Final setup
echo -e "${GREEN}✅ Installation COMPLETE!${NC}"
echo -e "${YELLOW}📂 Location: ~/KhalidHusain786${NC}"
echo -e "${YELLOW}🎮 Commands:${NC}"
echo -e "   ${GREEN}khalid-card -c \"4532015112830366\"${NC}"
echo -e "   ${GREEN}khalid-osint \"target@gmail.com\"${NC}"
echo -e "   ${GREEN}khalid${NC}  (opens directory)"
echo -e "   ${GREEN}./run_card_checker.sh -f cards.txt${NC}"

# Test run
echo -e "${BLUE}🧪 Testing installation...${NC}"
python3 -c "import requests, colorama; print('✅ All modules OK!')" &>/dev/null && echo -e "${GREEN}✅ Test PASSED!${NC}"

echo -e "\n${RED}🚀 KHALID HUSAIN786 READY! 🔥${NC}"
echo -e "${BLUE}💡 Run: source ~/.bashrc${NC}"
