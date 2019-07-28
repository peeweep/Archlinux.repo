#!/bin/bash

script_path=$(
  cd "$(dirname "${BASH_SOURCE[0]}")" || exit
  pwd
)

# repo folder same as this script
repo_path="${script_path}"

all_pkg=$(find "${repo_path}" -name "*.pkg.tar.xz" | awk -F "/" '{print $NF}')
db_name="fermiarcs"

# delete old sig and db
rm ${repo_path}/*.sig
rm ${repo_path}/${db_name}.*

for i in ${all_pkg}; do
  # get the package name
  package=${i}
  for j in {1..3}; do
    remove=$(echo ${package} | awk -F '-' '{print $NF}')
    package=$(echo ${package} | sed "s/-${remove}//")
  done

  # get the version name
  if [ "$(find ${repo_path} -name "${package}-[0-9]*.pkg.tar.xz" | wc -l)" -gt "1" ]; then
    remove=$(echo ${i} | awk -F '-' '{print $NF}' | head -n 1)
    version=$(echo ${i} | sed "s/-${remove}//g" | sed "s/${package}-//g" | awk -F ' ' '{print $1}')
    # version: 69.0b6-1

    # get the lastest_package
    find ${repo_path} -name "${package}-[0-9]*.pkg.tar.xz" >>${package}_version.txt
    lastest_package=$(sort -rV ${package}_version.txt | head -n 1)

    if [[ ${repo_path}/${i} == ${lastest_package} ]]; then
      # sign and repo-add the lastest_package
      gpg --batch --passphrase-file your_password_file --pinentry-mode loopback --detach-sign "${lastest_package}"
      repo-add "${repo_path}/${db_name}.db.tar.gz" "${lastest_package}"
      # remove old packages
      sed -i "s~${lastest_package}~~" ${package}_version.txt
      for i in $(sort firefox-beta-bin_version.txt | uniq); do
        rm ${i}*
      done

    fi
  # only have one version
  else
    gpg --batch --passphrase-file your_password_file --pinentry-mode loopback --detach-sign "${repo_path}/${i}"
    repo-add "${repo_path}/${db_name}.db.tar.gz" "${repo_path}/${i}"

  fi
done

# delete ${repo_path}/*_version.txt
if [ -n "$(find ${repo_path} -maxdepth 1 -name '*_version.txt')" ]; then
  rm ${repo_path}/*_version.txt
fi
