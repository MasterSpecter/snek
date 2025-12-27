#!/usr/bin/env python3

from pathlib import Path
import argparse
import os
from zipfile import ZipFile, ZIP_DEFLATED
import subprocess
import shutil

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
    print(f'working in folder {str(folder)}')

    if tiffs:
        upload_dir = folder / "_IA"
        upload_dir.mkdir()

        if delete and jpegs:
            for j in jpegs:
                print(f'deleting jpeg {str(j)}')
                os.remove(j)

        for tiff in tiffs:
            subprocess.run(["magick", "mogrify", "-quiet", "-density", "300", "-format", "jpg", f'{str(tiff)}'])

        zip_folder = folder / "raw.zip"
        with ZipFile(zip_folder, "w", compression=ZIP_DEFLATED) as raw:
            for tiff in tiffs:
                raw.write(tiff, arcname=tiff.name)

        jpegs = get_jpegs(folder)
        for jpeg in jpegs:
            shutil.move(str(jpeg), str(upload_dir / jpeg.name))

        shutil.move(str(zip_folder), str(upload_dir / zip_folder.name))

    for sub in subs:
        navigate(sub, delete)

def process(base: str, delete: bool):
    base_path = Path(base)
    print(f'Base is {str(base_path)}, {"DELETING" if delete else "NOT deleting"} existing JPEGs')
    navigate(base_path, delete)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base", help="Path to base folder that will be recursively searched for TIFFs")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete existing JPEGs")
    args = parser.parse_args()
    process(args.base, args.delete)
