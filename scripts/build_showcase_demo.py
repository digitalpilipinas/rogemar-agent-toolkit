#!/usr/bin/env python3
"""Assemble a non-looping README GIF from check_showcase.cjs captures (Pillow required)."""
from pathlib import Path
import argparse
from PIL import Image


def build(source, destination):
    frames=[]
    for i in range(7):
        with Image.open(source / f'frame-{i}.png') as image:
            frames.append(image.convert('RGB').quantize(colors=128))
    frames[0].save(destination,save_all=True,append_images=frames[1:],duration=[550]*6+[1000],optimize=True,disposal=2)
    with Image.open(destination) as gif:
        assert gif.n_frames == 7 and 'loop' not in gif.info


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('captures',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();build(args.captures,args.output)
