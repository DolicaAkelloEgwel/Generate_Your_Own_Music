from pathlib import Path

import pygame
from music21 import chord, converter, midi, note


def get_notes(input_path: str):
    """Get all the notes and chords from the midi files"""
    notes = []

    for file in Path(input_path).glob("*.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    return notes


def play_midi_bytes(
    string_io_file,
    busy_wait_milliseconds=50,
    play_for_milliseconds=float("inf"),
    blocked=True,
):

    pygame_clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(string_io_file)
    except Exception as e:
        print(e, "Couldn't open file...")
        exit()

    pygame.mixer.music.play()
    if not blocked:
        return

    framerate = int(
        1000 / busy_wait_milliseconds
    )  # coerce into int even if given a float.
    start_time = pygame.time.get_ticks()

    while pygame.mixer.music.get_busy():
        if pygame.time.get_ticks() - start_time > play_for_milliseconds:
            pygame.mixer.music.stop()
            break
        pygame_clock.tick(framerate)
