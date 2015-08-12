#!/usr/bin/env python
import argparse
import os
import subprocess
import ntpath

def save_to_mp3(midi_file, soundfont, output_dir):
    subprocess.call(['fluidsynth', '-l', '-i', '-a', 'file', '-z', '2048',
        soundfont, midi_file])
    out_file = os.path.join(output_dir, ntpath.basename(midi_file).split('.')[0] + '.mp3')
    subprocess.call(['avconv', '-vol', '320', '-y', '-i', 'fluidsynth.wav', out_file])
    os.remove('fluidsynth.wav')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('soundfont',
        help='Soundfont to use.')
    parser.add_argument('--output-dir', '-o', help='Directory to output files.')
    parser.add_argument('--start-index', '-s', type=int, default=1,
        help="Start index when converting files in directory. If -s=3, convert from third file on.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--input-file', '-i',
        help='MIDI file to be converted.')
    group.add_argument('--dir', '-d',
        help='Directory with MIDI files to be converted.')
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
        save_to_mp3(args.input_file, args.soundfont, output_dir)
    else:
        files = os.listdir(args.dir)
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        for file in files[args.start_index:]:
            if '.mid' in file:
                f = os.path.join(args.dir, file)
                save_to_mp3(f, args.soundfont, output_dir)
