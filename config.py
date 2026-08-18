import os
import subprocess  
import libqtile.resources
from libqtile import layout, qtile, hook 
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# --- WIDGET & BAR EXTENSIONS ---
from libqtile.bar import Bar  
from qtile_extras import widget  
from qtile_extras.widget.decorations import PowerLineDecoration

##
from libqtile.config import ScratchPad, DropDown
##

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        # Float any window given the class 'scanner-float'
        Match(wm_class="scanner-float"),
    ]
)

@hook.subscribe.client_name_updated
def force_floating_by_title(window):
    if window.name == "Floating Terminal" or window.name == "Volume Control":
        window.floating = True
        # 2. Define your desired size (Width, Height) in pixels
        width = 800
        height = 600
        
        # 3. Fetch your current monitor dimensions dynamically
        screen = window.qtile.current_screen
        
        # 4. Calculate coordinates to perfectly center the window
        x = screen.x + (screen.width - width) // 2
        y = screen.y + (screen.height - height) // 2
        
        # 5. Apply the dimensions and location
        window.place(x, y, width, height, 0, None)


mod = "mod4"
alt = "mod1"  # Alt key
terminal = "kitty"
##############
# Rofi menu  #
# ============
APPS = "rofi -show drun -theme ~/.config/qtile/apps.rasi"
DOCKER = os.path.expanduser("~/.config/qtile/docker.sh")
DEVSRV = os.path.expanduser("~/.config/qtile/devsrv.sh")
SSH = "rofi -show ssh -theme ~/.config/qtile/ssh.rasi -terminal kitty"
CLAMAV = os.path.expanduser("~/.config/qtile/scanner-avm.sh")
APPIMAGE = os.path.expanduser("~/.config/qtile/appimage.sh")
OLLAMA = os.path.expanduser("~/.config/qtile/ollama-ai.sh")
POWER = os.path.expanduser("~/.config/qtile/powermenu.sh")

ROFI_APPS = os.path.expanduser("~/.config/qtile/rofi_apps.sh")

