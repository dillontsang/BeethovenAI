'''
Created on Aug 18, 2023

@author: dillontsang
'''

import os
import json
import numpy as np
import tensorflow.keras as keras
import csv

CSV_DATASET_PATH = "beethovenchorddataset16"
SAVE_DIR = "beethoven_chord_progression_dataset_16"
MAPPING_PATH2 = "sequencemapping2.json"
MAPPING_PATH3 = "sequencemapping3.json"
MAPPING_PATH4 = "sequencemapping4.json"

symbol_chord_progression = 

'''['i', '_', '_', '_', '_', '_', '_', '_', '_', 'V65', '_', '_', '_', '_', '_', '_', '_', 'i', '_', '_', '_', 'V43', '_', '_', '_', 'i6', '_', 'ii-6', '_', 'V', '_', '_', 'iii', '_', '_', '_', '_', '_', '_', '_', '_', 
'IV65', '_', '_', '_', 'ii7', '_', '_', '_', 'V43', '_', '_', '_', 'I', '_', '_', '_', 'ii6', '_', 'V65/V', '_', 'V', '_', '_', '_', 'ii6', '_', 'V65/V', '_', 'V', '_', '_', '_', 'ii6', '_', 'V65/V', '_', 'V', '_', '_', 
'V7', '_', '_', '_', '_', '_', '_', 'I64', 'V7', '_', '_', '_', '_', '_', '_', 'I64', 'V7', '_', '_', 'V42', '_', 'I6', '_', 'V6', '_', 'I', '_', 'vii-6/V', '_', 'V', '_', 'vii-6/V', '_', 'V', '_', 'vii-43', '_', 'I6', 
'_', 'vii-43', '_', 'I6', '_', 'V6', '_', 'I', '_', 'V43', '_', 'I6', '_', '_', '_', 'ii6', '_', '_', '_', 'I64', '_', '_', '_', 'V42', '_', '_', '_', 'I', '_', 'vii-7/V', '_', 'I64', '_', 'I64', '_', 'I64', '_', 'IV', 
'_', 'vii-7/V', '_', 'I', '_', 'vii-6', '_', 'vii-6', '_', 'I64', '_', 'V', '_', 'i', '_', 'i6', '_', 'i', '_', 'V6', '_', 'i', '_', 'i', '_', 'i64', '_', '_', '_', 'V65', '_', '_', '_', 'vii-', '_', '_', '_', 'vii-42/V',
 '_', '_', '_', 'V6', '_', '_', '_', 'I', '_', '_', '_', 'i', '_', '_', '_', 'I', '_', '_', '_', 'vii-6/V', '_', '_', '_', 'V42', '_', '_', '_', 'i6', '_', '_', '_', 'i', '_', '_', '_', 'V43', '_', '_', '_', 'i', '_', 
'vii-6', '_', 'V6', '_', 'V65/iv', '_', 'i', '_', 'i6', '_', 'i64', '_', 'V7', '_', '_', '_', 'i64', '_', 'iv64', '_', '_', '_', '_', '_', 'i6', '_', 'vii-43/V', 'vii-6/V', 'vii-7/V', '_', 'vii-7/V', '_', '_', '_', 
'i64', '_', 'I64', '_', 'vii-7/V', '_', '_', '_', 'vii-7/V', '_', 'vii-7/V', 'I64', 'V7', '_', 'I64', '_', 'I64', 'V7', '_', '_', 'I', '_', '_', 'IV64', '_', '_', 'IV64', '_', '_', 'ii42', '_', 'vii-42/ii', 'ii42', 
'_', '_', 'IV64', '_', '_', '_', '_', '_', 'vii-42/iii', '_', 'V7/V', '_', '_', 'VI', '_', '_', 'VI', '_', 'vii-7/V', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'V7', '_', 
'_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'I', '_', 'i', '_', 'V7', '_', 'i', '_', 'V', '_', 'i', '_', 'V7', '_', '_', '_', 'I', 'V7', '_', '_', 'I', 'ii65', '_', 'V7', '_', 'I', '_', '_', '_']
Two chord similarity 0.7579365079365079
Three chord similarity 0.5137599999999999
Four chord similarity 0.45161290322580644'''




