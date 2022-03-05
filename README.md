# rsync-time-browse


Search for changes to specific files within a hardlink based backup. There are many programs that create hardlink style backup trees. This should work on any that use a 'backup.marker' file to denote the root of a backup tree. Probably others with minor tweaks.

The --links-dir option is particularly useful.

Tested with backups made by:

* [laurent22/rsync-time-backup](https://github.com/laurent22/rsync-time-backup)
* [eaut/rsync-time-backup](https://github.com/eaut/rsync-time-backup)



```
$./tmbrowse.py -h
usage: tmbrowse.py [-h] [-a] [-f] [-m] [-l LINKS_DIR] [input [input ...]]

List all version of a specific file in a timemachine style hardlink backup dir.

positional arguments:
  input                 input file ...

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Output every file, not just unique ones.
  -f, --fullpath        output the full path to files. Default: the absolute path from backup root
  -m, --md5             compare files based on md5hash. Default: compare by size only.
  -l LINKS_DIR, --links-dir LINKS_DIR
                        Directory to story links in. Create a linked file for each unique file found.
```
