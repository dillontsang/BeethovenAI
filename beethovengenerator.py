'''
Created on Aug 18, 2023

@author: dillontsang
'''
import json
import numpy as np
import tensorflow.keras as keras
import music21 as m21
from beethovenchordprogressionpreprocess import SEQUENCE_LENGTH, MAPPING_PATH
from pickle import NONE

class ChordProgressionGenerator:
    
    def __init__(self, model_path="beethovenodel.h5"):
        
        self.model_path = model_path
        self.model = keras.models.load_model(model_path)
        
        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)
            
        self._start_symbols = ["/"] * SEQUENCE_LENGTH
        
    def generate_chord_progression(self, seed, num_steps, max_sequence_length, temperature):
        # "64 _ 63 _ _ "
        
        # create seed with start symbol
        seed = seed.split()
        chordProgression = seed
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
            chordProgression.append(output_symbol)
            
        return chordProgression
            
            
    def _sample_with_temperature(self, probabilities, temperature):
        
        # temperature -> infinity
        # temperature -> 0 more rigid
        # temperature = 1
            
        predictions = np.log(probabilities) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))
            
        choices = range(len(probabilities)) # [0, 1, 2, 3]
        index = np.random.choice(choices, p = probabilities)
            
        return index
    
        
if __name__ == "__main__":
    cpg = ChordProgressionGenerator()
    seed = "I _ _ _ V65/vi _ _ _ vi _ _ _ V43/V _ _ _ V _ _ _ V7 _ V42 _ I6 _ _ _ IV _ vii=7/V _ I64 _ _ _ V _ _ _ I _ _ _"
    
    chordProgression = cpg.generate_chord_progression(seed, num_steps, max_sequence_length, temperature)(seed, 500, SEQUENCE_LENGTH, 1)
    print(chordProgression)      