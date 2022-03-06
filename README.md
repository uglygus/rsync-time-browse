# rsync-time-browse

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/psf/black/blob/main/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>

Search for changes to specific files within a hardlink based backup. There are many programs that create hardlink style backup trees. This should work on any that use a 'backup.marker' file to denote the root of a backup tree. Probably others with minor tweaks.

The --links-dir option is particularly useful.

Tested with backups made by:

* [laurent22/rsync-time-backup](https://github.com/laurent22/rsync-time-backup)
* [eaut/rsync-time-backup](https://github.com/eaut/rsync-time-backup)



## Usage

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



## License

The MIT License (MIT)

Copyright (c) 2013-2018 Laurent Cozic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
