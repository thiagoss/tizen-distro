# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# Copyright (c) 2012, Intel Corporation.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# DESCRIPTION
# This module implements the kernel-related functions used by
# 'yocto-kernel' to manage kernel config items and patches for Yocto
# BSPs.
#
# AUTHORS
# Tom Zanussi <tom.zanussi (at] intel.com>
#

import sys
import os
import shutil
from tags import *
import glob
import subprocess


def find_bblayers(scripts_path):
    """
    Find and return a sanitized list of the layers found in BBLAYERS.
    """
    try:
        builddir = os.environ["BUILDDIR"]
    except KeyError:
        print "BUILDDIR not found, exiting. (Did you forget to source oe-init-build-env?)"
        sys.exit(1)
    bblayers_conf = os.path.join(builddir, "conf/bblayers.conf")

    layers = []

    f = open(bblayers_conf, "r")
    lines = f.readlines()
    bblayers_lines = []
    in_bblayers = False
    for line in lines:
        line = line.strip()
        if line.strip().startswith("BBLAYERS"):
            bblayers_lines.append(line)
            in_bblayers = True
            quotes = line.strip().count('"')
            if quotes > 1:
                break
            continue
        if in_bblayers:
            bblayers_lines.append(line)
            if line.strip().endswith("\""):
                break
            else:
                continue

    for i, line in enumerate(bblayers_lines):
        if line.strip().endswith("\\"):
            bblayers_lines[i] = line.strip().replace('\\', '')

    bblayers_line = " ".join(bblayers_lines)

    start_quote = bblayers_line.find("\"")
    if start_quote == -1:
        print "Invalid BBLAYERS found in %s, exiting" % bblayers_conf
        sys.exit(1)

    start_quote += 1
    end_quote = bblayers_line.find("\"", start_quote)
    if end_quote == -1:
        print "Invalid BBLAYERS found in %s, exiting" % bblayers_conf
        sys.exit(1)

    bblayers_line = bblayers_line[start_quote:end_quote]
    layers = bblayers_line.split()

    f.close()

    return layers


def find_meta_layer(scripts_path):
    """
    Find and return the meta layer in BBLAYERS.
    """
    layers = find_bblayers(scripts_path)

    for layer in layers:
        if layer.endswith("meta"):
            return layer

    return None


def find_bsp_layer(scripts_path, machine):
    """
    Find and return a machine's BSP layer in BBLAYERS.
    """
    layers = find_bblayers(scripts_path)

    for layer in layers:
        if machine in layer:
            return layer

    print "Unable to find the BSP layer for machine %s." % machine
    print "Please make sure it is listed in bblayers.conf"
    sys.exit(1)


def gen_choices_str(choices):
    """
    Generate a numbered list of choices from a list of choices for
    display to the user.
    """
    choices_str = ""

    for i, choice in enumerate(choices):
        choices_str += "\t" + str(i + 1) + ") " + choice + "\n"

    return choices_str


def open_user_file(scripts_path, machine, userfile, mode):
    """
    Find one of the user files (user-config.cfg, user-patches.scc)
    associated with the machine (could be in files/,
    linux-yocto-custom/, etc).  Returns the open file if found, None
    otherwise.

    The caller is responsible for closing the file returned.
    """
    layer = find_bsp_layer(scripts_path, machine)
    linuxdir = os.path.join(layer, "recipes-kernel/linux")
    linuxdir_list = os.listdir(linuxdir)
    for fileobj in linuxdir_list:
        fileobj_path = os.path.join(linuxdir, fileobj)
        if os.path.isdir(fileobj_path):
            userfile_name = os.path.join(fileobj_path, userfile)
            try:
                f = open(userfile_name, mode)
                return f
            except IOError:
                continue
    return None


def read_config_items(scripts_path, machine):
    """
    Find and return a list of config items (CONFIG_XXX) in a machine's
    user-defined config fragment [user-config.cfg].
    """
    config_items = []

    f = open_user_file(scripts_path, machine, "user-config.cfg", "r")
    lines = f.readlines()
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#"):
            config_items.append(s)
    f.close()

    return config_items


def write_config_items(scripts_path, machine, config_items):
    """
    Write (replace) the list of config items (CONFIG_XXX) in a
    machine's user-defined config fragment [user-config.cfg].
    """
    f = open_user_file(scripts_path, machine, "user-config.cfg", "w")
    for item in config_items:
        f.write(item + "\n")
    f.close()

    kernel_contents_changed(scripts_path, machine)