####################
# Scripts launcher #
# ==================
SETTINGS = os.path.expanduser("~/.config/qtile/bin/settings.sh")
FILES =  os.path.expanduser("~/.config/qtile/bin/files.sh")
SOUND = os.path.expanduser("~/.config/qtile/bin/sound.sh")
BRIGHT = os.path.expanduser("~/.config/qtile/bin/brightness.sh")
SYSINFO = "kitty -T 'Floating Terminal' -e .config/qtile/bin/sysinfo.sh"
HTOP = "kitty -T 'Floating Terminal' -e htop"
####################
keys = [
    # ===============================================================
    # ROFI MODE LAUNCHERS
    # ===============================================================
    # Current Default: Mod + d -> Standard Desktop App Launcher
    # f10/box with arrow pointing to right bottom
    #       on Microsoft Microsoft® Nano Transceiver v2.0 
    # ===============================================================
    Key([mod], "d", lazy.spawn(APPS), desc="Rofi Desktop Apps"),
    # ===============================================================
    # d based keys
    # mod + shift + d -> Docker containers
    Key([mod, "shift"], "d", lazy.spawn(DOCKER), 
        desc="Launch Rofi Docker Manager"),
    # Mod + control + d  -> Instantly launch service toggle
    Key([mod, "control"], "d", lazy.spawn(DEVSRV), 
        desc="Rofi Service Launcher"),
    # Mod + Alt +d -> Instantly launch the custom AppImage Launcher
    Key([mod, alt], "d", lazy.spawn(APPIMAGE), 
        desc="Rofi AppImage Launcher"),
    # ==============================================================
    # s bases kays
    # Mod + s -> SSH Session Launcher
    Key([mod], "s", lazy.spawn(SSH), desc="Rofi SSH Launcher"),
    # Mod + Shift + s
    Key([mod, "shift"], "s", lazy.spawn(CLAMAV), 
        desc="Run Rofi Malware Scanner"),

    # ==============================================================
    # Mod + o -> launch selected Ollama Model
    Key([mod], "o", lazy.spawn(OLLAMA), 
        desc="Rofi Ollama AI Launcher"),
    # =============================================================
    # Projector / Display Key: 
    # MSI Katana projector shortcut is just a <win>+p on one button
    # f9/2 sceen icon on Microsoft Microsoft® Nano Transceiver v2.0
    # =============================================================
    Key([mod], "p", lazy.spawn("arandr"), 
        desc="arandr"),
    # ===========================================================
    # Quit
    Key([mod, "shift"], "q", lazy.window.kill(), 
        desc="kill focused window"),
    # ==========================================================
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), 
        desc="toggle tiling / floating"),
    Key([mod], "space", lazy.layout.next(), 
        desc="Move window focus to other window"),
    # ===========================================================
    # Window focus keys
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), 
        desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    # ===========================================================
    # Shuffling Windows
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    # ==========================================================
    # Window Resizing
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    # =========================================================
    # Change Layout
    Key([mod], "Tab", lazy.next_layout()),
    # =========================================================
    # Full Screen
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    # =========================================================
    # Reload Qtile Config
    Key([mod, "control"], "r", lazy.reload_config()),
    # =========================================================
    # terminal
    Key([mod], "Return", lazy.spawn(terminal), 
        desc="Launch terminal"),
    # =========================================================
    # scratchpad
    Key([mod], "Backspace", 
        lazy.group["scratchpad"].dropdown_toggle("term"), 
        desc="Toggle scratchpad terminal"),
    # ===============================================================
    # HARDWARE MEDIA & VOLUME KEYS
    # ===============================================================
    # Volume Up: Raises audio by 5% (Clamped at 100% max)
    Key([], "XF86AudioRaiseVolume", lazy.spawn(SOUND + " up"), 
        desc="Raise Volume"),
    # Volume Down: Lowers audio by 5%
    Key([], "XF86AudioLowerVolume", lazy.spawn(SOUND + " down"), 
        desc="Lower Volume"),
    # Audio Mute: Toggles system mute state on/off
    Key([], "XF86AudioMute", lazy.spawn(SOUND + " mute"), 
        desc="Toggle Mute"),
    # Microphone Mute: Toggles system input source on/off
    Key([], "XF86AudioMicMute", lazy.spawn(SOUND + " mic-mute"), 
        desc="Toggle Microphone Mute"),
    # ===============================================================
    # BACKLIGHT / BRIGHTNESS CONTROL KEYS
    # ===============================================================
    # Brightness Up: Increases backlight by 5%
    Key([], "XF86MonBrightnessUp", lazy.spawn(BRIGHT + " up"), 
        desc="Increase Screen Brightness"),
    # Brightness Down: Decreases backlight by 5% 
    Key([], "XF86MonBrightnessDown", lazy.spawn(BRIGHT + " down"), 
        desc="Decrease Screen Brightness"),
    # =============================================================
    # KEYBOARD BACKLIGHT CONTROLS
    # =============================================================
    # Lower Keyboard Backlight
    Key([], "XF86KbdBrightnessDown", lazy.spawn(BRIGHT + " macdown"),
        desc="Lower Keyboard Backlight"),
    # Raise Keyboard Backlight
    Key([], "XF86KbdBrightnessUp", lazy.spawn(BRIGHT + " macup"),
        desc="Raise Keyboard Backlight"),
    # =============================================================
    # MEDIA PLAYBACK CONTROLS (PLAYERCTL)
    # =============================================================
    # Play/Pause
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), 
        desc="Play/Pause Media"),
    # Next Track
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), 
        desc="Next Track"),
    # Previous Track
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), 
        desc="Previous Track"),
    # =============================================================
    # MacBook Mid-2012 - Fn keys
    # =============================================================
    # XF86Eject (MacBook Mid-2012 eject button
    Key([], "XF86Eject", lazy.spawn(POWER)),
    # XF86LaunchA (MacBook Mid-2012) 
    Key([], "XF86LaunchA", lazy.next_layout()),
    # XF86LaunchB (MacBook Mid-2012)
    Key([], "XF86LaunchB", lazy.spawn(ROFI_APPS)),

    # ============================================================
    #  Microsoft Microsoft® Nano Transceiver v2.0
    # ============================================================
    #  - Above Trackpad
    # ============================================================
    # House Icon  
    # - fn + f1 on SEMICO USB Keyboard
    Key([], "XF86HomePage", lazy.spawn("firefox"), 
        desc="Launch Firefox"),
    # Media Player headphones 
    # - fn + f4 on SEMICO USB Keyboard
    Key([], "XF86Tools", lazy.spawn("vlc"), 
        desc="Launch VLC"),
    # Folder icon 
    # - fn + f11 on SEMICO USB Keyboard
    Key([], "XF86Explorer", lazy.spawn(FILES), 
        desc="Launch File Manager"),
    # ===========================================================
    #  Fn keys on F keys
    # ===========================================================
    # f5/ Search icon 
    # - fn + f3 on SEMICO USB Keyboard
    Key([], "XF86Search", lazy.spawn("catfish"), 
        desc="Cat Fish search tool"), 
    # f6/Ubuntu Logo 
    #Key([alt, mod], "F21", lazy.spawn( ), desc=""),
    # f7/small squre over a big square
    #Key(["control", mod], "F21", lazy.spawn()),
    
    # f8/Settings, gear on Microsoft Microsoft® Nano Transceiver v2.0 
    Key([mod], "F21", lazy.spawn(SETTINGS), 
        desc="XFCE4/LXQt Settings"),
    # ==========================================================
    # SEMICO USB Keyboard Consumer Control (from Dollarama)
    # ==========================================================
    # fn + f2 - mail
    Key([], "XF86Mail", lazy.spawn("thunderbird")),
    # fn + f12 calculator
    #Key([], "XF86Calculator", lazy.spawn("galculator")),

    # ===============================================================
    # Compose Key, looks like a menu
    # If Multi_key doesn't catch it, use Menu as your backup fallback
    # - Try Multi_key 1st (the most standard X11 mapping for Compose)
    #Key([], "Multi_key", lazy.spawn("your-command-here")),
    #Key([], "Menu", lazy.spawn("your-command-here")),

    #===============================================================
    # Print Screen key to take a screenshot
    #Key([], "Print", lazy.spawn("")),

    # =============================================================
    #  Pause/Break key to a custom command (e.g., locking your screen)
    #Key([], "Pause", lazy.spawn("")),
]

