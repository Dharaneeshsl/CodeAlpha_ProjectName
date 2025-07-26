import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint

with open('TASK 3/notes.pkl', 'rb') as f:
    notes = pickle.load(f)

pitches = sorted(set(notes))
n_vocab = len(pitches)

note_to_int = {note: num for num, note in enumerate(pitches)}

sequence_length = 20
network_input = []
network_output = []
for i in range(0, len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    network_input.append([note_to_int[n] for n in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)
if n_patterns == 0:
    print("Not enough data to train. Add more MIDI files or use a smaller sequence length.")
    exit(1)

network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
network_input = network_input / float(n_vocab)
network_output = to_categorical(network_output, num_classes=n_vocab)

model = Sequential()
model.add(LSTM(128, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(128))
model.add(Dropout(0.3))
model.add(Dense(n_vocab, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

filepath = 'TASK 3/music_model.h5'
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')

model.fit(network_input, network_output, epochs=30, batch_size=32, callbacks=[checkpoint])
print('Model trained and saved to', filepath) 