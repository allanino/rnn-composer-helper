#!/usr/bin/env python
import argparse
import os
import subprocess
import ntpath

def save_to_svg(abc_file, output_dir):
    out_file = os.path.join(output_dir, ntpath.basename(abc_file).split('.')[0] + '.svg')
    subprocess.call(['abcm2ps', '-g', abc_file, '-O', out_file])
    os.rename(os.path.join(output_dir, ntpath.basename(abc_file).split('.')[0] + '001.svg'), out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', '-o', help='Directory to output files.')
    parser.add_argument('--start-index', '-s', type=int, default=1,
        help="Start index when converting files in directory. If -s=3, convert from third file on.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--input-file', '-i',
        help='ABC file to be rendered.')
    group.add_argument('--dir', '-d',
        help='Directory with ABC files to be converted.')
    args = parser.parse_args()

    if args.output_dir:
        output_dir = args.output_dir
        try:
            os.mkdir(output_dir)
        except OSError:
            pass
    else:
        if args.dir:
            output_dir = args.dir
            try:
                os.mkdir(output_dir)
            except OSError:
                pass
        else:
            output_dir = os.path.dirname(args.input_file)

    if args.input_file:
        save_to_svg(args.input_file, output_dir)
    else:
        files = os.listdir(args.dir)
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for file in files[args.start_index:]:
            if '.abc' in file:
                f = os.path.join(args.dir, file)
                save_to_svg(f, output_dir)
