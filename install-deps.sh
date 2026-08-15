#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting Multi-Distro Qtile & Desktop Dependencies Installer..."

# Core GUI, utilities, and audio stack available across Ubuntu, Kali, and DietPi
CORE_APT_PACKAGES=(
    "kitty"
    "python3-pip"
    "python3-venv"
    "python3-xcffib"
    "python3-cairocffi"
    "python3-setuptools"
    "libgirepository1.0-dev"
    "libcairo2-dev"
    "rofi"
    "brightnessctl"
    "libnotify-bin"
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
    echo "⚠️ 'qtile' package not found in APT (e.g., DietPi/Debian base). Installing Qtile via pip..."
    pip3 install --break-system-packages --user qtile
fi

# 2. Handle Qtile Extensions (qtile-extras, dbus-fast)
echo "🐍 Installing Python Qtile extensions..."
pip3 install --break-system-packages --user --upgrade qtile-extras dbus-fast

# 3. Audio Stack Service Initialization
echo "🔊 Configuring PipeWire & WirePlumber user services..."
rm -rf ~/.local/state/wireplumber/

systemctl --user daemon-reload
systemctl --user --now enable pipewire pipewire-pulse wireplumber || true
systemctl --user restart pipewire pipewire-pulse wireplumber || true

# 4. Generate Sudoers Rules for Services (if present)

SUDO_SCRIPT="~/.config/qtile/make_sudoers.sh"

if [ -f "$SUDO_SCRIPT" ]; then
    echo "🔑 Configuring passwordless systemctl permissions for installed services..."
    sudo "$SUDO_SCRIPT"
fi

echo "✅ Installation complete across all detected packages!"
