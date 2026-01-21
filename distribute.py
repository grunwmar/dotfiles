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
def create_symlink(source, target):
    if os.path.exists(target):
        pre_space = (2 * INDEX_SPACING + 6) * " "
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
            dirname = os.path.dirname(__file__)
            toml_data = toml.load(fp)

            for dotfiles in toml_data.keys():
                data = toml_data[dotfiles]
                size = len(data)
                nsp = len(str(size))
                for i, (source, target) in enumerate(data.items(), start=1):
                    abs_source_path = os.path.join(dirname, dotfiles, source)
                    index_pref = f"{i: ^{nsp + INDEX_SPACING}}" | CGREEN
                    index_suff = f"{size: ^{nsp + INDEX_SPACING}}" | CGREEN

                    print(
                        f" [{index_pref}/{index_suff}] Symlink {abs_source_path | CBLUE} --> {target | CCYAN}"
                    )

                    target = target.replace("$HOME", os.environ["HOME"])
                    create_symlink(abs_source_path, target)
                    print()
    except Exception as exc:
        print("Error:", exc)


print(40 * "=" + "[ SYMLINKING DOTFILES ]" + 40 * "=", "\n")
load_target_file("targets.toml")
print("DONE...")
