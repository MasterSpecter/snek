#!/usr/bin/env python3

from pathlib import Path
import argparse
import os
from zipfile import ZipFile
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
    print(subs)
    jpegs = get_jpegs(folder)
    print(jpegs)
    tiffs = get_tiffs(folder)
    print(tiffs)
    print(f'working in folder {str(folder)}')

    if tiffs:
        upload_dir = folder / "_IA"
        upload_dir.mkdir()

        if delete and jpegs:
            for j in jpegs:
                print(f'deleting jpeg {str(j)}')
                os.remove(str(j))

        for tiff in tiffs:
            subprocess.run(["magick", "mogrify", "-quiet", "-density", "300", "-format", "jpg", f'{str(tiff)}'])

        zip_folder = folder / "raw.zip"
        with ZipFile(zip_folder, "w") as raw:
            for tiff in tiffs:
                print(f'writing tiff {str(tiff)} to {str(zip_folder)}')
                raw.write(tiff)

        jpegs = get_jpegs(folder)
        for jpeg in jpegs:
            shutil.move(str(jpeg), str(upload_dir / jpeg.name))

        shutil.move(str(zip_folder), str(upload_dir / zip_folder.name))

    for sub in subs:
        navigate(sub, delete)

def process(base: str, delete: bool):
    base_path = Path(base)
    print(f'Base is {str(base_path)}')
    navigate(base_path, delete)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base", help="Path to base folder that will be recursively searched for TIFFs")
    parser.add_argument("-d", "--delete", action="store_true", help="Delete existing JPEGs")
    args = parser.parse_args()
    process(args.base, args.delete)
