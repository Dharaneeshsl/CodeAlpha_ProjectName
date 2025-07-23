import pickle
import numpy as np
from keras.models import load_model
from music21 import instrument, note, stream, chord

# Load data
with open('notes.pkl', 'rb') as f:
    notes = pickle.load(f)
pitches = sorted(set(notes))
n_vocab = len(pitches)
note_to_int = {note: num for num, note in enumerate(pitches)}
int_to_note = {num: note for note, num in note_to_int.items()}

# Prepare input
sequence_length = 20
network_input = []
for i in range(0, len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    network_input.append([note_to_int[n] for n in seq_in])

if not network_input:
    print("Not enough data to generate music.")
    exit(1)

# Pick a random seed
start = np.random.randint(0, len(network_input)-1)
pattern = network_input[start]

# Load model
model = load_model('music_model.h5')

# Generate notes
output_notes = []
for note_index in range(50):
    prediction_input = np.reshape(pattern, (1, sequence_length, 1)) / float(n_vocab)
    prediction = model.predict(prediction_input, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]
    output_notes.append(result)
    pattern.append(index)
    pattern = pattern[1:]

# Convert to MIDI
offset = 0
output_stream = stream.Stream()
for item in output_notes:
    if ('.' in item) or item.isdigit():
        notes_in_chord = item.split('.')
        notes_objs = [note.Note(int(n)) for n in notes_in_chord]
        new_chord = chord.Chord(notes_objs)
        new_chord.offset = offset
        output_stream.append(new_chord)
    else:
        new_note = note.Note(item)
        new_note.offset = offset
        output_stream.append(new_note)
    offset += 0.5
output_stream.write('midi', fp='generated_music.mid')
print('Generated music saved to generated_music.mid') 