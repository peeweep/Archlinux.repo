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

  # sign all
  gpg --detach-sign "${i}"

  # build repo db
  repo-add "${db_name}.db.tar.gz" "${i}"
done
