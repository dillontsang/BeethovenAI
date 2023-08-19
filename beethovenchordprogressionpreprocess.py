'''
Created on Aug 18, 2023

@author: dillontsang
'''
'''
Created on Jul 31, 2023

@author: dillontsang
'''
import os
import json
import music21 as m21
import numpy as np
import tensorflow.keras as keras
import csv

CSV_DATASET_PATH = "beethovenchorddataset"
SAVE_DIR = "beethoven_chord_progression_dataset"
# SINGLE_FILE_DATASET = "file_beethoven_chord_progression_dataset"
MAPPING_PATH = "beethovenchordmapping.json"
SEQUENCE_LENGTH = 16


def load_songs_in_csv(dataset_path):
    
    chords = []
    measures = []
    
    # go through all the files in dataset and load chords and measures
    for filename in os.listdir(dataset_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(dataset_path, filename)
            with open(csv_file_path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row:
                        # cannot compare if not int
                        measures.append(int(row[0]))
                        chords.append(row[6])
                        last_row = row
                    # measures.append(int(last_row[1]))       
    return chords, measures


def encode_song(chords, measures, sequence_length, time_step = 1):
    # p = 60, d = 1.0 -> [60, "_", "_", "_"]
    
    encoded_song = []
    chord_number = 0
    new_song_delimiter = "/ " * sequence_length
    
    switch_indices_list = []
    for i in range(1, len(measures) - 1):
            if measures[i] < measures[i - 1]:
                switch_indices_list.append(i)

    print(switch_indices_list)
    
    
    for event in chords:
        chord_number += 1
        symbol = event
        
        # convert the chords into time series notation
        
        if(chord_number == len(measures)) or (is_number_in_array(chord_number, switch_indices_list)):
            print(chord_number)
            steps = 4
            # steps = int(float(measures[chord_number + 1])) - int(float(measures[chord_number]))
            # del measures[chord_number]
            for step in range(steps):
                if step == 0:
                    encoded_song.append(symbol)
                else:
                    encoded_song.append("_")
                    
               
            encoded_song.append(new_song_delimiter)
            
        else:
            
            steps = int((int(float(measures[chord_number])) - int(float(measures[chord_number - 1])) / time_step))
            for step in range(steps):
                if step == 0:
                    encoded_song.append(symbol)
                else:
                    encoded_song.append("_")
        
        
    encoded_song = encoded_song[:-1]
    # cast encoded song to a string
    encoded_song = " ".join(map(str, encoded_song))
    
    return encoded_song

def preprocess(dataset_path):
    pass

    # load the folk songs
    print("Loading songs...")
    chords, measures = load_songs_in_csv(dataset_path)
    
    # encode songs with music time series representation
    encoded_song = encode_song(chords, measures, SEQUENCE_LENGTH)
        
    # save songs to text file
    save_path = os.path.join(SAVE_DIR)
    with open(save_path, "w") as fp:
        fp.write(encoded_song)
            
                     
def load(file_path): 
    with open(file_path, "r") as fp:
        song = fp.read()           
    return song

def create_mapping(songs, mapping_path):
    
    mappings = {}
    
    # identify the vocabulary
    songs = songs.split()
    vocabulary = list(set(songs))
    
    # create mapping
    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i
    
    # save vocabulary to a json file
    with open(mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)
        
def convert_songs_to_int(songs):
    int_songs = []
    
    # load mappings
    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)
    
    # cast songs string to a list
    songs = songs.split()
    
    # map songs to int
    for symbol in songs:
        int_songs.append(mappings[symbol])
        
    return int_songs

def generate_training_sequences(sequence_length):
    
    # load songs and map them to int
    songs = load(SAVE_DIR)
    int_songs = convert_songs_to_int(songs)
     
    # generate the training sequences
    inputs = []
    targets = []
    
    num_sequences = len(int_songs) - sequence_length
    for i in range(num_sequences):
        inputs.append(int_songs[i:i+sequence_length])
        targets.append(int_songs[i+sequence_length])
    
    
    # one-hot encode the sequences
    # inputs: (# of sequences, sequence length, vocabulary size)
    # [ [0, 1, 2], [1, 1, 2] ] -> [ [ [1, 0, 0], [0, 1, 0], [0, 0, 1] ], []}
    vocabulary_size = len(set(int_songs))
    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)
    
    return inputs, targets
    
def is_number_in_array(number, arr):
    return number in arr
    
def main():
    preprocess(CSV_DATASET_PATH)
    songs = load(SAVE_DIR)
    create_mapping(songs, MAPPING_PATH)
    # inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)

if __name__ == "__main__":
    main()