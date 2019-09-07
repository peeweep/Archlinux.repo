#!/usr/bin/env python3

import os
import fnmatch

sub_dir = "a"
pkgfile_list = []
for _dir, folder, files in os.walk("."):
    # print(files)
    for _file in files:
        # print(_file)
        # 同配符号找出 sub_dir-*.pkg.tar.xz
        if fnmatch.fnmatch(_file, sub_dir + '-*.pkg.tar.xz'):
            # print(_file)
            pkgfile_list.append(_file)
pkgfile_list.sort()
pkgfile_list_after_remove = pkgfile_list
print(len(pkgfile_list))
print(pkgfile_list[0].rfind('.pkg.tar.xz'))
print(pkgfile_list[1].rfind('.pkg.tar.xz'))

for i in range(len(pkgfile_list)):
    # 根据 .pkg.tar.xz 开始元素位置找到相同包名
    if len(pkgfile_list_after_remove) > 1:
        # a.r1096.ea2b7a3.pkg.tar.xz a.r880.69e75c9.pkg.tar.xz 无法识别
        if pkgfile_list[i].rfind('.pkg.tar.xz') == pkgfile_list[i+1].rfind('.pkg.tar.xz'):
            os.remove(pkgfile_list[i])
            pkgfile_list_after_remove.remove(i)
    print(pkgfile_list[i])

print(pkgfile_list_after_remove)

# clion-2019.1-1.pkg.tar.xz  clion-2019.2-1.pkg.tar.xz  clion-cmake-2019.1-1.pkg.tar.xz  clion-cmake-2019.2-1.pkg.tar.xz
