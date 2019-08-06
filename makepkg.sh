updpkgsums
namcap PKGBUILD
makepkg --syncdeps --force --noconfirm
makepkg --printsrcinfo > .SRCINFO
sudo pacman -Rns $(pacman -Qtdq) --noconfirm

