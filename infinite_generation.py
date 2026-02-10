from io import BytesIO
from pathlib import Path

import pygame
from music21 import chord, converter, midi, note

from create_generator_model import GAN
from generate_music import create_midi, generate_music

LATENT_DIMENSION = 1000


def get_notes():
    """Get all the notes and chords from the midi files"""
    notes = []

    for file in Path("input").glob("*.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    return notes


def play_midi_stream(
    stringIOFile,
    busyWaitMilliseconds=50,
    playForMilliseconds=float("inf"),
    blocked=True,
):

    pygameClock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(stringIOFile)
    except Exception as e:
        print(e, "Couldn't open file...")
        exit()

    pygame.mixer.music.play()
    if not blocked:
        return

    framerate = int(
        1000 / busyWaitMilliseconds
    )  # coerce into int even if given a float.
    start_time = pygame.time.get_ticks()

    while pygame.mixer.music.get_busy():
        if pygame.time.get_ticks() - start_time > playForMilliseconds:
            pygame.mixer.music.stop()
            break
        pygameClock.tick(framerate)


if __name__ == "__main__":

    notes = get_notes()
    n_vocab = len(set(notes))

    mixerFreq: int = 44100
    mixerBitSize: int = -16
    mixerChannels: int = 2
    mixerBuffer: int = 1024

    pygame.mixer.init(mixerFreq, mixerBitSize, mixerChannels, mixerBuffer)

    gan = GAN()
    gan.train(notes=notes, n_vocab=n_vocab, batch_size=24)

    while True:

        generated_music = generate_music(
            gan.generator, LATENT_DIMENSION, notes, n_vocab
        )
        midi_stream = create_midi(generated_music)

        streamMidiFile = midi.translate.streamToMidiFile(midi_stream)
        midi_bytes = BytesIO(streamMidiFile.writestr())

        play_midi_stream(midi_bytes)