def yocto_kernel_config_list(scripts_path, machine):
    """
    Display the list of config items (CONFIG_XXX) in a machine's
    user-defined config fragment [user-config.cfg].
    """
    config_items = read_config_items(scripts_path, machine)

    print "The current set of machine-specific kernel config items for %s is:" % machine
    print gen_choices_str(config_items)


def yocto_kernel_config_rm(scripts_path, machine):
    """
    Display the list of config items (CONFIG_XXX) in a machine's
    user-defined config fragment [user-config.cfg], prompt the user
    for one or more to remove, and remove them.
    """
    config_items = read_config_items(scripts_path, machine)

    print "Specify the kernel config items to remove:"
    input = raw_input(gen_choices_str(config_items))
    rm_choices = input.split()
    rm_choices.sort()

    removed = []

    for choice in reversed(rm_choices):
        try:
            idx = int(choice) - 1
        except ValueError:
            print "Invalid choice (%s), exiting" % choice
            sys.exit(1)
        if idx < 0 or idx >= len(config_items):
            print "Invalid choice (%d), exiting" % (idx + 1)
            sys.exit(1)
        removed.append(config_items.pop(idx))

    write_config_items(scripts_path, machine, config_items)

    print "Removed items:"
    for r in removed:
        print "\t%s" % r


def yocto_kernel_config_add(scripts_path, machine, config_items):
    """
    Add one or more config items (CONFIG_XXX) to a machine's
    user-defined config fragment [user-config.cfg].
    """
    new_items = []

    for item in config_items:
        if not item.startswith("CONFIG") or (not "=y" in item and not "=m" in item):
            print "Invalid config item (%s), exiting" % item
            sys.exit(1)
        new_items.append(item)

    cur_items = read_config_items(scripts_path, machine)
    cur_items.extend(new_items)

    write_config_items(scripts_path, machine, cur_items)

    print "Added items:"
    for n in new_items:
        print "\t%s" % n


def find_current_kernel(bsp_layer, machine):
    """
    Determine the kernel and version currently being used in the BSP.
    """
    machine_conf = os.path.join(bsp_layer, "conf/machine/" + machine + ".conf")

    preferred_kernel = preferred_kernel_version = preferred_version_varname = None

    f = open(machine_conf, "r")
    lines = f.readlines()
    for line in lines:
        if line.strip().startswith("PREFERRED_PROVIDER_virtual/kernel"):
            preferred_kernel = line.split()[-1]
            preferred_kernel = preferred_kernel.replace('\"','')
            preferred_version_varname = "PREFERRED_VERSION_" + preferred_kernel
        if preferred_version_varname and line.strip().startswith(preferred_version_varname):
            preferred_kernel_version = line.split()[-1]
            preferred_kernel_version = preferred_kernel_version.replace('\"','')
            preferred_kernel_version = preferred_kernel_version.replace('%','')

    if preferred_kernel and preferred_kernel_version:
        return preferred_kernel + "_" + preferred_kernel_version
    elif preferred_kernel:
        return preferred_kernel


def find_filesdir(scripts_path, machine):
    """
    Find the name of the 'files' dir associated with the machine
    (could be in files/, linux-yocto-custom/, etc).  Returns the name
    of the files dir if found, None otherwise.
    """
    layer = find_bsp_layer(scripts_path, machine)
    filesdir = None
    linuxdir = os.path.join(layer, "recipes-kernel/linux")
    linuxdir_list = os.listdir(linuxdir)
    for fileobj in linuxdir_list:
        fileobj_path = os.path.join(linuxdir, fileobj)
        if os.path.isdir(fileobj_path):
            # this could be files/ or linux-yocto-custom/, we have no way of distinguishing
            # so we take the first (and normally only) dir we find as the 'filesdir'
            filesdir = fileobj_path

    return filesdir


def read_patch_items(scripts_path, machine):
    """
    Find and return a list of patch items in a machine's user-defined
    patch list [user-patches.scc].
    """
    patch_items = []

    f = open_user_file(scripts_path, machine, "user-patches.scc", "r")
    lines = f.readlines()
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#"):
            fields = s.split()
            if not fields[0] == "patch":
                continue
            patch_items.append(fields[1])
    f.close()

    return patch_items


