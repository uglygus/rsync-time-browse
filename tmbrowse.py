#!/usr/bin/env python3

import argparse
import errno
import hashlib
import os
import re
import shutil
import subprocess
import sys

args = argparse.Namespace()


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def md5(filename):
    with open(filename, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def get_backup_root(filename):
    """
    Walks back a directory tree until it finds a folder containing
    the file 'backup.marker' .

    returns that folder or False.
    """

    path_parts = os.path.split(filename)

    if path_parts[0] == "/":
        return False

    if os.path.exists(os.path.join(path_parts[0], "backup.marker")):
        return path_parts[0]

    return get_backup_root(path_parts[0])


def get_backup_folders(path):
    """returns a list of the date/time folder names for
    each backup in the archive.
    """

    dates = []
    dirs = os.listdir(path)

    date_pattern = "(\d\d\d\d-\d\d-\d\d-\d\d\d\d\d\d)"

    for file in dirs:
        if re.match(date_pattern, file):
            dates.append(os.path.join(path, file))

    dates.sort(reverse=True)
    return dates


def process_file(filename):

    rel_path = ""
    orig_path, file = os.path.split(filename)
    backup_root = get_backup_root(filename)
#    print("BACKUP_ROOT = ", backup_root)
    if not backup_root:
        print("Cannot find .marker in this tree:", filename)
        return

    print(filename)

    pattern = ".+\d\d\d\d-\d\d-\d\d-\d\d\d\d\d\d(.+)"
    m = re.search(pattern, orig_path)
    if m:
        rel_path = m.group(1)
        rel_path = rel_path.lstrip("/")  # to make it relative strip leading slash

    backups = get_backup_folders(backup_root)

    num_backups = len(backups)
    print(f"{num_backups}  backups at root:", backup_root)

    previous_md5 = ""
    previous_size = ""
    this_md5 = ""


    if args.links_dir:
        try:
            make_sure_path_exists(args.links_dir)
            #os.makedirs(args.links_dir, exist_ok=False)
        except FileExistsError:
            print('links dir exists already. No links made.')
            args.links_dir=False

    for b in backups:

        b_date = os.path.split(b)[1]
        b_fullpath = os.path.join(b, rel_path, file)

        if args.fullpath:
            print(backup_root + "/", end="")

        this_md5 = ""
        this_size = ""

        if os.path.exists(b_fullpath):
            file_stats = os.stat(b_fullpath)
            this_size = file_stats.st_size


            size_changed = this_size != previous_size
            if not size_changed and args.md5:
                this_md5 = md5(b_fullpath)
                is_changed = this_md5 != previous_md5
            else:
                is_changed = size_changed
            # if args.md5:
            #     this_md5 = md5(b_fullpath)
            #     is_changed = this_md5 != previous_md5
            # else:
            #     is_changed = this_size != previous_size

            if is_changed:
                print(b_date + "/", end="")
                print(os.path.join(rel_path, file), end="")
                print("\t_size=", this_size, end="")
                if args.md5:
                    print("\t_md5=", this_md5, end="")
                print("")
            else:
                if args.all:
                    print(b_date + "/", end="")
                    print('       "', end="")
                    print("")
                if args.links_dir:
                    try:
                        os.symlink(b_fullpath, os.path.join(args.links_dir, b_date + "__" + file))
                    except FileExistsError:
                        print('file missing')
        else:
            pass

        previous_md5 = this_md5
        previous_size = this_size
        previous_fullpath = b_fullpath


def is_windows_lnk(file):
    if os.path.splitext(file)[1] == ".lnk":
        return True
    return False

def main():

    parser = argparse.ArgumentParser(
        description="List all version of a specific file in a timemachine style hardlink backup dir."
    )

    parser.add_argument("input", nargs="*", default="", help="input file ...")

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Output every file, not just unique ones.",
    )

    parser.add_argument(
        "-f",
        "--fullpath",
        action="store_true",
        help="output the full path to files. Default: the absolute path from backup root",
    )

    parser.add_argument(
        "-m",
        "--md5",
        action="store_true",
        help="compare files based on md5hash. Default: compare by size only.",
    )

    parser.add_argument(
        "-l",
        "--links-dir",
        type=str,
        default="",
        help="Directory to story links in. Create a linked file for each unique file found. ",
    )

    global args
    args = parser.parse_args()

    #print("args==", args)

    if not len(args.input):
        parser.print_help()
        return 0

    if os.path.exists(args.links_dir):
        shutil.rmtree(args.links_dir, ignore_errors=True)

    if args.md5:
        print("Comparing by md5sum. This could be slow if the file is large.")


    for single_input in args.input:

        print('\n')

        absinput = os.path.abspath(single_input)

        if not os.path.exists(single_input):
            print("File not Found:", single_input)
            continue

        if os.path.isdir(absinput):
            print(f"Directories not supported. '{single_input}'")
            continue

        if not (
            os.path.isfile(single_input)
            or os.path.islink(single_input)
            or is_windows_lnk(single_input)
        ):
            print("Not a file:", single_input)
            continue

        if os.path.isfile(absinput):
            process_file(absinput)


if __name__ == "__main__":
    sys.exit(main())