# ===================================================================
# WORKSPACE GROUPS & AUTOMATIC APP ROUTING
# ===================================================================
# ===================================================================
# WORKSPACE GROUPS (CUSTOM LABELS & AUTOMATIC APP ROUTING)
# ===================================================================

# Internal Name (for code/hotkeys) : Visual Label (what displays on the bar)
GROUP_NAMES = {
    "1": "🥷1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "🌐",
    "9": "🥷",
}

groups = [
    # General Workspaces with Custom Labels
    Group("1", label=GROUP_NAMES["1"]),
    Group("2", label=GROUP_NAMES["2"]),
    Group("3", label=GROUP_NAMES["3"]),
    Group("4", label=GROUP_NAMES["4"]),
    #Group("5", label=GROUP_NAMES["5"]),
    #Group("6", label=GROUP_NAMES["6"]),
    #Group("7", label=GROUP_NAMES["7"]),
    
    # Group 8: Web Browser Workspace (Forces Firefox here)
    Group(
        "8", 
        label=GROUP_NAMES["8"],
        matches=[Match(wm_class="firefox")],
    ),
    
    # Group 9: Code Development Workspace (Forces VS Code here)
    Group(
        "9", 
        label=GROUP_NAMES["9"],
        matches=[Match(wm_class="code")],
    ),
]


