# Environment clean-up aur essential fixes
export PIP_BREAK_SYSTEM_PACKAGES=1
sudo apt remove -y python3-logilab-astng
python3 -m pip install --user --upgrade setuptools pip
python3 -m pip install --user social-analyzer sherlock-project holehe maigret

# Path link fix taaki 'not found' error na aaye
sudo ln -sf ~/.local/bin/social-analyzer /usr/local/bin/social-analyzer
sudo ln -sf ~/.local/bin/sherlock /usr/local/bin/sherlock
sudo ln -sf ~/.local/bin/holehe /usr/local/bin/holehe
