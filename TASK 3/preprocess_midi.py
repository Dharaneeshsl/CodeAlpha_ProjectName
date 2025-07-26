import os
import pickle
from music21 import converter, instrument, note, chord

midi_folders = ['TASK 3/midi_data', 'TASK 3']
notes = []

midi_files = []
for folder in midi_folders:
    if os.path.exists(folder):
        midi_files += [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.mid', '.midi'))]

if not midi_files:
    print("No MIDI files found in the folders.")
    exit(1)

for file_path in midi_files:
    print(f"Processing {file_path}")
    try:
        midi = converter.parse(file_path)
        parts = instrument.partitionByInstrument(midi)
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

with open('TASK 3/notes.pkl', 'wb') as f:
    pickle.dump(notes, f)
print(f"Extracted {len(notes)} notes/chords. Saved to TASK 3/notes.pkl") 