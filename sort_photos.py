#! /usr/bin/env python3

import os
import argparse
import itertools
import shutil
import re
from pathlib import Path

parser = argparse.ArgumentParser(description='Move JPGs from source to dest renaming parent directory in dest based on EXIF date')
parser.add_argument('-s', '--source', required=True, help='Source directory')
parser.add_argument('-d', '--dest', required=True, help='Destation directory')
parser.add_argument('--dry-run', action='store_true', default=False, help='Dry run')
args = parser.parse_args()

import PIL.Image
import PIL.ExifTags

exif_dt_tag = list(PIL.ExifTags.TAGS.keys())[ list(PIL.ExifTags.TAGS.values()).index("DateTime") ]

for p in itertools.chain(Path(args.source).rglob('*.JPG'), Path(args.source).rglob('*.jpg'), Path(args.source).rglob('*.jpeg')):

    img = PIL.Image.open(p)
    exif_data = img._getexif()

    if exif_dt_tag in exif_data:

        # not sure if you can set the datetime delimiters to something other than colon (:)
        year, month, day, hour, minute, seconds = re.match(r"(\d\d\d\d):(\d\d):(\d\d) (\d\d):(\d\d):(\d\d)", exif_data[exif_dt_tag]).groups()

        dest_dir = Path(args.dest) / ("%s-%02d-%02d" % (year, int(month), int(day)))
        if args.dry_run:
            print("Would move %s => %s" % (p, dest_dir / p.name))
        else:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(p, dest_dir / p.name)

