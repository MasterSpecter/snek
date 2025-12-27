#!/usr/bin/env python3

from pathlib import Path
import argparse
import os
from zipfile import ZipFile
import subprocess

def get_jpegs(folder: Path):
    return [jpeg for jpeg in folder.iterdir() if jpeg.suffix == '.jpg']

def get_tiffs(folder: Path):
    return [tiff for tiff in folder.iterdir() if tiff.suffix == '.tif']

def get_subs(folder: Path):
    return [sub for sub in folder.iterdir() if sub.is_dir()]

def navigate(folder: Path, delete: bool):
    subs = get_subs(folder)
    jpegs = get_jpegs(folder)
    tiffs = get_tiffs(folder)

    if delete and jpegs:
        for j in jpegs:
            os.remove(str(j))

    subprocess.run(["magick", "mogrify", "-format", "jpg", "*.tif"])
    
    with ZipFile("raw.zip", "w") as raw:
        for tiff in tiffs:
            raw.write(tiff)

    for tiff in tiffs:
        os.remove(str(tiff))

    for sub in subs:
        navigate(sub, delete)

def process(base: str, delete: bool):
    base_path = Path(base)
    navigate(base_path, delete)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base", help="Path to base folder that will be recursively searched for TIFFs")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete existing JPEGs")
    args = parser.parse_args()
    process(args.base, args.delete)
