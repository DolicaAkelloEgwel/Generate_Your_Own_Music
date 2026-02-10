from create_generator_model import GAN
from generate_music import generate_music
from pathlib import Path
from music21 import converter, note, chord

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


if __name__ == "__main__":

    notes = get_notes()
    n_vocab = len(set(notes))

    gan = GAN()
    gan.train(notes=notes, n_vocab=n_vocab, batch_size=24)

    # Save the generator and discriminator models
    # gan.generator.save("generator_model.h5")
    # gan.discriminator.save("discriminator_model.h5")

    generated_music = generate_music(gan.generator, LATENT_DIMENSION, notes, n_vocab)
