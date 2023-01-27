#!/bin/sh

xrandr --output eDP-1 --scale 0.5x0.5 &
xset s off -dpms &
nm-applet --indicator &
pa-applet &
picom &
lxsession &
