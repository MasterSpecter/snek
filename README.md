# Image Processing Tool

```shell
usage: python process.py [-h] [-d] base

positional arguments:
  base          Path to base folder that will be recursively searched for TIFFs

options:
  -h, --help    show this help message and exit
  -d, --delete  Delete existing JPEGs
```

## Description

This tool recursively searches all folders in the base folder for TIFF files. When found, a folder called "_IA" is created at the current level. Lower resolution JPEGs are made from the TIFFs, and all TIFFs are zipped in a folder called "raw.zip". Then the zipped folder and JPEGs are placed in the "_IA" folder. If the `-d` flag is used, existing JPEGs in the folder are deleted before new ones are created. If a folder already has an "_IA" folder, it is ignored.

## Requirements

* Python 3
* [Image Magick](https://imagemagick.org/download/#gsc.tab=0) (installed and viewable from `PATH` environment variable)
