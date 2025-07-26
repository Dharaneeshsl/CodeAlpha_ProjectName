import pickle
import numpy as np
import argparse
import os
from keras.models import load_model
from music21 import instrument, note, stream, chord
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_music_data():
    try:
        with open('notes.pkl', 'rb') as f:
            notes = pickle.load(f)
        
        pitches = sorted(set(notes))
        n_vocab = len(pitches)
        note_to_int = {note: num for num, note in enumerate(pitches)}
        int_to_note = {num: note for note, num in note_to_int.items()}
        
        sequence_length = 20
        network_input = []
        for i in range(0, len(notes) - sequence_length):
            seq_in = notes[i:i + sequence_length]
            network_input.append([note_to_int[n] for n in seq_in])
        
        if not network_input:
            raise ValueError("Not enough data to generate music.")
        
        model = load_model('music_model.h5')
        
        return model, network_input, note_to_int, int_to_note, n_vocab, sequence_length
        
    except Exception as e:
        logger.error(f"Error loading music data: {e}")
        raise

def generate_music_sequence(model, network_input, note_to_int, int_to_note, n_vocab, sequence_length, 
                          num_notes=50, temperature=0.7, style='default'):
    try:
        if style == 'classical':
            start = np.random.randint(0, len(network_input)//2)
        elif style == 'jazz':
            start = np.random.randint(len(network_input)//4, len(network_input)-1)
        else:
            start = np.random.randint(0, len(network_input)-1)
        
        pattern = network_input[start]
        output_notes = []
        
        if style == 'ambient':
            note_duration = 1.0
        elif style == 'rock':
            note_duration = 0.25
        else:
            note_duration = 0.5
        
        for note_index in range(num_notes):
            prediction_input = np.reshape(pattern, (1, sequence_length, 1)) / float(n_vocab)
            prediction = model.predict(prediction_input, verbose=0)
            
            if temperature != 1.0:
                prediction = np.log(prediction) / temperature
                prediction = np.exp(prediction)
                prediction = prediction / np.sum(prediction)
            
            if style == 'jazz' and note_index % 4 == 0:
                indices = np.argsort(prediction[0])[-3:]
            else:
                index = np.argmax(prediction)
                indices = [index]
            
            for idx in indices:
                result = int_to_note[idx]
                output_notes.append((result, note_duration))
            
            pattern.append(indices[0])
            pattern = pattern[1:]
        
        return output_notes
        
    except Exception as e:
        logger.error(f"Error generating music sequence: {e}")
        raise

def create_midi_stream(output_notes, style='default'):
    try:
        output_stream = stream.Stream()
        
        if style == 'classical':
            output_stream.append(instrument.Piano())
        elif style == 'jazz':
            output_stream.append(instrument.Piano())
        elif style == 'rock':
            output_stream.append(instrument.ElectricGuitar())
        elif style == 'ambient':
            output_stream.append(instrument.Synthesizer())
        else:
            output_stream.append(instrument.Piano())
        
        offset = 0
        for item, duration in output_notes:
            if ('.' in item) or item.isdigit():
                notes_in_chord = item.split('.')
                notes_objs = [note.Note(int(n)) for n in notes_in_chord]
                new_chord = chord.Chord(notes_objs)
                new_chord.offset = offset
                new_chord.duration.quarterLength = duration
                output_stream.append(new_chord)
            else:
                new_note = note.Note(item)
                new_note.offset = offset
                new_note.duration.quarterLength = duration
                output_stream.append(new_note)
            offset += duration
        
        return output_stream
        
    except Exception as e:
        logger.error(f"Error creating MIDI stream: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Generate MIDI music using LSTM model')
    parser.add_argument('--style', default='default', choices=['classical', 'jazz', 'pop', 'ambient', 'rock', 'default'],
                       help='Music style to generate')
    parser.add_argument('--length', type=int, default=50, help='Number of notes to generate')
    parser.add_argument('--temperature', type=float, default=0.7, help='Creativity temperature (0.1-2.0)')
    parser.add_argument('--output', default='generated_music.mid', help='Output MIDI filename')
    
    args = parser.parse_args()
    
    try:
        logger.info(f"Generating {args.style} music with {args.length} notes...")
        
        model, network_input, note_to_int, int_to_note, n_vocab, sequence_length = load_music_data()
        
        output_notes = generate_music_sequence(
            model, network_input, note_to_int, int_to_note, n_vocab, sequence_length,
            num_notes=args.length, temperature=args.temperature, style=args.style
        )
        
        output_stream = create_midi_stream(output_notes, args.style)
        
        output_stream.write('midi', fp=args.output)
        logger.info(f"Generated music saved to {args.output}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        return False

if __name__ == '__main__':
    success = main()
    if not success:
        exit(1) 