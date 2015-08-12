#!/usr/bin/env python
import os
import tempfile
import subprocess
import argparse
import shutil

def generate_midi(abc_file, midi_file, keep_warn=False, keep_error=False):
    """ Save abc_file to midi_file. """
    try:
        res = subprocess.check_output(['abc2midi', abc_file, '-o', midi_file])
    except subprocess.CalledProcessError:
        return False

    if 'Error in line' in res:
        if keep_error:
            os.rename(midi_file, midi_file.split('.')[0] + '_error.mid')
        else:
            try:
                os.remove(midi_file)
            except:
                pass
            return False
    elif 'Warning in line' in res:
        # See if is like this and keep it if so
        # Warning in line 10 : Assuming repeat
        # writing MIDI file data/musics_2_new/156.mid
        #
        res_lines = res.split('\n')
        if 'Assuming repeat' in res_lines[0] and len(res.split('\n')) == 3:
            return True
        if keep_warn:
            try:
                os.rename(midi_file, midi_file.split('.')[0] + '_warn.mid')
            except OSError:
                return False
        else:
            try:
                os.remove(midi_file)
            except:
                pass
            return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('abc-file',
        help='File with abc musics to be converted to MIDI.')
    parser.add_argument('output-dir',
        help='DIrectory to ouput results.')
    parser.add_argument('--error', '-e', action="store_true",
        help='Keep MIDI files with errors on conversion.')
    parser.add_argument('--warn', '-w', action="store_true",
        help='Keep MIDI files with warnings on conversion.')
    parser.add_argument('--min-size', '-m', default=0, type=int,
        help='Keep only MIDI larger than min-size bytes.')
    args = parser.parse_args()

    # Get musics from abc_file
    with open(args.abc_file, 'r') as f:
        lines = f.readlines()
        musics = ['']
        for l in lines:
            if l == '\n':
                musics.append('')
            else:
                musics[-1] += l

    # Ignore first one, as it's just message from Torch
    musics = musics[1:]

    musics_dir = os.path.join(args.output_dir, 'mid')
    try:
        shutil.rmtree(musics_dir)
    except OSError:
        pass
    os.mkdir(musics_dir)

    abc_dir = os.path.join(args.output_dir, 'abc')
    try:
        shutil.rmtree(abc_dir)
    except OSError:
        pass
    os.mkdir(abc_dir)

    # Generate MIDIs
    c = 1
    for m in musics:
        abc_file = os.path.join(abc_dir, '%d.abc' % c)
        with open(abc_file, 'w') as f:
            m = 'X:%d\n' % c + m
            f.write(m)
            f.seek(0)
            midi_file = os.path.join(musics_dir, '%d.mid' % c)
            success = generate_midi(abc_file, midi_file,
                        keep_warn=args.warn, keep_error=args.error)
            if not success:
                os.remove(abc_file)
            else:
                if not os.path.isfile(midi_file):
                    if os.path.isfile(midi_file.split('.')[0] + '_error.mid'):
                        midi_file = midi_file.split('.')[0] + '_error.mid'
                    elif os.path.isfile(midi_file.split('.')[0] + '_warn.mid'):
                        midi_file = midi_file.split('.')[0] + '_warn.mid'
                    else:
                        os.remove(abc_file)
                        continue
                if os.path.getsize(midi_file) < args.min_size:
                    os.remove(abc_file)
                    os.remove(midi_file)
                else:
                    c += 1
