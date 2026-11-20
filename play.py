import argparse

import pygame

from helpers import get_list_of_midi_files

args = argparse.ArgumentParser()

group = args.add_mutually_exclusive_group(required=True)

group.add_argument(
    "-f",
    "--file",
    help="path for the single midi file to play",
)

args.add_argument("-d", "--dir", help="path for the folder of midi files to play")

args = args.parse_args()


def play_midi(filename: str):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(30)


pygame.init()

if args.file:
    paths = [args.file]
else:
    paths = get_list_of_midi_files(args.dir)

for midi_file in paths:
    play_midi(midi_file)
