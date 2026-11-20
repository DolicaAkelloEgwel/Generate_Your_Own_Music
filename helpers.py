from pathlib import Path

from music21 import chord, converter, note


def get_list_of_midi_files(path: str) -> list[str]:
    return Path(path).glob("*.mid")


def get_notes(path: str) -> list[str]:
    """Get all the notes and chords from the midi files"""
    notes = []

    for midi_file in get_list_of_midi_files(path):
        midi = converter.parse(midi_file)
        print(f"Parsing {midi_file}")

        notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append(".".join(str(n) for n in element.normalOrder))

    return notes
