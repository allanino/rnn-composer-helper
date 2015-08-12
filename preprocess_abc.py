#!/usr/bin/env python
import re
import argparse
import os
import random

parser = argparse.ArgumentParser()
parser.add_argument('dirs', nargs='*',
    help='Directories with abc files.')
parser.add_argument('--output_file', '-o', required=True,
    help='File to ouput results.')
parser.add_argument('--recursive', '-r', action='store_true',
    help='Look folders recursively.')
parser.add_argument('--shuffle', '-s', action='store_true',
    help='Shuffle resulting dataset.')
parser.add_argument('--keep_title', '-t', action='store_true',
    help='Keep tunes titles when processing files.')
args = parser.parse_args()

def process_folder(dir_path, data=[]):
    """ Concatenate all lines from all files in dir_path and return a list. """
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)]

    for file in files:
        if file.split('.')[-1] == 'abc': # Only open abc files
            with open(file, 'r') as f:
                lines = f.readlines()
                # Skip header info
                i = 0
                init = lines[i][0:2]
                while init != 'X:':
                    i += 1
                    try:
                        init = lines[i][0:2]
                    except:
                        i -= 1
                        break
                data += lines[i:]

    return data

# Get a list with all lines from all files
data = []
for directory in args.dirs:
    data = process_folder(directory, data)
    if args.recursive:
        sub_dirs = [x[0] for x in os.walk(directory)]
        for dir_path in sub_dirs:
            data = process_folder(dir_path, data)

pattern = re.compile('^([A-Za-z]):')

fields_to_keep = ['Q', 'M', 'L', 'K', 'X', 'P']
if args.keep_title:
    fields_to_keep.append('T')

# Process all lines to create a big string with ABC tunes
res = ''
for l in data:
    p = pattern.match(l)
    if pattern.match(l):
        c = p.group(1)
        if c in fields_to_keep:
            if c == 'X':
                res += '\n\n'
                continue
            if c == 'P' and res[-1] == '|' or res[-1] == '\\':
                res += '\n'
            res += l
    else:
        if l[0] != '%': # Ignore comment line
            # Strip spaces and newlines
            res += l.replace(' ', '')

# Shuffle the tunes (not the individual lines)
if args.shuffle:
    musics = res.split('\n\n')
    random.shuffle(musics)
    res = ''
    for m in musics:
        if len(m) > 2: # HACK: test if it's really a music
            res += m.rstrip().lstrip() + '\n\n'

with open(args.output_file, 'w') as f:
    f.write(res)
