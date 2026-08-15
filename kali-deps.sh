sudo apt update

sudo apt install qtile python3-xcffib python3-cairocffi python3-setuptools rofi

pip3 install --break-system-packages --user qtile-extras dbus-fast

#install tools for audio and brightness
sudo apt install wireplumber pipewire-audio brightnessctl pipewire-alsa pipewire-pulse

mkdir -p ~/.config/wireplumber 2>/dev/null
cp -r /usr/share/wireplumber/* ~/.config/wireplumber/
rm -rf ~/.local/state/wireplumber/

systemctl --user daemon-reload

systemctl --user --now enable pipewire wireplumber
systemctl --user restart pipewire pipewire-pulse wireplumber



