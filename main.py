from io import BytesIO
from pathlib import Path

from music21 import midi
from pygame import mixer

from helpers.helpers import get_notes, play_midi_bytes
from trainer.train_generator import GAN
from trainer.use_generator import create_midi, generate_music

LATENT_DIMENSION = 1000

MIXER_FREQ = 44100
MIXER_BIT_SIZE = -16
MIXER_CHANNELS = 2
MIXER_BUFFER = 1024

BATCH_SIZE = 24

INPUT_PATH = "input"

notes = get_notes(INPUT_PATH)
n_vocab = len(set(notes))

mixer.init(MIXER_FREQ, MIXER_BIT_SIZE, MIXER_CHANNELS, MIXER_BUFFER)

# Train a GAN on the midi files once
gan = GAN()
gan.train(notes=notes, n_vocab=n_vocab, batch_size=BATCH_SIZE)

while True:

    # Get a midi sequence from the generator
    generated_music = generate_music(gan.generator, LATENT_DIMENSION, notes, n_vocab)

    # Convert midi output to bytes
    midi_stream = midi.translate.streamToMidiFile(create_midi(generated_music))
    midi_bytes = BytesIO(midi_stream.writestr())

    # play the output
    play_midi_bytes(midi_bytes)
