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
FILTERED_CSV_DATASET_PATH = "filteredbeethovenmelodydataset"
SAVE_DIR = "beethoven_melody_dataset"
MAPPING_PATH = "melodymapping.json"
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

def remove_bad_durations(dataset_path, filtered_dataset_path, acceptable_durations):
    
    i = 0
    
    # go through all the files in dataset and remove anything that doesnt fit in acceptable durations
    for filename in os.listdir(dataset_path):
        output_file_name = str(i) + '.csv' 
        output_file_path = os.path.join(filtered_dataset_path, output_file_name)
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(dataset_path, filename)
            with open(csv_file_path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                rows = list(csv_reader)
                
            filtered_rows = [row for row in rows if float(row[3]) in acceptable_durations]
            print(filtered_rows)
                
            with open(output_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(filtered_rows)

        i += 1
        
def load_songs_in_csv(filtered_dataset_path):
    
    notes = []
    durations = []
    
    # go through all the files in dataset and load notes and durations
    for filename in os.listdir(filtered_dataset_path):
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(filtered_dataset_path, filename)
            with open(csv_file_path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row:
                        notes.append(row[1])
                        durations.append(row[3])
        notes.append('/')
        durations.append('/')    
    return notes, durations

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

def preprocess(filtered_dataset_path):
    pass

    # load the songs
    print("Loading songs...")
    notes, durations = load_songs_in_csv(filtered_dataset_path)
    
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
    # remove_bad_durations(CSV_DATASET_PATH, FILTERED_CSV_DATASET_PATH, ACCEPTABLE_DURATIONS)
    # preprocess(FILTERED_CSV_DATASET_PATH)
    
    songs = load(SAVE_DIR)
    # create_mapping(songs, MAPPING_PATH)
    # inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)

if __name__ == "__main__":
    main()