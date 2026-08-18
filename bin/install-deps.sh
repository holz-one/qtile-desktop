#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting Multi-Distro Qtile & Desktop Dependencies Installer..."


# Core GUI, CLI tools, utilities, and audio stack across Ubuntu, Kali, and DietPi
CORE_APT_PACKAGES=(
    # Core Terminal & Shell
    "kitty"
    "git"
    "jq"
    "zsh"
    "htop"
    "curl"
    "openssh-client"
    "procps"
    "clamav" 
    "clamav-daemon" 
    "rkhunter"
    "chkrootkit"
    "playerctl"
    
    # Python & Build Headers
    "python3-pip"
    "python3-venv"
    "python3-xcffib"
    "python3-cairocffi"
    "python3-setuptools"
    "python3-dbus"
    "python3-gi"
    "python3-gi-cairo"
    "libgirepository1.0-dev"
    "libcairo2-dev"
    
    # Rofi, Desktop Utilities & Graphics
    "rofi"
    "feh"
    "brightnessctl"
    "libnotify-bin"
    "x11-xserver-utils"
    "papirus-icon-theme"
    "i3lock"
    
    # PipeWire & WirePlumber Audio Stack
    "pipewire"
    "pipewire-audio"
    "pipewire-alsa"
    "pipewire-pulse"
    "wireplumber"
)

echo "📦 Updating APT cache..."
sudo apt update

echo "📦 Installing core system dependencies..."
sudo apt install -y "${CORE_APT_PACKAGES[@]}"

# 1. Handle Qtile System Package vs. Pip Installation
if apt-cache show qtile &>/dev/null; then
    echo "✅ Installing Qtile via APT..."
    sudo apt install -y qtile
else
    echo "⚠️ 'qtile' package not found in APT. Installing Qtile via pip..."
    pip3 install --break-system-packages --user qtile
fi

# 2. Handle Qtile Extensions
echo "🐍 Installing Python Qtile extensions..."
pip3 install --break-system-packages --user --upgrade qtile-extras dbus-fast

# 3. Audio Stack Service Initialization
echo "🔊 Configuring PipeWire & WirePlumber user services..."
rm -rf ~/.local/state/wireplumber/

systemctl --user daemon-reload
systemctl --user --now enable pipewire pipewire-pulse wireplumber || true
systemctl --user restart pipewire pipewire-pulse wireplumber || true

# 4. Generate Sudoers Rules for Services
# Uses $HOME instead of ~ to ensure proper path expansion inside quotes
SUDO_SCRIPT="${HOME}/.config/qtile/bin/make_sudoer.sh"

if [ -f "$SUDO_SCRIPT" ]; then
    echo "🔑 Configuring passwordless systemctl permissions for installed services..."
    sudo "$SUDO_SCRIPT"
else
    echo "⚠️  Sudoer generator script not found at $SUDO_SCRIPT (skipping)"
fi



# 5. Install Oh-My-Zsh & Powerlevel10k Theme (Non-Interactive)
echo "🐚 Installing Oh-My-Zsh & Powerlevel10k theme..."
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    RUNZSH=no KEEP_ZSHRC=yes sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

P10K_DIR="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k"
if [ ! -d "$P10K_DIR" ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$P10K_DIR"
fi

if [ -f "$HOME/.zshrc" ]; then
    cp "$HOME/.zshrc" "$HOME/.zshrc.old"
    sed -i 's|ZSH_THEME=".*"|ZSH_THEME="powerlevel10k/powerlevel10k"|' "$HOME/.zshrc"
fi

# 6. Install Astral UV Package Manager
echo "⚡ Installing UV package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# 7. Run Interactive Git Configuration
GIT_SETUP_SCRIPT="${HOME}/.config/qtile/bin/setup-git.sh"
if [ -f "$GIT_SETUP_SCRIPT" ]; then
    chmod +x "$GIT_SETUP_SCRIPT"
    "$GIT_SETUP_SCRIPT"
fi

# 8. ClamAV Update
echo "📦 Updating Clam AV "
sudo systemctl stop clamav-freshclam
sudo freshclam
sudo systemctl start clamav-freshclam

# 9. RKHunter - update Rootkits and Backdoors data
echo "📦 Updating RKHunker "
sudo rkhunter --propupd          # Set baseline system properties
sudo rkhunter --update           # Update rootkit signatures

echo "✅ Installation complete across all detected packages!"
