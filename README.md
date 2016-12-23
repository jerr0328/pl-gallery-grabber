# PL Gallery Grabber

Grabs the latest gallery images, useful if you like having gallery images for desktop background

Requires Python 3.

## Instructions

1. Clone repository with `git clone git@code.earth.planet.com:jeremy/pl-gallery-grabber.git`
2. Go into directory: `cd pl-gallery-grabber`
3. Install requirements: `pip install -r requirements.txt`
4. Run the Python script, passing in directory to download to (otherwise downloads to current directory) e.g.: `./plg.py ~/Backgrounds/`

Note: Ensure target directory already exists.

## Usage Options

Full help available by calling with `--help`:
```text
usage: plg.py [-h] [-q] [-o] [-l LIMIT] [-n] directory

positional arguments:
  directory             Images output directory

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't print anything
  -o, --overwrite       Get the image, even if it already exists. Ignores
                        --newer flag.
  -l LIMIT, --limit LIMIT
                        Number of images to download [default: 10]
  -n, --newer           Only get newer images. Script stops when it detects
                        already-existing files.
```
