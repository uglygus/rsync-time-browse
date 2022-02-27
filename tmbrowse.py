#!/usr/bin/env python3

import argparse
import errno
import hashlib
import os
import re
import shutil
import subprocess

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
    print("BACKUP_ROOT = ", backup_root)

    pattern = ".+\d\d\d\d-\d\d-\d\d-\d\d\d\d\d\d(.+)"
    m = re.search(pattern, orig_path)
    if m:
        rel_path = m.group(1)
        rel_path = rel_path.lstrip("/")  # to make it relative strip leading slash

    backups = get_backup_folders(backup_root)

    num_backups = len(backups)
    print(f"Contains __{num_backups}__ backup folders.\n")

    previous_md5 = ""
    previous_size = ""
    this_md5 = ""

    for b in backups:

        b_date = os.path.split(b)[1]
        b_fullpath = os.path.join(b, rel_path, file)

        if args.fullpath:
            print(backup_root + "/", end="")

        print(b_date + "/", end="")

        this_md5 = ""
        this_size = ""

        if os.path.exists(b_fullpath):
        3 ake this depend on th -u flag    file_stats = os.stat(b_fullpath)
            this_size = file_stats.st_size
            if args.md5:
                this_md5 = md5(b_fullpath)

        #    print(os.path.join(rel_path, file), end="")
            # print("/" + file, end="")

            if args.md5:
                is_changed = this_md5 != previous_md5
            else:
                is_changed = this_size != previous_size

            if is_changed:
                print(os.path.join(rel_path, file), end="")
                print("\t_size=", this_size, end="")
                if args.md5:
                    print("\t_md5=", this_md5, end="")
            else:
                print('       "', end="")

                if args.links_dir:
                    os.makedirs(path, exists=True)
                    # make_sure_path_exists(args.links_dir)
                    os.symlink(b_fullpath, os.path.join(args.links_dir, b_date + "__" + file))

        else:
            pass

        previous_md5 = this_md5
        previous_size = this_size
        previous_fullpath = b_fullpath
        print("")


def main():

    parser = argparse.ArgumentParser(
        description="List all version of a specific file in a timemachine style hardlink backup dir."
    )
    parser.add_argument("input", nargs="*", default="", help="input file ...")

    parser.add_argument(
        "-u",
        "--unique",
        action="store_true",
        help="Only output each file state once.",
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
        "-d",
        "--links-dir",
        type=str,
        default="",
        help="Create a linked file to each state of the fle. Directory to story links in.",
    )

    global args
    args = parser.parse_args()

    print("args==", args)

    if not len(args.input):
        print("asdf")
        parser.print_help()
        return 0

    if os.path.exists(args.links_dir):
        shutil.rmtree(args.links_dir, ignore_errors=True)

    if args.md5:
        print("Comparing by md5sum. This could be slow if the file is large.")
    else:
        print("Comparing by file size.")
    for single_input in args.input:

        print("os.path.isfile(single_input)=", os.path.isfile(single_input))

        if not (os.path.isdir(single_input) or os.path.isfile(single_input)):
            parser.print_help()
            return 0

        absinput = os.path.abspath(single_input)

        if os.path.isdir(absinput):
            print(single_input, "is not a file. Folders do not work.")

        if os.path.isfile(absinput):
            process_file(absinput)


if __name__ == "__main__":
    main()
