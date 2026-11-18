import argparse

import pygame

args = argparse.ArgumentParser()

args.add_argument(
    "-f",
    "--file",
    required=True,
    help="path for the midi file to play",
)

args = args.parse_args()


def play_midi(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(30)


pygame.init()
play_midi(args.file)
