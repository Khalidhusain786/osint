#!/usr/bin/env bash

# ┌──────────────────────────────────────────────────────────────┐
# │     KHALID HUSAIN786 OSINT v90.1 - Installer                 │
# │     Installs dependencies and sets up the tool               │
# └──────────────────────────────────────────────────────────────┘

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
cat << "EOF"
╔════════════════════════════════════════════╗
║   KHALID HUSAIN786 OSINT v90.1 Installer   ║
║         Social • Docs • Live Cards         ║
╚════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ────────────────────────────────────────────────
# 1. Check if running as root (not strictly needed)
# ────────────────────────────────────────────────
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running installer as root is not recommended.${NC}"
    echo -e "Press Enter to continue anyway, or Ctrl+C to cancel."
    read -r
fi

# ────────────────────────────────────────────────
# 2. Install system dependencies
# ────────────────────────────────────────────────
echo -e "\n${GREEN}[+]${NC} Updating package list..."
sudo apt update -qq >/dev/null || { echo -e "${RED}[-] apt update failed${NC}"; exit 1; }

echo -e "${GREEN}[+]${NC} Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv git \
    || { echo -e "${RED}[-] Package installation failed${NC}"; exit 1; }

# ────────────────────────────────────────────────
# 3. Create virtual environment
# ────────────────────────────────────────────────
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}[i] Virtual environment already exists. Skipping creation.${NC}"
else
    echo -e "${GREEN}[+]${NC} Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR" || { echo -e "${RED}[-] venv creation failed${NC}"; exit 1; }
fi

# ────────────────────────────────────────────────
# 4. Activate venv & install Python packages
# ────────────────────────────────────────────────
echo -e "${GREEN}[+]${NC} Activating virtual environment and installing dependencies..."

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

pip install --upgrade pip -q
pip install colorama requests argparse urllib3 certifi -q || {
    echo -e "${RED}[-] pip install failed${NC}"
    deactivate
    exit 1
}

deactivate

# ────────────────────────────────────────────────
# 5. Create launcher script (optional but convenient)
# ────────────────────────────────────────────────
echo -e "${GREEN}[+]${NC} Creating launcher script: khalid-osint"

cat > khalid-osint << 'EOL'
#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/venv/bin/activate"
python3 "$DIR/khalid_osint_v901.py" "$@"
deactivate
EOL

chmod +x khalid-osint

# ────────────────────────────────────────────────
# 6. Final instructions
# ────────────────────────────────────────────────
echo -e "\n${GREEN}Installation completed!${NC}\n"

echo -e "To run the tool:"
echo -e "  ${CYAN}./khalid-osint \"target name or keyword\"${NC}"
echo -e "  or"
echo -e "  ${CYAN}source venv/bin/activate && python3 khalid_osint_v901.py \"target\"${NC}\n"

echo -e "${YELLOW}Note:${NC} This tool appears to be designed for finding leaked card data."
echo -e "Using it for illegal purposes is a serious crime in most countries."
echo -e "Use responsibly and only for legal security research.\n"

echo -e "${GREEN}Happy hunting... or whatever you're actually doing ¯\_(ツ)_/¯${NC}"
