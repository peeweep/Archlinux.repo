#!/usr/bin/env python3
import os
import shlex
import logging
import subprocess
from packaging import version
import fnmatch


def get_subdir(father_dir):
    # 整一个空的子目录列表
    subdir = []
    # 遍历目录下所有子目录、文件
    for i in os.walk(father_dir):
        # 找出子目录，忽略文件
        if i[0] == father_dir:
            # i = ('father_dir', ['subdir1', 'subdir2'], ['file1', 'file2', 'file3'])
            for j in i[1]:
                # 忽略 .git 之类的目录
                if j[0] != ".":
                    # 尾部插入到 subdir
                    subdir.append(j)
    return subdir


def get_file_content(file__path):
    f = open(file__path)
    content = f.read()
    f.close()
    return content


def build_pkg(args=None):
    proc = subprocess.Popen("pwd", shell=True)
    proc.communicate()[0]


def build_extra(args=None):
    if args == "check()" or args == "check":
        build_extra = shlex.split('extra-x86_64-build -c -- -- --nocheck')
    else:
        build_extra = ['extra-x86_64-build', '-c']
    proc_build_extra = subprocess.Popen(build_extra, shell=True)
    proc_build_extra.communicate()[0]


def update_SRCINFO():
    update_SRCINFO = shlex.split('makepkg --printsrcinfo > .SRCINFO')
    proc_update_SRCINFO = subprocess.Popen(update_SRCINFO, shell=True)
    proc_update_SRCINFO.communicate()[0]


def update_pkg(root_dir, sub_directories):
    for sub_dir in sub_directories:
        # sub_dir_path = root_dir + "/" + sub_dir
        # 进入目录 /father_dir/sub_dir1
        os.chdir(root_dir + "/" + sub_dir)

        # 跳过检查
        keyword_check = 'check()'
        if keyword_check in get_file_content(root_dir + "/" + sub_dir + "/PKGBUILD"):
            # build_extra(keyword_check)
            # update_SRCINFO()
            print("skip sub_dir: %s" % sub_dir)
        else:
            # build_extra()
            # update_SRCINFO()
            print("cur sub_dir is: %s, dont skip" % sub_dir)


def get_latest_pkgname(root_dir, sub_directories):
    pkgfile_list = []
    for sub_dir in sub_directories:
        sub_dir_folder = root_dir + "/" + sub_dir
        os.chdir()
        # 遍历目录下所有子目录、文件
        for i in os.walk(sub_dir_folder):
            if i[0] == sub_dir_folder:
                # i = ('father_dir', ['subdir1', 'subdir2'], ['file1', 'file2', 'file3'])
                for j in i[2]:
                    # 同配符号找出 sub_dir-*.pkg.tar.xz
                    if fnmatch.fnmatch(i, sub_dir + "-*.pkg.tar.xz"):
                        pkgfile_list.append(j)
        if len(pkgfile_list) > 1:
            same_package_name = []
            for i in pkgfile_list:
                # sub_dir-*.pkg.tar.xz 两个相近的元素自左边找出相同的
                for x in i:
                    if x in i + 1:
                        same_package_name.append(x)
                if str(same_package_name) == sub_dir:
                    pass
    # return latest_version


root_dir = os.path.dirname(os.path.abspath(__file__))
sub_directories = get_subdir(root_dir)
update_pkg(root_dir, sub_directories)
get_latest_pkgname(root_dir, sub_directories)

pkgfile_dir = root_dir + "/pkg/archlinux/x86_64"
# 检查目录是否存在
if not os.path.exists(pkgfile_dir):
    # 多层创建目录
    os.makedirs(pkgfile_dir)
