updpkgsums
namcap PKGBUILD
makepkg --printsrcinfo > .SRCINFO
makepkg --syncdeps -f
