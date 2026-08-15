# Qtile Desktop Configuration

A modular, portable Qtile desktop setup configured for multi-distro compatibility across Lubuntu, Xubuntu, Kali Linux, and DietPi (ARM64 / Orange Pi 5 Plus). 

It features custom Rofi control menus, a Game Mode background service toggle, dynamic sound and brightness notifications, and automated permission setup scripts.

> ⚠️ **Work in Progress:** This setup is actively being developed. Scripts, keybindings, and configurations will be added and updated as needed.

---

## 🛠️ Features

* **Rofi Service Manager (`devsrv.sh` & `devsrv.rasi`):** Toggle developer and background services (Docker, PostgreSQL, Redis, Ollama, etc.) with a dedicated Game Mode to free up RAM and CPU.
* **Auto-Sudoers Setup (`make_sudoer.sh`):** Detects installed services on the target machine and generates passwordless `systemctl` permissions safely using `visudo`.
* **OSD Audio & Brightness Controls (`sound.sh` & `brightness.sh`):** Wrapper scripts for `wpctl` and `brightnessctl` featuring progress bars and stack-tagging for clean notifications.
* **Custom Rofi Launchers:** Styled theme files for application launching, power management, developer services, and SSH sessions (`appimage.rasi`, `apps.rasi`, `devsrv.rasi`, `power.rasi`, `ssh.rasi`).
* **Cross-Distro Support:** Configured to run across Ubuntu/Debian bases, Kali Linux, and lightweight LXQt/DietPi nodes.

---

## 📂 Repository Structure

```text
~/.config/qtile/
├── config.py         # Main Qtile configuration file
├── autostart.sh      # Startup commands and background daemons
├── make_sudoer.sh    # Sudoers generator for service toggles
├── devsrv.sh         # Rofi Service Manager / Game Mode script
├── devsrv.rasi       # Service Manager Rofi theme
├── sound.sh          # PipeWire volume notification handler
├── brightness.sh     # Backlight notification handler
├── appimage.sh       # AppImage launcher wrapper
├── powermenu.sh      # System shutdown/reboot menu
├── sysinfo.sh        # Quick system information utility
├── kali-deps.sh      # Dependency setup script
├── *.rasi            # Rofi layout and color theme files
└── wp/               # Wallpapers and menu header image assets
```

## 🚀 Installation & Setup

### 1. Clone the Repository
  
  Clone this repository directly into your user config directory:
  
```bash
git clone git@github.com:holz-one/qtile-desktop.git ~/.config/qtile
```

Or via HTTPS:

```bash
git clone https://github.com/holz-one/qtile-desktop.git ~/.config/qtile
```

### 2. Make Scripts Executable & Install Dependencies

   Navigate into your directory, make all shell scripts executable, and run the dependency installer:

```bash
cd ~/.config/qtile
chmod +x *.sh
./install-deps.sh
```

### 3. Generate Service Permissions

   Allow devsrv.sh to start and stop services without password prompts:

```bash
sudo ./make_sudoer.sh
```

### ⌨️ Useful Keybindings

| Keybinding | Action | Description |
| :--- | :--- | :--- |
| `XF86AudioRaiseVolume` | `./sound.sh up` | Raises volume (+5%) with OSD |
| `XF86AudioLowerVolume` | `./sound.sh down` | Lowers volume (-5%) with OSD |
| `XF86AudioMute` | `./sound.sh mute` | Toggles audio mute |
| `XF86AudioMicMute` | `./sound.sh mic-mute` | Toggles microphone mute |
| `XF86MonBrightnessUp` | `./brightness.sh up` | Increases backlight (+5%) |
| `XF86MonBrightnessDown` | `./brightness.sh down` | Decreases backlight (-5%) |

More will eventually be added from my other systems.

## 📝 License
Distributed under the MIT License. See LICENSE for details.
