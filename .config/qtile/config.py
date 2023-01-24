from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess

mod = "mod4"
terminal = "alacritty"
browser = "firefox-developer-edition"


if qtile.core.name == "x11":
    launcher = "rofi -combi-modi window,drun,ssh -theme solarized -font \"hack 10\" -show combi"
    # Autostart when qtile launches
    @hook.subscribe.startup_once
    def autostart():
        home = os.path.expanduser('~/.config/qtile/autostart-x11.sh')
        subprocess.Popen([home])
elif qtile.core.name == "wayland":
    launcher = "fuzzel --width 50 --no-icons"
    # Autostart when qtile launches
    @hook.subscribe.startup_once
    def autostart():
        home = os.path.expanduser('~/.config/qtile/autostart-wayland.sh')
        subprocess.Popen([home])


keys = [

    # Switch things
    Key([mod], "Left", lazy.layout.left(),desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(),desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(),desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(),desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),desc="Move window focus to other window"),
    Key([mod], "period", lazy.next_screen(), desc="Move focus to other screen"),

    # Move things
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(),desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(),desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(),desc="Move window up"),

    # Grow things
    Key([mod, "control"], "Left", lazy.layout.grow_left(),desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(),desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Launch things
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "d", lazy.spawn(launcher), desc="Launch application launcher"),

    # Toggle things
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating mode"),

    # Kill things
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Reload things
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),

    # Spawn things
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # XF86 things
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10"), desc="Turn the brightness up"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10-"), desc="Turn the brightness up"),
    # Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    # Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")),
    # Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute"))
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_defaults = {
    "border_focus": "#000000",
    "border_normal": "#000000",
    "border_width": 1.5,
    "margin": 8,
    "border_on_single": True
}

layouts = [
    layout.MonadTall(**layout_defaults),
    layout.Columns(**layout_defaults),
    layout.Max(**layout_defaults),
    layout.Floating(**layout_defaults)
]

widget_defaults = {
    "font": "Lexend Bold",
    "fontshadow":"000000",
    "fontsize": 13,
    "padding": 3
}
extension_defaults = widget_defaults.copy()

separator_defaults = {
    "linewidth": 1,
    "size_percent": 50,
    "padding": 20
}

groupbox_defaults = {
    "highlight_method":"line",
    "borderwidth":5,
    "highlight_color":['00000000', '87CEEB'],
    "this_current_screen_border":'87CEEB',
    "this_screen_border":'4682B4',
    "other_current_screen_border":'87CEEB',
    "other_screen_border":'676767',
    "padding_x":7,
    "margin_x":1
}

clock_defaults = {
    "format":"%Y-%m-%d %a %H:%M:%S"
}

# Wallpaper defaults (applied to every desktop)
wallpaper_default = 'Wallpaper/13.jpg'
wallpaper_mode_defalt = 'stretch'


screens = [
    Screen(
        wallpaper=wallpaper_default,
        wallpaper_mode=wallpaper_mode_defalt,
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    **groupbox_defaults
                ),
                widget.Spacer(
                    length=50
                ),
                widget.Prompt(
                    prompt="[benv@archlinux ~]$ ",
                    font="Hack Bold",
                    cursorblink=0.3
                ),
                widget.Spacer(),
                widget.PulseVolume(
                    fmt="VOL:{}"
                ),
                widget.Sep(
                    **separator_defaults
                ),
                widget.Wlan(
                    format="NET: {essid} ({percent:2.0%})"
                ),
                widget.Net(
                    format="{down} ↓↑ {up}",
                    prefix="M"
                ),
                widget.Sep(
                    **separator_defaults
                ),
                widget.Battery(
                    format="BATTERY: {percent:2.0%} ({hour:d}:{min:02d})"
                ),
                widget.Sep(
                    **separator_defaults
                ),
                widget.Clock(
                    **clock_defaults
                ),
                widget.Sep(
                    **separator_defaults
                ),
                widget.CurrentLayoutIcon(
                    scale=0.5
                )
            ],
            30,
            background=["00000000","000000"]
        )
    ),
    Screen(
        wallpaper=wallpaper_default,
        wallpaper_mode=wallpaper_mode_defalt,
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    **groupbox_defaults
                ),
                widget.Spacer(),
                widget.Clock(
                    **clock_defaults
                ),
                widget.Sep(
                    **separator_defaults
                ),
                widget.CurrentLayoutIcon(
                    scale=0.5
                )
            ],
            30,
            background=["00000000","000000"]
            )
    ),
    Screen(
        wallpaper=wallpaper_default,
        wallpaper_mode=wallpaper_mode_defalt,
        bottom=bar.Bar(
            [
                widget.GroupBox(
                    **groupbox_defaults
                ),
                widget.Spacer(),
                widget.Clock(
                    **clock_defaults
                ),
                widget.Sep(
                    **separator_defaults
                ),
                widget.CurrentLayoutIcon(
                    scale=0.5
                )
            ],
            30,
            background=["00000000","000000"])
    )
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