def write_patch_items(scripts_path, machine, patch_items):
    """
    Write (replace) the list of patches in a machine's user-defined
    patch list [user-patches.scc].
    """
    f = open_user_file(scripts_path, machine, "user-patches.scc", "w")
    for item in patch_items:
        f.write("patch " + item + "\n")
    f.close()

    kernel_contents_changed(scripts_path, machine)


def yocto_kernel_patch_list(scripts_path, machine):
    """
    Display the list of patches in a machine's user-defined patch list
    [user-patches.scc].
    """
    patches = read_patch_items(scripts_path, machine)

    print "The current set of machine-specific patches for %s is:" % machine
    print gen_choices_str(patches)


def yocto_kernel_patch_rm(scripts_path, machine):
    """
    Remove one or more patches from a machine's user-defined patch
    list [user-patches.scc].
    """
    patches = read_patch_items(scripts_path, machine)

    print "Specify the patches to remove:"
    input = raw_input(gen_choices_str(patches))
    rm_choices = input.split()
    rm_choices.sort()

    removed = []

    filesdir = find_filesdir(scripts_path, machine)
    if not filesdir:
        print "Couldn't rm patch(es) since we couldn't find a 'files' dir"
        sys.exit(1)

    for choice in reversed(rm_choices):
        try:
            idx = int(choice) - 1
        except ValueError:
            print "Invalid choice (%s), exiting" % choice
            sys.exit(1)
        if idx < 0 or idx >= len(patches):
            print "Invalid choice (%d), exiting" % (idx + 1)
            sys.exit(1)
        filesdir_patch = os.path.join(filesdir, patches[idx])
        if os.path.isfile(filesdir_patch):
            os.remove(filesdir_patch)
        removed.append(patches[idx])
        patches.pop(idx)

    write_patch_items(scripts_path, machine, patches)

    print "Removed patches:"
    for r in removed:
        print "\t%s" % r


def yocto_kernel_patch_add(scripts_path, machine, patches):
    """
    Add one or more patches to a machine's user-defined patch list
    [user-patches.scc].
    """
    existing_patches = read_patch_items(scripts_path, machine)

    for patch in patches:
        if os.path.basename(patch) in existing_patches:
            print "Couldn't add patch (%s) since it's already been added" % os.path.basename(patch)
            sys.exit(1)

    filesdir = find_filesdir(scripts_path, machine)
    if not filesdir:
        print "Couldn't add patch (%s) since we couldn't find a 'files' dir to add it to" % os.path.basename(patch)
        sys.exit(1)

    new_patches = []

    for patch in patches:
        if not os.path.isfile(patch):
            print "Couldn't find patch (%s), exiting" % patch
            sys.exit(1)
        basename = os.path.basename(patch)
        filesdir_patch = os.path.join(filesdir, basename)
        shutil.copyfile(patch, filesdir_patch)
        new_patches.append(basename)

    cur_items = read_patch_items(scripts_path, machine)
    cur_items.extend(new_patches)
    write_patch_items(scripts_path, machine, cur_items)

    print "Added patches:"
    for n in new_patches:
        print "\t%s" % n


def inc_pr(line):
    """
    Add 1 to the PR value in the given bbappend PR line.  For the PR
    lines in kernel .bbappends after modifications.
    """
    idx = line.find("\"")

    pr_str = line[idx:]
    pr_str = pr_str.replace('\"','')
    fields = pr_str.split('.')
    fields[1] = str(int(fields[1]) + 1)
    pr_str = "\"" + '.'.join(fields) + "\"\n"

    idx2 = line.find("\"", idx + 1)
    line = line[:idx] + pr_str
    
    return line


def kernel_contents_changed(scripts_path, machine):
    """
    Do what we need to do to notify the system that the kernel
    recipe's contents have changed.
    """
    layer = find_bsp_layer(scripts_path, machine)

    kernel = find_current_kernel(layer, machine)
    if not kernel:
        print "Couldn't determine the kernel for this BSP, exiting."
        sys.exit(1)

    kernel_bbfile = os.path.join(layer, "recipes-kernel/linux/" + kernel + ".bbappend")
    if not os.path.isfile(kernel_bbfile):
        kernel_bbfile = os.path.join(layer, "recipes-kernel/linux/" + kernel + ".bb")
        if not os.path.isfile(kernel_bbfile):
            return
    kernel_bbfile_prev = kernel_bbfile + ".prev"
    shutil.copyfile(kernel_bbfile, kernel_bbfile_prev)

    ifile = open(kernel_bbfile_prev, "r")
    ofile = open(kernel_bbfile, "w")
    ifile_lines = ifile.readlines()
    for ifile_line in ifile_lines:
        if ifile_line.strip().startswith("PR"):
            ifile_line = inc_pr(ifile_line)
        ofile.write(ifile_line)
    ofile.close()
    ifile.close()


