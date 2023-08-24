'''
Created on Aug 3, 2023

@author: dillontsang
'''
import json
import numpy as np
import tensorflow.keras as keras
import music21 as m21
import random
from preprocess import SEQUENCE_LENGTH, MAPPING_PATH
from pickle import NONE

class MelodyGenerator:
    
    def __init__(self, model_path="model.h5"):
        
        self.model_path = model_path
        self.model = keras.models.load_model(model_path)
        
        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)
            
        self._start_symbols = ["/"] * SEQUENCE_LENGTH
        
    def generate_melody(self, seed, num_steps, max_sequence_length, temperature):
        # "64 _ 63 _ _ "
        
        # create seed with start symbol
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed
        
        # map seed to int
        seed = [self._mappings[symbol] for symbol in seed]
        
        for _ in range(num_steps):
            
            # limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]
            
            # one-hot encode the seed
            onehot_seed = keras.utils.to_categorical(seed, num_classes = len(self._mappings))
            # (1, max_sequence_length, num of symbols in the vocabulary)
            onehot_seed = onehot_seed[np.newaxis, ...]
            
            # make a prediction
            probabilities = self.model.predict(onehot_seed)[0]
            # [0.1, 0.2, 0.1, 0.6] -> 1
            
            output_int = self._sample_with_temperature(probabilities, temperature)
            
            # update seed
            seed.append(output_int)
            
            # map int to our encoding
            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]
            
            # check whether we're at the end of a melody
            if output_symbol == "/":
                break
            
            # update the melody
            melody.append(output_symbol)
            
        return melody
    
    def generate_melody_to_match_chord_progression(self, seed, max_sequence_length, quarter_length_duration, soprano_choices, temperature):
        # "64 _ 63 _ _ "
        
        # create seed with start symbol
        # print(seed)
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed
        steps = quarter_length_duration * 4
        step = 0
        
        # map seed to int
        seed = [self._mappings[symbol] for symbol in seed]
        
        for step in range(steps):
            
            # limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]
            
            # one-hot encode the seed
            onehot_seed = keras.utils.to_categorical(seed, num_classes = len(self._mappings))
            # (1, max_sequence_length, num of symbols in the vocabulary)
            onehot_seed = onehot_seed[np.newaxis, ...]
            
            probabilities = self.model.predict(onehot_seed)[0]
            
            # make a prediction
            if step != 0:
                output_int = self._sample_with_temperature(probabilities, temperature)
                # [0.1, 0.2, 0.1, 0.6] -> 1
            else: 
                # align melody with chord progression
                output_int = self._sample_with_soprano_choices(probabilities, soprano_choices)
            
            # update seed
            seed.append(output_int)
            
            # map int to our encoding
            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]
            
            # check whether we're at the end of a melody
            if output_symbol == "/":
                break
            
            # update the melody
            melody.append(output_symbol)
            
        cut_melody = melody[-steps:]
        
        soprano_note = int(cut_melody[0])
        
        return cut_melody, soprano_note
    
    def _sample_with_soprano_choices(self, probabilities, soprano_choices):
        
        # takes valid soprano options, picks whichever one the AI favors the most
        
        soprano_choices_string = list(map(str, soprano_choices))
        
        soprano_choices_mapped = [self._mappings[note] for note in soprano_choices_string]
        
        highest_index = soprano_choices_mapped[0]
        highest_value = probabilities[highest_index]
        
        for index in soprano_choices_mapped:
            if index >= len(probabilities):
                continue  # Skip invalid indexes
        
            num = probabilities[index]
            if num > highest_value:
                highest_value = num
                highest_index = index
            
        return highest_index
        
            
            
    def _sample_with_temperature(self, probabilities, temperature):
        
        # temperature -> infinity
        # temperature -> 0 more rigid
        # temperature = 1
            
        predictions = np.log(probabilities) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))
            
        choices = range(len(probabilities))
        
        index = np.random.choice(choices, p = probabilities)
        index_symbol = [k for k, v in self._mappings.items() if v == index][0]
        
        chances = 0
        
        # make sure doesnt return / because / signals end of piece
        while index_symbol == "/":
            index = np.random.choice(choices, p = probabilities)
            index_symbol = [k for k, v in self._mappings.items() if v == index][0]
            chances += 1
            
            if (chances >= 50):
                # choose most probable c major note
                c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79]
                scale_string = list(map(str, c_major_scale))
                scale_mapped = [self._mappings[note] for note in scale_string]
                
                highest_index = scale_mapped[0]
                highest_value = probabilities[highest_index]
                
                for scale_note in scale_mapped:
                    if scale_note >= len(probabilities):
                        continue  # Skip invalid indexes
        
                    num = probabilities[scale_note]
                    if num > highest_value:
                        highest_value = num
                        highest_index = scale_note
            
                index = highest_index
                index_symbol = [k for k, v in self._mappings.items() if v == index][0]
                
        return index
    
        
    def save_melody(self, melody, step_duration = 0.25, format = "mid", file_name = "mel.midi"):
        
        # create a music21 stream
        stream = m21.stream.Stream()
        
        # parse all the symbols in the melody and create note/rest objects
        # 60 _ _ _ r _ 62 _
        start_symbol = None
        step_counter = 1
        
        for i, symbol in enumerate(melody):
            
            # handle case in which we have a note/rest
            if symbol != "_" or i + 1 == len(melody):
                
                # ensure we're not dealing with note/rest beyond the first symbol
                if start_symbol is not None:
                    
                    quarter_length_duration = step_duration * step_counter # 0.25 * 4
                    
                    # handle rest
                    if start_symbol == "r":
                        m21_event = m21.note.Rest(quarterLength = quarter_length_duration)
                    
                    # handle note
                    else:
                        m21_event = m21.note.Note(int(start_symbol), quarterLength = quarter_length_duration)
                    
                    stream.append(m21_event)
                    
                    # reset step counter
                    step_counter = 1
                    
                start_symbol = symbol
            
            # handle case in which we have a prolongation sign "_"
            else:
                step_counter += 1
            
        # write the m21 stream to a midi file
        stream.write(format, file_name)
        
if __name__ == "__main__":
    mg = MelodyGenerator()
    seed = "60 _ 64 _ _ 65 64 _ 60 _ 64 _" # 205
    
    # melody = mg.generate_melody(seedtest, 500, SEQUENCE_LENGTH, 0.4)
    # print(melody)
    # mg.save_melody(melody)        
            
            
            
            
            
            
            