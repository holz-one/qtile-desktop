# qtile-desktop
![Qtile-Desktop](./wp/bg.jpeg)


My personal Qtile window manager configuration. This repository contains my complete desktop environment setup, optimized for efficiency with custom scripting and modular configurations.

---

## Recent Updates

* **Keyboard Function Keys:** Updated media, audio, and backlight function keys to interact with hardware scripts and system utilities.
* **Script Restructuring:** Moved all non-Rofi system and utility shell scripts into `./bin/` to clean up the root directory.
* **Expanded Rofi Scripts:** Added several new Rofi menu scripts directly in the root directory alongside `.rasi` theme files.
* **Rofi Keybindings:** Mapped Rofi scripts directly to Qtile shortcuts for quick access.

---

## Directory Overview

```text
├── config.py    # Core Qtile configuration & keybindings
├── bin/         # Non-rofi executable scripts 
├── wp/          # AI generated images used in Rofi launchers
├── system-conf/ # Configs to install into /etc 
├── *.sh         # Rofi menu scripts
├── *.rasi       # Rofi theme files
├── README.md    # Repository documentation
└── LICENSE      # MIT Licence 
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
The script will also install most dependancies of programs I use and it will also configure git, zsh, vu.  
I intend to add more to this install script. 
Ollama still needs to be added, maybe llama.cpp. 

I also plan to make a tool to replace snap with flatpak, 
my current system has snap removed completlety.


### 3. Generate Service Permissions

Allow devsrv.sh to start and stop services without password prompts.
Other apps will also be added as needed for other commands like freashclam, rkhunter, gparted, apt update/upgrade, ss, 


```bash
sudo ./make_sudoer.sh
```

### 4. Useful Keybindings

These are all key bindings from all my avalible keyboards I have from:

- MacBook Mid-2012
- MSI Katana
- SEMICO USB Keyboard ($5 Dollarama Specal)
- Microsoft Nano Transceiver v2.0

The keys I haven't configured yet are commented out in the `config.py`

| Keybinding | Action | Description |
| :--- | :--- | :--- |
| **XF86AudioRaiseVolume** | `./bin/volume.sh up` | Raise audio volume |
| **XF86AudioLowerVolume** | `./bin/volume.sh down` | Lower audio volume |
| **XF86AudioMute** | `./bin/volume.sh mute` | Toggle audio mute |
| **XF86AudioMicMute** | `./bin/sound.sh mic-mute` | Toggles microphone mute |
| **XF86MonBrightnessUp** | `./bin/brightness.sh up` | Increases backlight (+5%) |
| **XF86MonBrightnessDown** | `./bin/brightness.sh down` | Decreases backlight (-5%) |
| **XF86KbdBrightnessUp** | `./bin/brightness.sh macup` | Increases backlight (+5%) |
| **XF86KbdBrightnessDown** | `./bin/brightness.sh macdown` | Decreases backlight (-5%) |
| **XF86AudioPlay** | `playerctl play-pause` | Play / Pause active media |
| **XF86AudioNext** | `playerctl next` | Skip to next track |
| **XF86AudioPrev** | `playerctl previous` | Skip to previous track |
| **XF86Eject** | `./powermenu.sh` | Power Menu |
| **XF86LaunchA** | Next Layout | Switch Qtile Layout |
| **XF86LaunchB** | `./rofi_apps.sh` | Launcher of configured Rofi Scripts |
| **XF86HomePage** | `firefox` | Firefox Web Browser |
| **XF86Tools** | `vlc` | VLC Media Player |
| **XF86Explorer** | `./bin/files.sh` | File Browser |
| **XF86Search** | `catfish` | Cat Fish Search tool |
| **XF86Mail** | `thunderbird` | Thunderbird Mail Client |

More will eventually be added from my other systems as they're configured.


#### Other Keyboard Script Keybindings

Below are the key combinations configured in `config.py` to launch Rofi scripts and other Apps:

| Keybinding | Target Script / Action | Description |
| :--- | :--- | :--- |
| `Super + D` | `rofi -show drun` | Rofi Application launcher |
| `Super + Shift + D` | `./docker.sh` | Docker Containers |
| `Super + Control + D` | `./devsrv.sh` | Services and Game Mode |
| `Super + Alt + D` | `./appimage.sh` | AppImage launcher |
| `Super + S` | `./ssh.sh` | Rofi SSH |
| `Super + Shift + S` | `./scanner-avm.sh` | ClamAV/RKHunter launcher |
| `Super + O` | `./ollama.sh` | Rofi Ollama |
| `Super + P` | `arandr` | Display Config |
| `Super + Enter` | `kitty` | kitty terminal |
| `Super + F21` | `./bin/settings.sh` | launch settings app |


## Images

All the images in ./wp have been generated with Google Gemini for rofi menus and wallpaper.  
It has improved a lot compaired to CoPilot or ChatGPT.
 
## 📝 License
Distributed under the MIT License. See LICENSE for details.
