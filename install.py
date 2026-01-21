#!/usr/bin/python

import os
import tomllib as toml
from subprocess import Popen, STDOUT, PIPE
from shlex import split 


# Text colorization
class Colorize:

    def __init__(self, *args):
        self.args = args

    def __getitem__(self, string):
        args = ";".join([str(i) for i in self.args])
        return f"\033[{args}m{string}\033[0m"

    def __ror__(self, string):
        return self[string]


CBLUE = Colorize(95)
CCYAN = Colorize(96)
CGREEN = Colorize(92)

INDEX_SPACING = 2


def has_package(command):
    proc = Popen(split(f"which {command}"), stdout=PIPE, stderr=PIPE)
    proc.communicate() 
    if proc.returncode == 0:
        return True 
    else:
        return False


def run_cmd(command):
    print(f"=> {command}")
    os.system(command)


def install_pkg(packager, packages):
    shcmd_template = "sudo {pkgr} {opt} {pkgs}"
    pkgs_string = " ".join(packages)

    if packager in ["dnf", "yum"] and has_package(packager):
        shcmd = shcmd_template.format(pkgr=packager, opt="install", pkgs=pkgs_string)
        run_cmd(shcmd)

    if packager in ["zypper"] and has_package(packager):
        shcmd = shcmd_template.format(pkgr=packager, opt="install", pkgs=pkgs_string)
        run_cmd(shcmd)

    elif packafer in ["apt", "apt-get"] and has_package(packager):
        shcmd = shcmd_template.format(pkgr=packager, opt="install", pkgs=pkgs_string)
        run_cmd(shcmd)

    elif packafer in ["pacman"] and has_package(packager):
        shcmd = shcmd_template.format(pkgr=packager, opt="-Syy", pkgs=pkgs_string)
        run_cmd(shcmd)
    else:
        print(f"Packager {packager} is not valid in this context.")


# iterate TOML definition
def load_target_file(path):
    try:
        with open(path, "rb") as fp:
            dirname = os.path.dirname(__file__)[:-1]
            toml_data = toml.load(fp)["install"]
            
            # packagers
            for packager in toml_data["packagers"].keys():
                install_pkg(packager, toml_data["packagers"][packager])

            # COMMANDS
            for command in toml_data["commands"]["cmds"]:
                run_cmd(command)

            #syspip
            for pip in toml_data["syspip"].keys():
                pip_pkgs = toml_data["syspip"][pip]
                pkgstr = " ".join(pip_pkgs) 
                run_cmd(f"{pip}/bin/pip install {pkgstr}")

    except Exception as exc:
        print("Error:", exc)


print(40 * "=" + "[ INSTALLING PACKAGES & COMMANDS ]" + 40 * "=", "\n")
load_target_file("packages.toml")
print("DONE...")
