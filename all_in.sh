#!/bin/bash

source_code_project="your_source_code_project"
source_code=$(ls -l ${source_code_project} | awk '/^d/ {print $NF}')

# makepkg from source code folder
for i in ${source_code}; do
  cd "${source_code_project}/${i}" || return
  updpkgsums
  namcap PKGBUILD
  makepkg --syncdeps -f
  makepkg --printsrcinfo >.SRCINFO
done

repo_path="your_/archlinux/x86_64"
all_pkg=$(find "${repo_path}" -name "*.pkg.tar.xz" | awk -F "/" '{print $NF}')
db_name="fermiarcs"

# delete old sig and db
rm ${repo_path}/*.sig
rm ${repo_path}/${db_name}.*

for i in ${all_pkg}; do

  # sign all
  gpg --batch --passphrase-file your_password_file --pinentry-mode loopback --detach-sign "${repo_path}/${i}"

  # build repo db
  repo-add "${repo_path}/${db_name}.db.tar.gz" "${repo_path}/${i}"
done
