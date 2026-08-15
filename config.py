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
terminal = "kitty"

keys = [
    # --- Core i3 Keybindings Translated to Qtile ---
    Key([mod, "shift"], "q", lazy.window.kill(), desc="kill focused window"),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc="toggle tiling / floating"),
    # Navigation
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    
    # Shuffling Windows
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),

    # Window Resizing
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # Standard Shortcuts
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "control"], "r", lazy.reload_config()),
    # terminal
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # scratchpad
    Key([mod], "Backspace", lazy.group["scratchpad"].dropdown_toggle("term"), desc="Toggle scratchpad terminal"),

    # ===============================================================
    # ROFI MODE LAUNCHERS
    # ===============================================================
# d
    # Current Default: Mod + d -> Standard Desktop App Launcher
    Key([mod], "d", lazy.spawn("rofi -show drun -theme ~/.config/qtile/apps.rasi"), desc="Rofi Desktop Apps"),

    # Mod + Shift + d -> SSH Session Launcher
    Key([mod, "shift"], "d", lazy.spawn("rofi -show ssh -theme ~/.config/qtile/ssh.rasi -terminal kitty"), desc="Rofi SSH Launcher"),

#a
    # Mod + a -> Instantly launch the custom AppImage Game Launcher
    Key([mod], "a", lazy.spawn(os.path.expanduser("~/.config/qtile/appimage.sh")), 
        desc="Rofi AppImage Launcher"),
#g
    # Mod + g -> Instantly launch service toggle
    Key([mod], "g", lazy.spawn(os.path.expanduser("~/.config/qtile/devsrv.sh")), 
        desc="Rofi Service Launcher"),
    # more to come, just need to make a script


    # ===============================================================
    # HARDWARE MEDIA & VOLUME KEYS
    # ===============================================================

    # Volume Up: Raises audio by 5% (Clamped at 100% max)
    Key([], "XF86AudioRaiseVolume", lazy.spawn(os.path.expanduser("~/.config/qtile/sound.sh up")), desc="Raise Volume"),

    # Volume Down: Lowers audio by 5%
    Key([], "XF86AudioLowerVolume", lazy.spawn(os.path.expanduser("~/.config/qtile/sound.sh down")), desc="Lower Volume"),

    # Audio Mute: Toggles system mute state on/off
    Key([], "XF86AudioMute", lazy.spawn(os.path.expanduser("~/.config/qtile/sound.sh mute")), desc="Toggle Mute"),

    # Microphone Mute: Toggles system input source on/off
    Key([], "XF86AudioMicMute", lazy.spawn(os.path.expanduser("~/.config/qtile/sound.sh mic-mute")), desc="Toggle Microphone Mute"),

    # ===============================================================
    # BACKLIGHT / BRIGHTNESS CONTROL KEYS
    # ===============================================================
    
    # Brightness Up: Increases backlight by 5%
    Key([], "XF86MonBrightnessUp", lazy.spawn(os.path.expanduser("~/.config/qtile/brightness.sh up")), desc="Increase Screen Brightness"),

    # Brightness Down: Decreases backlight by 5% (Automatically stops at 1% min)
    Key([], "XF86MonBrightnessDown", lazy.spawn(os.path.expanduser("~/.config/qtile/brightness.sh down")), desc="Decrease Screen Brightness"),

    # Projector / Display Key: Launches an interactive Rofi multi-display menu
    # MSI Katana projector shortcut is just a <win>+p on one button
    Key([mod], "p", lazy.spawn("arandr"), desc="Interactive Rofi Monitor Layout Switcher"),
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
        layout="max"
    ),
    
    # Group 9: Code Development Workspace (Forces VS Code here)
    Group(
        "9", 
        label=GROUP_NAMES["9"],
        matches=[Match(wm_class="code")],
        layout="columns"
    ),
]


# ===================================================================
# ADDING THE KITTY SCRATCHPAD
# ===================================================================
groups.append(
    ScratchPad("scratchpad", [
        DropDown(
            "term",
            f"kitty --class=scratchpad", # Forces a unique window class for the dropdown
            opacity=0.95,
            height=0.6,                       # Spans 60% of screen height
            width=0.8,                        # Spans 80% of screen width
            x=0.1,                            # Centers it horizontally (10% margin left)
            y=0.1,                            # Centers it vertically (10% margin top)
            on_focus_lost_hide=True           # Automatically hides when you click away
        ),


    ])
)
#########################################
for i in groups:
    if i.name.isdigit():
        keys.extend([
            Key([mod], i.name, lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}"),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
                desc=f"Move focused window to group {i.name}"),
        ])

layouts = [
    layout.Columns(
        border_focus="#ff5555",      # Blood Red border for the active window
        border_normal="#282a36",     # Dark Steel border for inactive windows
        border_width=5,
        margin=10                     # Adds a clean gap between windows
    ),
    layout.Max(),
]

# ===================================================================
# RED, WHITE & BLACK COLOR PALETTE
# ===================================================================

COLORS = {
    "bg_dark":      "#000000", # Pure Black (Bar & Outer space)
    "panel_dark":   "#121212", # Dark Charcoal / Matte Black (Bar Segments)
    "panel_mid":    "#242424", # Medium Charcoal (Contrasting Segments)
    "accent_red":   "#FF0033", # Vibrant Crimson / Neon Red (Highlights & Clock)
    "border_red":   "#E60000", # Pure Red (Active Window Borders)
    "text_white":   "#FFFFFF", # Crisp White (Primary text & icons)
    "text_dim":     "#888888", # Dimmed Gray (Inactive workspace icons)
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

layouts = [
    layout.Columns(
        border_focus=COLORS["border_red"],     # Vivid Red for focused window
        border_normal=COLORS["panel_mid"],     # Dark Charcoal for inactive windows
        border_width=4,
        margin=8                               # Clean gap between windows
    ),
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
                    format="󰀂  󰇚{down:6.2f} 󰕒{up:6.2f}",
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
                        'Button1': lazy.spawn("kitty -T 'Floating Terminal' -e .config/qtile/sysinfo.sh") 
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
                        'Button1': lazy.spawn("kitty -T 'Floating Terminal' -e htop"),
                       
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

                # Clock Block (Bold Accent)
                widget.Clock(
                    format="%Y-%m-%d %I:%M %p",
                    background=COLORS["panel_dark"],
                    foreground=COLORS["text_white"],
                    padding=10,
                ),
                widget.Chord(
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(padding=5),
                widget.TextBox(
                    text="󰐥 Power",
                    background=COLORS["accent_red"],
                    foreground=COLORS["text_white"],
                    padding=10,
                    mouse_callbacks={
                        'Button1': lazy.spawn(os.path.expanduser("~/.config/qtile/powermenu.sh"))
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

# =============================================================================
# STARTUP HOOKS
# =============================================================================

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(['nm-applet'])
    initial_wp = os.path.expanduser("~/.config/qtile/wp/bg.png")
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
    if os.path.exists(initial_wp):
        subprocess.Popen(["feh", "--bg-fill", initial_wp])
