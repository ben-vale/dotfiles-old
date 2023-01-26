# Arch Linux install notes

I don't like install scripts, so this goes step by step and also serves as a place to capture new packages I need. The only parts that really deviate from the Arch wiki are the packages. Some parts haven't been touched in years, especially the DE/WM stuff.

## INITIAL CONFIG

Keyboard layout and time are the only things that really need doing here, and both could be argued too.

### SET KEYBOARD

`loadkeys uk`

### CHECK UEFI

Make sure it's EFI rather than BIOS.

`ls /sys/firmware/efi/efivars`

### CHECK INTERNET

Just make sure a connection is present, I always do this wired so no need to do anything more right now.

`ip link`

`ping archlinux.org -c 1`

### SET TIME

`timedatectl set-ntp true`

`timedatectl status`

## PARTITIONS

First lookup the current setup  with **lsblk** then **cgdisk** does the heavy lifting of creating things. Format based on exactly what the Arch docs say, then mount. Size wise I'm copying what EndeavourOS does, honestly haven't put that much thought into it (though I maybe should).

`lsblk`

### Create partitions

The below implies swap but it doesn't really have to.

`cgdisk /dev/sda`

|Label|Size|Hex|
|---|---|---|
|/dev/sda1|1000MB|ef00 (EFI System)|
|/dev/sda2|20GB|8200 (Swap)|
|/dev/sda3|Remaining space|8300|

### FORMAT NEW PARTITIONS

`mkfs.fat -F32 /dev/sda1`

`mkfs.ext4 /dev/sda3`

`mkswap /dev/sda2`

`swapon /dev/sda2`

### MOUNT THE NEW PARTITIONS

`mount /dev/sda3 /mnt`

`mkdir /mnt/boot`

`mount /dev/sda1 /mnt/boot`

## UPDATE MIRROR LIST

Just reorder this so UK is up top

`nano /etc/pacman.d/mirrorlist`

## BASE INSTALL

Only including the main things needed at this stage, more packages are maybe dependent on WM/DE. There isn't really a reason I split these out.

`pacstrap -k /mnt base base-devel linux linux-firmware mesa xf86-video-nouveau network-manager git vi nano man-db man-pages texinfo`

## GENERATE FSTAB RECORDS

`genfstab -U /mnt >> /mnt/etc/fstab`

## POST INSTALL

### CHROOT INTO SYSTEM

`arch-chroot /mnt`

### TIMEZONE AND LOCALE

All of this implies it's for me and I'm in London.

`ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime`

`hwclock --systohc`

`nano /etc/locale.gen`

Uncomment 'en_GB.UTF-8' and save it.

`locale-gen`

`echo "LANG=en_GB.UTF-8" > /etc/locale.conf`

`echo "KEYMAP=uk" > /etc/vconsole.conf`

### SET HOSTNAME

Obviously replace "hostname-here" with whatever.

`echo "hostname-here" > /etc/hostname`

### SET ROOT PASSWORD

`passwd`

### CREATE YOUR USER AND SET PASSWORD

I've always included `storage` here but I don't think it's needed anymore, need to confirm.

`useradd -g users -G wheel,storage,sys,rfkill -m benv`

`passwd benv`

### INSTALL AND CONFIGURE BOOTLOADER

I know I know, I've just been too lazy to move away from GRUB.

`pacman -S grub efibootmgr`

`grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB`

`grub-mkconfig -o /boot/grub/grub.cfg`

## FIN

`exit`

`reboot`

## IMMEDIATE POST INSTALL CONFIG

### ENABLE NETWORK MANAGER

`systemctl enable --now NetworkManager`

### VISUDO

Do this bit logged in as root. I'm lazy, I like rid of being prompted for a password.

`visudo`

Add the line `benv ALL=(ALL) ALL`

uncomment `%wheel ALL=(ALL) NOPASSWD: ALL`

### ADDITIONAL PACKAGES

I lied earlier, in nearly all cases all of these are getting installed.

`pacman -S network-manager-applet firefox firefox-developer-edition alacritty emacs gnome-keyring lxappearance vlc ark`

### INSTALL AURA

I really like aura in spite of the Haskell dependencies. Doing this here because some of the environments depend on AUR packages.

`cd /opt`

`sudo git clone https://aur.archlinux.org/aura.git`

`sudo chown -R benv ./aura`

`cd aura`

`makepkg -si`

## SETTING UP AN ENVIRONMENT

Old notes for everything I may have been interested in at one point, currently the main thing I use is Qtile.

### Qtile

`pacman -S qtile pulseaudio alsa-utils pcmanfm lxsession`

And then these correspond with what's in my config.

For X11's sake, `pacman -S picom rofi`

For Wayland's arksake, `pacman -S kanshi fuzzel`

Todo

- Sort a display manager here

### i3

`pacman -S i3 xorg xorg-xinit i3status xterm xorg-xeyes xorg-xclock alsa-utils pulseaudio pcmanfm picom`

`pacman -S i3status xterm xorg-xeyes xorg-xclock alsa-utils pulseaudio pcmanfm picom`

`pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings`

`systemctl enable lightdm`

`localectl --no-convert set-x11-keymap gb`

### PLASMA

`pacman -S xorg plasma plasma-wayland-session kde-applications`

`systemctl enable sddm.service`

### XFCE

`pacman -S xorg xorg-server`

`pacman -S xfce4 xfce4-goodies`

`pacman -S lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings`

`systemctl enable lightdm`

### GNOME

`pacman -S gnome gnome-extra`

`systemctl enable gdm.service`

### PACMAN CONFIG

`nano /etc/pacman.conf`

UNCOMMENT 'MULTILIB' LINES

`pacman -Syu`

## POST POST INSTALL  PACKAGE INSTALLATION (OPTIONAL)

### PACMAN PACKAGES

`pacman -S discord cura conky conky-manager grub-customizer feh vlc`

### AUR PACKAGES

`aura -A visual-studio-code-bin nordvpn-bin dropbox zoom steam-fonts timeshift evernote-beta-bin ocs-url ttf-fork-awesome pa-applet-git`

### FONTS

Quality of life, and overkill - don't judge me.

`pacman -S noto-fonts noto-fonts-emoji ttf-roboto terminus-font ttf-bitstream-vera ttf-croscore ttf-dejavu ttf-droid ttf-anonymous-pro ttf-cascadia-code ttf-fira-mono ttf-fira-code ttf-hack ttf-inconsolata ttf-jetbrains-mono adobe-source-code-pro-fonts`