def kernels(context):
    """
    Return the list of available kernels in the BSP i.e. corresponding
    to the kernel .bbappends found in the layer.
    """
    archdir = os.path.join(context["scripts_path"], "lib/bsp/substrate/target/arch/" + context["arch"])
    kerndir = os.path.join(archdir, "recipes-kernel/linux")
    bbglob = os.path.join(kerndir, "*.bbappend")

    bbappends = glob.glob(bbglob)

    kernels = []

    for kernel in bbappends:
        filename = os.path.splitext(os.path.basename(kernel))[0]
        idx = filename.find(CLOSE_TAG)
        if idx != -1:
            filename = filename[idx + len(CLOSE_TAG):].strip()
        kernels.append(filename)

    kernels.append("custom")

    return kernels


def extract_giturl(file):
    """
    Extract the git url of the kernel repo from the kernel recipe's
    SRC_URI.
    """
    url = None
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("SRC_URI"):
            line = line[len("SRC_URI"):].strip()
            if line.startswith("="):
                line = line[1:].strip()
                if line.startswith("\""):
                    line = line[1:].strip()
                    prot = "git"
                    for s in line.split(";"):
                        if s.startswith("git://"):
                            url = s
                        if s.startswith("protocol="):
                            prot = s.split("=")[1]
                    if url:
                        url = prot + url[3:]
    return url


def find_giturl(context):
    """
    Find the git url of the kernel repo from the kernel recipe's
    SRC_URI.
    """
    name = context["name"]
    filebase = context["filename"]
    scripts_path = context["scripts_path"]

    meta_layer = find_meta_layer(scripts_path)

    kerndir = os.path.join(meta_layer, "recipes-kernel/linux")
    bbglob = os.path.join(kerndir, "*.bb")
    bbs = glob.glob(bbglob)
    for kernel in bbs:
        filename = os.path.splitext(os.path.basename(kernel))[0]
        if filename in filebase:
            giturl = extract_giturl(kernel)
            return giturl
    
    return None

    
def base_branches(context):
    """
    Return a list of the base branches found in the kernel git repo.
    """
    giturl = find_giturl(context)

    print "Getting branches from remote repo %s..." % giturl

    gitcmd = "git ls-remote %s *heads* 2>&1" % (giturl)
    tmp = subprocess.Popen(gitcmd, shell=True, stdout=subprocess.PIPE).stdout.read()

    branches = []

    if tmp:
        tmpline = tmp.split("\n")
        for line in tmpline:
            if len(line)==0:
                break;
            if not line.endswith("base"):
                continue;
            idx = line.find("refs/heads/")
            kbranch = line[idx + len("refs/heads/"):]
            if kbranch.find("/") == -1 and kbranch.find("base") == -1:
                continue
            idx = kbranch.find("base")
            branches.append(kbranch[:idx - 1])

    return branches


def all_branches(context):
    """
    Return a list of all the branches found in the kernel git repo.
    """
    giturl = find_giturl(context)

    print "Getting branches from remote repo %s..." % giturl

    gitcmd = "git ls-remote %s *heads* 2>&1" % (giturl)
    tmp = subprocess.Popen(gitcmd, shell=True, stdout=subprocess.PIPE).stdout.read()

    branches = []

    base_prefixes = None

    try:
        branches_base = context["branches_base"]
        if branches_base:
            base_prefixes = branches_base.split(":")
    except KeyError:
        pass

    arch = context["arch"]

    if tmp:
        tmpline = tmp.split("\n")
        for line in tmpline:
            if len(line)==0:
                break;
            idx = line.find("refs/heads/")
            kbranch = line[idx + len("refs/heads/"):]
            kbranch_prefix = kbranch.rsplit("/", 1)[0]

            if base_prefixes:
                for base_prefix in base_prefixes:
                    if kbranch_prefix == base_prefix:
                        branches.append(kbranch)
                continue

            if (kbranch.find("/") != -1 and
                (kbranch.find("standard") != -1 or kbranch.find("base") != -1) or
                kbranch == "base"):
                branches.append(kbranch)
                continue

    return branches
