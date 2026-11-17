from pathlib import Path

from music21 import chord, converter, note


def get_notes(path: str = "input"):
    """Get all the notes and chords from the midi files"""
    notes = []

    for file in Path(path).glob("*.mid"):
        midi = converter.parse(file)

        print(f"Parsing {file}")

        notes_to_parse = midi.flat.notesq

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    return notes
