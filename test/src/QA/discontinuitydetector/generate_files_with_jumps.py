#!/usr/bin/env python

# Copyright (C) 2006-2018  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/


import os

import numpy as np

import essentia.standard as es
from essentia import array as esarr


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if basename.lower().endswith(pattern):
                filename = os.path.join(root, basename)
                yield filename


if __name__ == '__main__':
    """
    This script find all the files in a folder, tries to open
    them as audio files, removes some samples in order to 
    generate a jump and ens and saves them in a desired folder
    """

    in_folder = '../../audio/recorded'
    out_folder = '../../QA-audio/Jumps/'
    fs = 44100.
    files = [x for x in find_files(in_folder, 'wav')]

    for f in files:
        try:
            audio = es.MonoLoader(filename=f, sampleRate=fs)()
        except Exception:
            print('{} was not loaded'.format(f))
            continue

        original_len = len(audio)

        start_jump = original_len // 4

        end_jump = start_jump + int(np.abs(np.random.randn()) * fs)

        audio = np.hstack([audio[:start_jump], audio[end_jump:]])

        text = ['{}\t0.0\tevent\n'.format(start_jump / float(fs))]

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        f_name = ''.join(os.path.basename(f).split('.')[:-1])
        with open('{}/{}_jump.lab'.format(out_folder, f_name), 'w') as o_file:
            o_file.write(''.join(text))

        es.MonoWriter(filename='{}/{}_jump.wav'.format(out_folder, f_name))(esarr(audio))
