updpkgsums
namcap PKGBUILD
makepkg --syncdeps -f
makepkg --printsrcinfo > .SRCINFO
