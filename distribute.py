#!/usr/bin/python

import os
import tomllib as toml


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


# create symlinks
def create_symlink(index, source, target):
    
    nsp = len(str(index[1]))
    index_pref = f"{index[0]: ^{nsp + INDEX_SPACING}}" | CGREEN
    index_suff = f"{index[1]: ^{nsp + INDEX_SPACING}}" | CGREEN                               
    pre_space = (2 * INDEX_SPACING + 6) * " "

    print(f" [{index_pref}/{index_suff}] Symlink {source | CBLUE} --> {target | CCYAN}")
    
    if os.path.exists(target) or os.path.isfile(target) or os.path.isdir(target):
        print(
            f"{pre_space} ! Symlink '{target | CCYAN}' already exists. Removing old symlink."
        )
        if os.path.isdir(target):
            os.system(f"""rm -rf {target}""")
        else:
            os.system(f"""rm {target}""")
    symlink_cmd = f"""ln -s "{source}" "{target}" """
    os.system(symlink_cmd)


# iterate TOML definition
def load_target_file(path):
    try:
        with open(path, "rb") as fp:
            dirname = os.path.dirname(__file__)[:-1]
            toml_data = toml.load(fp)

            for dotfiles in toml_data.keys():
                data = toml_data[dotfiles]
                size = len(data)
                for i, (source, target) in enumerate(data.items(), start=1):
                    print(dirname,dotfiles,source)
                    abs_source_path = os.path.join(dirname, dotfiles, source)
                    target = target.replace("$HOME", os.environ["HOME"])
                    create_symlink([i,size],abs_source_path, target)
                    print()
    except Exception as exc:
        print("Error:", exc)


print(40 * "=" + "[ SYMLINKING DOTFILES ]" + 40 * "=", "\n")
load_target_file("targets.toml")
print("DONE...")
