updpkgsums
namcap PKGBUILD
makepkg --syncdeps --force --noconfirm --nocheck
makepkg --printsrcinfo > .SRCINFO
sudo pacman -Rns $(pacman -Qtdq) --noconfirm

