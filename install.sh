#!/usr/bin/env bash

# ┌──────────────────────────────────────────────────────────────┐
# │     KHALID HUSAIN786 OSINT v88.0 - MARIANA WEB INSTALLER     │
# │     Auto install all requirements - NO UPGRADE               │
# └──────────────────────────────────────────────────────────────┘

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
cat << "EOF"
╔════════════════════════════════════════════════════╗
║   KHALID HUSAIN786 v88.0 - MARIANA WEB INSTALLER   ║
║         1000+ Sites • Live Cards • Exact PII       ║
╚════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ────────────────────────────────────────────────
# 1. Install system dependencies (quiet mode)
# ────────────────────────────────────────────────
echo -e "\n${GREEN}[+]${NC} Installing required system packages..."

sudo apt update -qq >/dev/null 2>&1 || {
    echo -e "${RED}[-] Failed to update package list${NC}"
    exit 1
}

sudo apt install -yqq --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    >/dev/null 2>&1 || {
    echo -e "${RED}[-] Failed to install system packages${NC}"
    exit 1
}

# ────────────────────────────────────────────────
# 2. Create virtual environment
# ────────────────────────────────────────────────
VENV_DIR="venv"

if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}[i] Virtual environment already exists. Skipping creation.${NC}"
else
    echo -e "${GREEN}[+]${NC} Creating clean Python virtual environment..."
    python3 -m venv "$VENV_DIR" || {
        echo -e "${RED}[-] Failed to create virtual environment${NC}"
        exit 1
    }
fi

# ────────────────────────────────────────────────
# 3. Install only required Python packages (NO upgrade)
# ────────────────────────────────────────────────
echo -e "${GREEN}[+]${NC} Installing exact required Python packages..."

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

pip install --no-cache-dir --quiet \
    requests \
    colorama \
    || {
    echo -e "${RED}[-] Failed to install Python packages${NC}"
    deactivate
    exit 1
}

deactivate

# ────────────────────────────────────────────────
# 4. Create easy-to-use launcher
# ────────────────────────────────────────────────
echo -e "${GREEN}[+]${NC} Creating launcher script: ./khalid88"

cat > khalid88 << 'EOL'
#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$DIR/venv/bin/activate"
python3 "$DIR/khalid-osint-v88.py" "$@"
deactivate
EOL

chmod +x khalid88

# ────────────────────────────────────────────────
# 5. Final message
# ────────────────────────────────────────────────
echo -e "\n${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Installation Complete!           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}\n"

echo -e "To run the tool:"
echo -e "   ${CYAN}./khalid88 \"target_name_or_email\"${NC}"
echo -e "   Example:"
echo -e "   ${CYAN}./khalid88 \"john.doe@gmail.com\"${NC}"
echo -e "   ${CYAN}./khalid88 \"ahyan123\"${NC}\n"

echo -e "${YELLOW}Note:${NC} Make sure your main script file is named:"
echo -e "     ${CYAN}khalid-osint-v88.py${NC}\n"

echo -e "${GREEN}All set! Now you can start Mariana Web scanning...${NC}"
echo -e "${CYAN}Use responsibly.${NC}\n"