# ===================================================================
# ADDING THE KITTY SCRATCHPAD
# ===================================================================
groups.append(
    ScratchPad("scratchpad", [
        DropDown(
            "term",
            # Forces a unique window class for the dropdown
            f"kitty --class=scratchpad", 
            opacity=0.95,
            # Spans 60% of screen height
            height=0.6,                  
            # Spans 80% of screen width
            width=0.8,      
            # Centers it horizontally (10% margin left)
            x=0.1,                       
            # Centers it vertically (10% margin top)
            y=0.1,                       
            # Automatically hides when you click away
            on_focus_lost_hide=True      
        ),


    ])
)
#########################################
for i in groups:
    if i.name.isdigit():
        keys.extend([
            Key([mod], i.name, lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}"),
            Key([mod, "shift"], i.name, 
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Move focused window to group {i.name}"),
        ])

# ===================================================================
# RED, WHITE & BLACK COLOR PALETTE
# ===================================================================

COLORS = {
    # Pure Black (Bar & Outer space)
    "bg_dark":    "#000000", 
    # Dark Charcoal / Matte Black (Bar Segments)
    "panel_dark": "#121212", 
    # Medium Charcoal (Contrasting Segments)
    "panel_mid":    "#242424", 
    # Vibrant Crimson / Neon Red (Highlights & Clock)
    "accent_red":   "#FF0033", 
    # Pure Red (Active Window Borders)
    "border_red":   "#E60000", 
    # Crisp White (Primary text & icons)
    "text_white":   "#FFFFFF", 
    # Dimmed Gray (Inactive workspace icons)
    "text_dim":     "#888888", 
}

katana_slash = {
    "decorations": [
        PowerLineDecoration(
            path="forward_slash", 
            size=11,             
            shift=0,
        )
    ]
}

widget_defaults = dict(
    font="JetBrains Mono, sans-serif",
    fontsize=13,
    padding=6,
    foreground=COLORS["text_white"],
)
extension_defaults = widget_defaults.copy()

# ===================================================================
# LAYOUT BORDERS
# ===================================================================
# Shared border theme settings so every layout looks consistent
layout_theme = {
    "border_width": 2,
    # Outer gaps around windows
    "margin": 8,                         
    # Active window border
    "border_focus": COLORS["border_red"], 
    # Inactive window border
    "border_normal": COLORS["panel_dark"]
}

layouts = [
    # 1. COLUMNS (Your main tiling driver
    # - flexible left/right split)
    layout.Columns(
        **layout_theme,
        border_focus_stack=COLORS["border_red"],
        border_normal_stack=COLORS["panel_dark"],
        num_columns=2,
        insert_position=1
    ),

    # 2. MONADTALL (Classic i3/XMonad layout
    # - 1 large master on left, stack on right)
    layout.MonadTall(
        **layout_theme,
        # Master window takes 55% of screen width
        ratio=0.55,                      
        new_client_position='after_current'
    ),

    # 3. MONADWIDE (Same as MonadTall, but split horizontally
    # - great for ultra-wides)
    layout.MonadWide(
        **layout_theme,
        # Master window takes 60% of screen height
        ratio=0.60,                      
    ),

    # 4. BSPACE (Binary Space Partitioning
    # - automatically splits active pane)
    layout.Bsp(
        **layout_theme,
        # Keeps window sizes balanced automatically
        fair=False,                      
    ),

    # 5. MATRIX (Grid-based layout
    # - arranges windows evenly in a grid)
    layout.Matrix(
        **layout_theme,
        # Start as a 2-column matrix grid
        columns=2                        
    ),

    # 6. ZOOMY (Focus mode
    # - active window is huge, background apps form a side strip)
    layout.Zoomy(
        **layout_theme,
        # Width of the inactive window sidebar 
        column_width=200                 
    ),

    # 7. MAX (Full screen workspace layout)
    layout.Max(),
]


# ===================================================================
# SCREEN CONFIGURATION
# ===================================================================

screens = [
    Screen(
        top=Bar(  
            [
                # Left Side: Workspaces / Current Status
                widget.CurrentLayoutIcon(
                    background=COLORS["accent_red"],
                    scale=0.65,
                    use_mask=True,
                    foreground=COLORS["bg_dark"],
                    **katana_slash
                ),
                widget.GroupBox(
                    background=COLORS["panel_dark"],
                    active=COLORS["accent_red"],
                    inactive=COLORS["text_dim"],
                    this_current_screen_border=COLORS["accent_red"],
                    highlight_method="text",
                    padding_x=6,
                    **katana_slash
                ),
                widget.WindowName(
                    background=COLORS["panel_mid"],
                    foreground=COLORS["text_white"],
                    max_chars=40,
                ),
                
                widget.Spacer(
                    background=COLORS["panel_mid"],
                    **katana_slash
                ),

                # Network Monitor
                widget.Net(
                    format="󰀂 󰇚{down:6.2f} 󰕒{up:6.2f}",
                    background=COLORS["accent_red"],
                    foreground=COLORS["text_white"],
                    **katana_slash
                ),

                # CPU Usage
                widget.CPU(
                    format="󰍛 {load_percent}%",
                    background=COLORS["panel_dark"],
                    foreground=COLORS["text_white"],
                    mouse_callbacks={
                        'Button1': lazy.spawn(SYSINFO) 
                    },
                    **katana_slash
                ),

                # Thermal Sensor
                widget.ThermalSensor(
                    format="🔥 {temp}°C",
                    background=COLORS["accent_red"],
                    foreground=COLORS["text_white"],
                    foreground_alert=COLORS["accent_red"],
                    threshold=75,
                    **katana_slash
                ),

                # RAM Usage
                widget.Memory(
                    format="󰘚 {MemUsed: .1f}M",
                    background=COLORS["panel_dark"],
                    foreground=COLORS["text_white"],
                    mouse_callbacks={
                        'Button1': lazy.spawn(HTOP),
                       
                    },
                    **katana_slash
                ),

                # Volume Widget
                widget.Volume(
                    fmt="🔊 {}",
                    background=COLORS["accent_red"],
                    foreground=COLORS["text_white"],
                    mouse_callbacks={
                        'Button1': lazy.spawn('pavucontrol'),
                        'Button3': lazy.spawn('systemctl --user restart pipewire pipewire-pulse wireplumber')
                    },
                    **katana_slash
                ),
                widget.Battery(
                    format="{char} {percent:2.0%}",
                    charge_char="⚡",
                    discharge_char="🔋",
                    full_char="🔋",
                    empty_char="🪫",
                    unknown_char="🔌",
    
                    # Threshold warning colors
                    # Trigger low alert at 20%
                    low_percentage=0.2,                  
                    # Color when battery is low
                    low_foreground=COLORS["panel_dark"],  
                    # Normal text color
                    foreground=COLORS["text_white"],     
                    # Update frequency (in seconds)
                    update_interval=10,
                    # Apply your bar's background/separator style
                    **katana_slash  
                ),
                # Clock Block (Bold Accent)
                widget.Clock(
                    format="%Y-%m-%d %H:%M",
                    background=COLORS["accent_red"],
                    foreground=COLORS["text_white"],
                    padding=10,
                    **katana_slash
                ),
                widget.Chord(
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(
                    padding=5,
                    **katana_slash
                ),
                widget.TextBox(
                    text="󰐥",
                    background=COLORS["accent_red"],
                    foreground=COLORS["text_white"],
                    padding=10,
                    mouse_callbacks={
                        'Button1': lazy.spawn(POWER)
                    }
                ),
            ],
            26,  
            background=COLORS["bg_dark"],
            opacity=1.0,
            margin=[0, 0, 0, 0], 
        ),
    ),
]

# Update Floating Layout colors as well
floating_layout = layout.Floating(
    border_focus=COLORS["accent_red"],
    border_normal=COLORS["panel_dark"],
    border_width=3,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  
        Match(wm_class="makebranch"),  
        Match(wm_class="maketag"),  
        Match(wm_class="ssh-askpass"),  
        Match(title="branchdialog"),  
        Match(title="pinentry"),  
    ]
)
# =============================================================================
# MOUSE & WINDOW RULES,
# =============================================================================

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules: list = []  
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"

# =================================================================
# STARTUP HOOKS
# =================================================================

@hook.subscribe.startup_once
def autostart():
    #subprocess.Popen(['nm-applet'])
    #initial_wp = os.path.expanduser("~/.config/qtile/wp/bg.png")
    home = os.path.expanduser('~/.config/qtile/bin/autostart.sh')
    subprocess.Popen([home])
    #if os.path.exists(initial_wp):
    #    subprocess.Popen(["feh", "--bg-fill", initial_wp])
