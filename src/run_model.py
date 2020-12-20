import torch
import torchaudio
import matplotlib.pyplot as plt
import os
from mido import MidiFile
import glob
# torchaudio.USE_SOUNDFILE_LEGACY_INTERFACE = False
# torchaudio.set_audio_backend("soundfile")
from music21 import converter, instrument, note, chord


def remove_duplicate_tracks(filepath):
    cv1 = MidiFile(filepath, clip=True)
    message_numbers = []
    duplicates = []

    for track in cv1.tracks:
        if len(track) in message_numbers:
            duplicates.append(track)
        else:
            message_numbers.append(len(track))

    for track in duplicates:
        cv1.tracks.remove(track)

    cv1.save("clean_" + filepath)


if __name__ == '__main__':
    # remove_duplicate_tracks("mz_311_1.mid")

    notes = []
    for file in glob.glob("../data/processed/*.mid"):
        midi = converter.parse(file)
        notes_to_parse = None
        parts = instrument.partitionByInstrument(midi)
        for part in parts.parts:
            print(part)
        if parts:  # file has instrument parts
            notes_to_parse = parts.parts[0].recurse()
        else:  # file has notes in a flat structure
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    print(notes)
