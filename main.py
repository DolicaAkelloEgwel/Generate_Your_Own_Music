from io import BytesIO
from pathlib import Path

import pygame
from music21 import chord, converter, midi, note

from trainer.train_generator import GAN
from trainer.generate_music import create_midi, generate_music

LATENT_DIMENSION = 1000

MIXER_FREQ = 44100
MIXER_BIT_SIZE = -16
MIXER_CHANNELS = 2
MIXER_BUFFER = 1024

BATCH_SIZE = 24

INPUT_PATH = "input"


def get_notes():
    """Get all the notes and chords from the midi files"""
    notes = []

    for file in Path(INPUT_PATH).glob("*.mid"):
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


if __name__ == "__main__":

    notes = get_notes()
    n_vocab = len(set(notes))

    pygame.mixer.init(MIXER_FREQ, MIXER_BIT_SIZE, MIXER_CHANNELS, MIXER_BUFFER)

    # Train a GAN on the midi files once
    gan = GAN()
    gan.train(notes=notes, n_vocab=n_vocab, batch_size=BATCH_SIZE)

    while True:

        # Get a midi sequence from the generator
        generated_music = generate_music(
            gan.generator, LATENT_DIMENSION, notes, n_vocab
        )

        # Convert midi output to bytes
        midi_stream = midi.translate.streamToMidiFile(create_midi(generated_music))
        midi_bytes = BytesIO(midi_stream.writestr())

        # play the output
        play_midi_bytes(midi_bytes)