def load_songs_in_csv(dataset_path):
    
    chords = []
    
    # go through all the files in dataset and load chords and measures
    for filename in os.listdir(dataset_path):
        if filename.endswith('.csv'):
            print(filename)
            csv_file_path = os.path.join(dataset_path, filename)
            with open(csv_file_path, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row:
                        chords.append(row[6])       
    return chords

def encode_song(chords):
    
    encoded_song = []
    chord_number = 0
    # print(measures[0])
    
    
    for event in chords:
        chord_number += 1
        symbol = event
        
        # convert the chords into time series notation
        
        encoded_song.append(symbol)
        
    encoded_song = " ".join(map(str, encoded_song))
    
    return encoded_song

def create_progressions(dataset_path):
    pass

    # load the chords and measures
    print("Loading songs...")
    chords = load_songs_in_csv(dataset_path)
    
    # encode songs with music time series representation
    encoded_song = encode_song(chords)
    # print(encoded_song)
        
    # save songs to text file
    save_path = os.path.join(SAVE_DIR)
    with open(save_path, "w") as fp:
        fp.write(encoded_song)
            
                     
def load(file_path): 
    with open(file_path, "r") as fp:
        song = fp.read()           
    return song

'''def create_sequences2(songs):
    
    sequences2 = []
    cleaned_sequences = []
    # song is string
    songs = songs.split()
    
    for i in range(len(songs) - 1):
        sequence2 = [songs[i], songs[i + 1]]
        sequences2.append(sequence2)
        
    
    for list in sequences2:
        string = ' '.join(list)
        string_without_apostrophes = string.replace("'", "")
        
        # Remove underscores
        string_without_underscores = string_without_apostrophes.replace("_", "")
        
        cleaned_sequences.append(string_without_underscores)
        
    return cleaned_sequences

def create_sequences3(songs):
    
    sequences3 = []
    cleaned_sequences = []
    songs = songs.split()
    
    for i in range(len(songs) - 2):
        sequence3 = [songs[i], songs[i + 1], songs[i + 2]]
        sequences3.append(sequence3)
        
    
    for list in sequences3:
        string = ' '.join(list)
        string_without_apostrophes = string.replace("'", "")
        
        # Remove underscores
        string_without_underscores = string_without_apostrophes.replace("_", "")
        
        cleaned_sequences.append(string_without_underscores)
        
    return cleaned_sequences

def create_sequences4(songs):
    
    sequences4 = []
    cleaned_sequences = []
    songs = songs.split()
    
    for i in range(len(songs) - 3):
        sequence4 = [songs[i], songs[i + 1], songs[i + 2], songs[i + 3]]
        sequences4.append(sequence4)
        
    
    for list in sequences4:
        string = ' '.join(list)
        string_without_apostrophes = string.replace("'", "")
        
        # Remove underscores
        string_without_underscores = string_without_apostrophes.replace("_", "")
        
        cleaned_sequences.append(string_without_underscores)
        
    return cleaned_sequences'''


        
def create_mapping(sequences, mapping_path):
    frequency_dict = {} 
    sequence_vocab = []
    
    # create mapping
    for symbol in sequences:
        
        if symbol in frequency_dict:
            frequency_dict[symbol] += 1
        else:
            frequency_dict[symbol] = 1
    
    # save vocabulary to a json file
    for symbol, frequency in frequency_dict.items():
        sequence_vocab.append(str(symbol) + ": " + str(frequency))
    
    with open(mapping_path, "w") as fp:
        json.dump(sequence_vocab, fp, indent=4)
        

def remove_strings_with_underscores(strings):
    # Use a list comprehension to filter out strings with underscores
    filtered_strings = [s for s in strings if '_' not in s]
    return filtered_strings

    # Example usage
    input_strings = ["apple", "banana", "cherry", "date", "kiwi", "pear", "pine_apple"]
    filtered_list = remove_strings_with_underscores(input_strings)

    print(filtered_list)
    return filtered_list

def clean_chord_progression(chord_progression):
    cleaned_sequences = []
    for list in chord_progression:
        string = ' '.join(list)
        string_without_apostrophes = string.replace("'", "")
        
        # Remove underscores
        string_without_underscores = string_without_apostrophes.replace("_", "")
        
        cleaned_sequences.append(string_without_underscores)
    
    return cleaned_sequences

def clean_notepad_files(beethoven_progression):
    cleaned_beethoven_progression = []
    
    for string in beethoven_progression:
        result_string = string[4:]

        # Remove double quotation marks and commas from the result string
        result_string = result_string.replace('"', '').replace(',', '')
        cleaned_beethoven_progression.append(result_string)
        
    return cleaned_beethoven_progression
    
def main():
    '''songs = load(SAVE_DIR)
    sequences4 = create_sequences4(songs)
    create_mapping(sequences4, MAPPING_PATH4)'''

    twochordsimilarity = 0
    chord_number = 0
    beethoven_progressions2 = []
    
    with open(MAPPING_PATH2, "r") as fp:
        for line in fp:
            beethoven_progressions2.append(line)
            
    beethoven_progressions2 = clean_notepad_files(beethoven_progressions2)
    
    chord_progression = remove_strings_with_underscores(symbol_chord_progression)
    chord_progression2 = []
    cleaned_chord_progressions2 = []
    
    for i in range(len(chord_progression) - 1):
        sequence2 = [chord_progression[i], chord_progression[i + 1]]
        chord_progression2.append(sequence2)
    
    cleaned_chord_progressions2 = clean_chord_progression(chord_progression2)
    
    for symbol in cleaned_chord_progressions2:
        chord_number += 1
        
        for progression in beethoven_progressions2:
            progression = progression.strip("\n")
            colon_index = progression.find(':')
            chords = progression[:colon_index]
            # print(progression)
            frequency = progression[colon_index + 2:]
            # print(frequency)
            frequency = int(frequency)
            
            if(symbol == chords):
                if frequency == 1:
                    twochordsimilarity += 0.25
                elif frequency == 2:
                    twochordsimilarity += 0.5
                elif frequency == 3:
                    twochordsimilarity += 0.75
                elif frequency >= 4:
                    twochordsimilarity += 1
            
            
    print("Two chord similarity " + str(twochordsimilarity / float(chord_number)))
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    threechordsimilarity = 0
    chord_number = 0
    beethoven_progressions3 = []
    
    with open(MAPPING_PATH3, "r") as fp:
        for line in fp:
            beethoven_progressions3.append(line)
            
    beethoven_progressions3 = clean_notepad_files(beethoven_progressions3)
    
    chord_progression = remove_strings_with_underscores(symbol_chord_progression)
    chord_progression3 = []
    cleaned_chord_progressions3 = []
    
    for i in range(len(chord_progression) - 2):
        sequence3 = [chord_progression[i], chord_progression[i + 1], chord_progression[i + 2]]
        chord_progression3.append(sequence3)
    
    cleaned_chord_progressions3 = clean_chord_progression(chord_progression3)
    
    for symbol in cleaned_chord_progressions3:
        chord_number += 1
        
        for progression in beethoven_progressions3:
            progression = progression.strip("\n")
            colon_index = progression.find(':')
            chords = progression[:colon_index]
            # print(progression)
            frequency = progression[colon_index + 2:]
            # print(frequency)
            frequency = int(frequency)
            
            if(symbol == chords):
                if frequency == 1:
                    threechordsimilarity += 0.33
                elif frequency == 2:
                    threechordsimilarity += 0.66
                elif frequency >= 3:
                    threechordsimilarity += 1
            
            
    print("Three chord similarity " + str(threechordsimilarity / float(chord_number)))
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    fourchordsimilarity = 0
    chord_number = 0
    beethoven_progressions4 = []
    
    with open(MAPPING_PATH4, "r") as fp:
        for line in fp:
            beethoven_progressions4.append(line)
            
    beethoven_progressions4 = clean_notepad_files(beethoven_progressions4)
    
    chord_progression = remove_strings_with_underscores(symbol_chord_progression)
    chord_progression4 = []
    cleaned_chord_progressions4 = []
    
    for i in range(len(chord_progression) - 3):
        sequence4 = [chord_progression[i], chord_progression[i + 1], chord_progression[i + 2], chord_progression[i + 3]]
        chord_progression4.append(sequence4)
    
    cleaned_chord_progressions4 = clean_chord_progression(chord_progression4)
    
    for symbol in cleaned_chord_progressions4:
        chord_number += 1
        
        for progression in beethoven_progressions4:
            progression = progression.strip("\n")
            colon_index = progression.find(':')
            chords = progression[:colon_index]
            # print(progression)
            frequency = progression[colon_index + 2:]
            # print(frequency)
            frequency = int(frequency)
            
            if(symbol == chords):
                if frequency == 1:
                    fourchordsimilarity += 0.5
                elif frequency >= 2:
                    fourchordsimilarity += 1
            
            
    print("Four chord similarity " + str(fourchordsimilarity / float(chord_number)))
    
if __name__ == "__main__":
    main()