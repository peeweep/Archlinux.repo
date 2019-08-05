updpkgsums
namcap PKGBUILD
makepkg --syncdeps --force --noconfirm
makepkg --printsrcinfo > .SRCINFO
