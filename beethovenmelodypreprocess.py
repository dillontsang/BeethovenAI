'''
Created on Aug 21, 2023

@author: dillontsang
'''

import os
import json
import numpy as np
import tensorflow.keras as keras
import csv

CSV_DATASET_PATH = "beethovenmelodydataset"
SAVE_DIR = "beethoven_melody_dataset"
MAPPING_PATH = "beethovenmelodymapping.json"
SEQUENCE_LENGTH = 64

# durations expressed in quarter length
ACCEPTABLE_DURATIONS = [
    0.25,
    0.5,
    0.75,
    1.0,
    1.5,
    2,
    3,
    4
]
        
def load_songs_in_tsv(dataset_path, acceptable_durations):
    
    notes = []
    durations = []
    column_index = 0
    midi_index = 0
    voice_index = 0
    
    # go through all the files in dataset and load notes and durations
    for filename in os.listdir(dataset_path):
        print(filename)
        if filename.endswith('.tsv'):
            tsv_file_path = os.path.join(dataset_path, filename)
            with open(tsv_file_path, 'r', newline='') as tsvfile:
                tsv_reader = csv.reader(tsvfile, delimiter='\t')
                for row_index, row in enumerate(tsv_reader):
                    if row_index == 0:
                        key = row[0]
                        print(key)
                        for element in row:
                            if(element == "duration_qb"):
                                duration_index = column_index
                                print("duration index: " + str(duration_index))
                            if(element == "staff"):
                                voice_index = column_index
                                print("voice index: " + str(voice_index))
                            if(element == "midi"):  
                                midi_index = column_index
                                print("midi_index: " + str(midi_index))
                            
                            column_index += 1
                        column_index = 0
                    else:
                        if(row[voice_index] == "1" and float(row[duration_index]) in acceptable_durations):
                            # print(row[midi_index])
                            transposed_note = transpose_note(row[midi_index], key)
                            # print(transposed_note)
                            fixed_range_note = fix_range(transposed_note)
                            print(fixed_range_note)
                            notes.append(fixed_range_note)
                            durations.append(row[duration_index])
                        
        print()
        print ("-" * 80) 
        notes.append('/')
        durations.append('/')
        
    
    return notes, durations

def transpose_note(note, key):
    if(key == "C"):
        return int(note)
    elif(key == "G"):
        return int(note) + 5
    elif(key == "D"):
        return int(note) - 2
    elif(key == "Bb"):
        return int(note) + 2
    elif(key == "A"):
        return int(note) + 3
    elif(key == "Eb"):
        return int(note) - 3
    elif(key == "F"):
        return int(note) - 5
    elif(key == "E"):
        return int(note) - 4
    elif(key == "Ab"):
        return int(note) + 4
    elif(key == "Db"):
        return int(note) - 1
    else:
        print("not a valid key")
        
def fix_range(note):
    while (note < 63 or note > 92):
        if(note < 63):
            note += 12
        if(note > 92):
            note -= 12
            
    # range from G3 to E5
    note -= 12
    return str(note)

def encode_song(notes, durations, sequence_length, time_step = 0.25):
    # p = 60, d = 1.0 -> [60, "_", "_", "_"]
    
    encoded_song = []
    note_number = 0
    new_song_delimiter = "/ " * sequence_length
    
    for event in notes:
        midi = event
        
        # convert the melody into time series notation
        
        if(event == '/'):
            encoded_song.append(new_song_delimiter)
        else:
            steps = int(float(durations[note_number]) / time_step)
            for step in range(steps):
                if step == 0:
                    encoded_song.append(midi)
                else:
                    encoded_song.append("_")
        
        note_number += 1
        
        
    encoded_song = encoded_song[:-1]
    # cast encoded song to a string
    encoded_song = " ".join(map(str, encoded_song))
    
    return encoded_song

def preprocess(dataset_path, acceptable_durations):
    pass

    # load the songs
    print("Loading songs...")
    notes, durations = load_songs_in_tsv(dataset_path, acceptable_durations)
    
    encoded_song = encode_song(notes, durations, SEQUENCE_LENGTH)
   
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
    

def main():
    # preprocess(CSV_DATASET_PATH, ACCEPTABLE_DURATIONS)
    
    songs = load(SAVE_DIR)
    # create_mapping(songs, MAPPING_PATH)
    
    
    # inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)

if __name__ == "__main__":
    main()