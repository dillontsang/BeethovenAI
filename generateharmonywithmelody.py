'''
Created on Aug 17, 2023

@author: dillontsang
'''
from music21 import *
import itertools
import re
from melodygenerator import MelodyGenerator, SEQUENCE_LENGTH

# soprano seed to start song
soprano_beginning_seed = "72 _ _ _ 76 _ _ _ 79 _ _ _ 74 _ _ _ 77 _ _ _ 76 _ _ _ 72 _ _ _ 74 72 71 69 67 _ _ _ _ _ _ _ 67 _ _ _ 67 _ _ _ 69 _ 71 _ 72 _ _ _ 72 _ _ _ 74 _ _ _"



# "67 _ _ _ 67 65 _ 62 64 _ _ _ _ _ _ _ 62 _ _ _ 60 _ _ _ 67 65 _ 62 64 _ _ _ _ _ _ _ 62 _ _ _"
# "62 _ 59 _ _ _ 67 _ _ _ 69 _ _ _ 67 _ 62 _ 59 _ _ _ 67 _ _ _ 60 _ 67 _ 64 _"

# "60 _ _ _ 60 _ _ _ 62 _ _ _ 62 _ _ _ 64 _ _ _ 62 _ 64 _ 65 _ _ _ 64 _ _ _ 62 _ _ _ 62 _ _ _"
# "64 _ _ _ 67 _ 65 _ 65 _ _ _ 62 _ _ _ 62 _ _ _ 64 _ _ _ 64 _ 65 _ 67 _ _ _ 64 _ 62 _" #not beethoven
# "60 _ 62 _ 62 _ 59 _ 59 _ 60 _ _ _"
# "60 _ 64 _ _ 65 64 _ 60 _ 64 _"
# 67 _ 72 _ _ _ 69 _ 67 _ _ _ 64 _ 62 _ _ _ 64 _ 65 _ _ _ 67 _ 64 _ _ _ 62 _ 60 _ _ _"


# Define the chord progression

symbol_chord_progression = ['I', '_', 'I6', '_', 'V7', '_', 'I', '_', 'I', '_', 'V7/IV', '_', 'IV', '_', 
                            'IV6', '_', 'ii7', '_', 'V65', '_', 'I', '_', 'V65', '_', 'I', '_', 
                            '_', '_', 'V65', '_', '_', '_', 'I', '_', '_', '_', 'V7/IV', '_', '_', '_', 
                            'IV', '_', 'I64', 'V7', 'I', '_', '_', '_', 'IV', '_', '_', '_', 'I', 'ii6', 
                            'I64', 'V', 'I', '_', '_', '_', 'IV', '_', '_', '_', 'I', 'ii6', 'I64', 'V', 
                            'I', '_', 'V42', '_', 'I', '_', 'V42', '_', 'I', 'V42', 'I', 'V42', 'I', '_', 
                            '_', '_', 'I', '_', '_', '_', 'I6', 'V64', 'I', 'V6', 'V', 'I', 'V42/IV', 
                            'vi7', 'V65', 'I', '_', '_', '_', 'I6', 'V64', 'I', 'V6', 'V', 
                            'I', 'V42/IV', 'vi7', 'V65', 'I', '_', 'ii6', '_', '_', '_', 'I6', '_', '_', 
                            '_', 'IV', '_', 'V', '_', 'I', '_', '_', '_', 'ii6', '_', '_', '_', 'V65/V', 
                            '_', '_', '_', 'V7', '_', '_', '_', 'I64', '_', '_', '_', 'V7', '_', '_', '_', 
                            'I64', '_', '_', '_', 'V', 'I64', 'V', 'I64', 'V', '_', '_', '_', 'I6', 'V42', 
                            'I6', 'V6', 'I', 'V6', 'V', '_', 'V42', 'I6', 'V64', 'I', 'V65', 'I', '_', '_', 
                            'ii6', '_', 'I6', '_', 'ii6', '_', 'I6', '_', 'ii6', '_', 'I64', 'V7', 'I', 
                            '_', 'V43', '_', 'I', '_', 'V65', '_',
                            'I', '_', 'V7/IV', '_', 'IV', '_', 'I64', 'V7', 'I', '_', '_', '_']

'''['ii7', '_', 'V65', '_', 'I', '_', 'V65', '_', 'I', '_', 
                            '_', '_', 'V65', '_', '_', '_', 'I', '_', '_', '_', 'V7/IV', '_', '_', '_', 
                            'IV', '_', 'I64', 'V7', 'I', '_', '_', '_', 'IV', '_', '_', '_', 'I', 'ii6', 
                            'I64', 'V', 'I', '_', '_', '_', 'IV', '_', '_', '_', 'I', 'ii6', 'I64', 'V', 
                            'I', '_', 'V42', '_', 'I', '_', 'V42', '_', 'I', 'V42', 'I', 'V42', 'I', '_', 
                            '_', '_', 'I', '_', '_', '_', 'I6', 'V64', 'I', 'V6', 'V', 'I', 'V42/IV', 
                            'vi7', 'V65', 'I', '_', '_', '_', 'I6', 'V64', 'I', 'V6', 'V', 
                            'I', 'V42/IV', 'vi7', 'V65', 'I', '_', 'ii6', '_', '_', '_', 'I6', '_', '_', 
                            '_', 'IV', '_', 'V', '_', 'I', '_', '_', '_', 'ii6', '_', '_', '_', 'V65/V', 
                            '_', '_', '_', 'V7', '_', '_', '_', 'I64', '_', '_', '_', 'V7', '_', '_', '_', 
                            'I64', '_', '_', '_', 'V', 'I64', 'V', 'I64', 'V', '_', '_', '_', 'I6', 'V42', 
                            'I6', 'V6', 'I', 'V6', 'V', '_', 'V42', 'I6', 'V64', 'I', 'V65', 'I', '_', '_', 
                            'ii6', '_', 'I6', '_', 'ii6', '_', 'I6', '_', 'ii6', '_', 'I64', 'V7', 'I', 
                            '_', 'V43', '_', 'I', '_', 'V65', '_',
                            'I', '_', 'V7/IV', '_', 'IV', '_', 'I64', 'V7', 'I', '_', '_', '_']'''



'''['I', 'IV', '_', 'ii6', 'I64', '_', 'V7', 'I', '_', '_', '_', 'V43', '_', '_', '_', 'I', '_', 'V42', '_', '_', '_', 'I6', 
'_', '_', '_', 'ii6', '_', 'V', '_', 'I', '_', '_', '_', 'V42', '_', '_', '_', 'I6', '_', '_', '_', 'ii6', '_', 'V7', '_', 'I', '_', 
'_', '_', 'V42', '_', '_', '_', 'I6', '_', '_', '_', 'ii6', '_', 'V7', '_', 'I', '_', 'V42', '_', 'I', '_', '_', '_', 'V7', '_', 'I',
 '_', 'I', '_', '_', '_', 'V7/IV', '_', 'V42', '_', 'I', '_', '_', '_', 'V65', '_', 'I', '_', 'V42', '_', '_', '_', 'I', '_', 'V7', 
'_', 'I', '_', '_', '_', 'I', '_', 'V', '_', 'I', '_', '_', '_', 'V/V', '_', '_', '_', 'V7', '_', '_', 'vii-/V', 'V7', '_', '_', '_', 
'I', '_', '_', 'V7', 'I', '_', '_', 'V43', '_', '_', '_', '_', '_', 'V65', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'I', 
'_', '_', 'V65', '_', '_', 'V7', '_', '_', 'I', '_', '_', 'I', '_', '_', 'V65', '_', '_', 'V7', '_', '_', 'I', '_', '_', 'V', '_', '_', 
'vi', '_', '_', 'V42/V', '_', '_', 'V7', '_', '_', '_', '_', '_', 'vii-42', '_', '_', 'V7', '_', 'V42', 'I6', '_', 'I', 'V7', '_', '_', 
'vii-42', '_', '_', 'V7', '_', 'V42', 'I6', '_', 'I', 'IV', '_', 'ii6', 'I64', '_', 'V7', 'I', '_', '_', 'V43', '_', '_', 'I6', '_', '_', 
'V43', '_', '_', 'I', '_', '_', '_', 'IV', '_', '_', 'ii6', '_', '_', 'V7', '_', 'I', '_', 
'_', '_']'''

'''['I', '_', 'ii6', '_','V7', '_', 'I', '_', 'IV', '_', 'I6', '_', 'IV6', '_', 'I64', '_', 'V42', 
'_', 'I6', '_', 'V7', '_', 'I', '_', '_', '_', 'ii6', '_', '_', '_', 'V43', '_', '_', '_', 'I', '_', '_', '_', 
'I64', '_', 'V7', '_', 'I64', '_', 'V7', '_', 'I', '_', 'IV', '_', 'I64', 
'_', 'V7', '_', 'I', '_', '_', '_', 'ii6', '_', '_', '_', 'I', '_', 
'IV6', '_', 'V42/IV', '_', 'vi7', '_', 'V65', '_', 'I', '_', '_', '_','V', '_', 'I', '_', '_', '_',
'V65/ii', '_', 'ii', '_', '_', '_', 'V65', '_', '_', '_', 'V65', '_', 'I', '_',
'V7/ii', '_', 'ii', '_', '_', '_', 'V6', '_', '_', '_', 'V', '_', 'V7', '_', 
'I', '_', 'I6', '_', 'V42', '_', 'I6', '_', 'V42', '_', 'I6', 'vii-65/ii', 'ii6', '_', 'V7', '_', 'I', '_', '_', 
'I6', 'V42', '_', 'I6', '_', 'V42', '_', 'I6', 'vii-65/ii', 'ii6', '_', 'V7', '_', 'I', '_', 'IV64', 'V7', 'I', '_',
'V43', 'I6', 'ii6', '_', 'I64', 'V', 'I6', '_', 
'V64', 'I', 'ii6', '_', 'I64', 'V', 'I6', '_', 'V64', 'I', 'ii6', '_', '_', '_', 'V7', '_', '_', '_', 'I', '_', 
'IV', '_', 'I6', '_', 'IV6', '_', 'I64', '_', 'V42', '_', 'I6', '_', 'V7', '_', 'I', '_', '_', '_', 'IV6', '_', '_', '_', 
'vii=65', '_', '_', '_', 'vii-43/vi', '_', '_', '_', 'vi6', '_', '_', '_', 'ii7', '_', '_', '_', 
'V65/V', '_', 'V7', '_', 'I64', '_', '_', '_', 'V7', '_', '_', '_', 'I', '_', '_', '_', 'vii-6', '_', 'I', '_', 'IV6', '_', 
'I64', '_', 'V7', '_', 'I', '_', '_', '_', 'ii6', '_', '_', '_', 'V43', '_', '_', '_', 'I', 
'_', 'IV', '_', 'I64', '_', 'V7', '_', 'I', '_', '_', '_']'''

'''['i', '_', '_', '_', '_', '_', '_', '_', '_', 'V65', '_', '_', '_', '_', '_', '_', '_', 'i', '_', '_', '_', 'V43', 
'_', '_', '_', 'i6', '_', 'ii-6', '_', 'V', '_', '_', 'iii', '_', '_', '_', '_', '_', '_', '_', '_', 
'IV65', '_', '_', '_', 'ii7', '_', '_', '_', 'V43', '_', '_', '_', 'I', '_', '_', '_', 'ii6', '_', 'V65/V', '_', 
'V', '_', '_', '_', 'ii6', '_', 'V65/V', '_', 'V', '_', '_', 'V7', '_', '_', '_', '_', '_', '_', 'I64', 
'V7', '_', '_', '_', '_', '_', '_', 'I64', 'V7', '_', '_', 'V42', '_', 'I6', '_', 'V6', '_', 'I', '_', 'vii-6/V', 
'_', 'V', '_', 'vii-6/V', '_', 'V', '_', 'vii-43', '_', 'I6', '_', 'vii-43', '_', 'I6', '_', 'V6', '_', 
'I', '_', 'V43', '_', 'I6', '_', '_', '_', 'ii6', '_', '_', '_', 'I64', '_', '_', '_', 'V42', '_', '_', '_', 'I', 
'_', 'vii-7/V', '_', 'I64', '_', 'V7', '_', 'I', '_', 'vii-7/V', '_', 'I64', '_', 'V7', '_', 'I', '_', 
'vii-7/V', '_', 'I64', '_', 'V7', '_', 'I', '_', '_', '_', '_', '_', '_', 'I', '_', '_', '_', '_', '_', '_', '_', 
'V43/V', 'V65', '_', '_', '_']'''

'''['I', '_', 'IV', '_', 'V', '_', 'I', '_', '_', '_', 'ii65', '_', '_', '_', 'vii-7/V', '_', '_', '_', 'I64', '_', '_', 'V7', '_', '_', 'I', '_', '_', '_', 'ii65', '_', '_', '_', 'vii-7/V', '_', '_', '_', 'I64', '_', '_', 'V7', '_', 
'_', 'I', '_', '_', '_', 'ii65', '_', '_', '_', 'vii-7/V', '_', '_', '_', 'I64', '_', '_', 'V7', '_', '_', 'I', '_', '_', '_', 'ii65', '_', 'vii-7/V', '_', '_', '_', 'i64', '_', '_', '_', 'vii-7/V', '_', '_', 'vii-43', '_', '_', 
'i6', '_', '_', 'V65', '_', '_', 'I', '_', '_', 'IV64', '_', '_', 'I7', '_', '_', 'ii42', '_', 'V42', 'I', '_', '_', 'IV64', '_', '_', 'I7', '_', '_', 'ii42', '_', 'V42', 'I', '_', '_', 'Fr+6', '_', '_', 'V', '_', '_', 'Fr+6', 
'_', '_', 'V', '_', '_', 'Fr+6', '_', '_', 'V', '_', '_', 'V7', '_', '_', 'I', '_', '_', 'Fr+6', '_', '_', 'V', '_', '_', 'Fr+6', '_', '_', 'V', '_', '_', 'V7', '_', '_', 'i', '_', '_', 'V7', '_', '_', 'I', '_', '_', 'V7', '_', '_', 
'I', '_', '_', 'I+', '_', '_', 'ii6', '_', '_', '_', 'V7', '_', '_', '_', 'i', '_', 'ii-', '_', '_', 'V65', '_', '_', 'V7', '_', '_', 'V65', '_', '_', 'i', '_', '_', '_', 'V42', 'i6', '_', '_', 'i', '_', '_', 'ii-', '_', '_', 
'V65', '_', '_', 'V', '_', '_', 'V65', '_', '_', 'i', '_', '_', '_', 'V7', '_', 'I', '_', '_', '_']'''




def roman_to_int(roman):
        roman_numerals = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7,
                      'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7
                      }

        return roman_numerals.get(roman, roman)

def analyze_chord_symbol(chord_symbol, index, duration_check):
          
    roman_numeral_end = 0
    triad_or_seventh = 0
    inversion_end = 0
    inversion = 0
    secondary_dominant_numeral = 0
    duration = 1
    
    for i in range(index + 1, len(duration_check)):
        if duration_check[i] == '_':
            duration += 1
        else:
            break
     
    if chord_symbol == "_":
        return "", "", "", "", ""

    # Extract Roman numeral, quality, and inversion from chord symbol
    
    if chord_symbol[:3].isalpha():
        roman_numeral_end = 3
    elif chord_symbol[:2].isalpha():
        roman_numeral_end = 2
    else:
        roman_numeral_end = 1
        
    roman_numeral = chord_symbol[:roman_numeral_end]
    
    remainder = chord_symbol[roman_numeral_end:]
    
    
    # check quality
    if(chord_symbol[0].isupper()):
        quality = 'M'
    else:
        quality = 'm'
    
    if remainder != "":
        if remainder[0] == '+':
            quality = 'a'
            remainder = chord_symbol[roman_numeral_end + 1:]
        elif remainder[0] == '-':
            quality = 'd'
            remainder = chord_symbol[roman_numeral_end + 1:]
        elif remainder[0] == '=':
            quality = 'hd7'
            remainder = chord_symbol[roman_numeral_end + 1:]
    
    
    # check inversion
    if remainder != "":
        if remainder[:2].isdigit():
            inversion_end = 2
            
        elif remainder[:1].isdigit():
            inversion_end = 1
    else:
        inversion = 0
        
        
    if remainder != "":
        # triads chordorseventh = 0
        if(remainder[:inversion_end] == "6"):
            inversion = 1
            triad_or_seventh = 0
        elif(remainder[:inversion_end] == "64"):
            inversion = 2
            triad_or_seventh = 0
        # sevenths chordorseventh = 1
        elif(remainder[:inversion_end] == "7"):
            inversion = 0
            triad_or_seventh = 1
        elif(remainder[:inversion_end] == "65"):
            inversion = 1
            triad_or_seventh = 1
        elif(remainder[:inversion_end] == "43"):
            inversion = 2
            triad_or_seventh = 1
        elif(remainder[:inversion_end] == "42"):
            inversion = 3
            triad_or_seventh = 1
            
    # deal with dominant, major seventh, and fully diminished for seventh chords
    if quality == 'M' and triad_or_seventh == 1:
        quality = 'M7'
        if roman_numeral == 'V':
            quality = 'D7'
    elif quality == 'm' and triad_or_seventh == 1:
        quality = 'm7'
    elif quality == 'd' and triad_or_seventh == 1:
        quality = 'fd7'
            
    # deal with secondary dominant
    if remainder[inversion_end:] != "":
        secondary_dominant_numeral = remainder[inversion_end + 1:]
        
    # deal with special chords
    if len(chord_symbol) > 1:
        if(str(roman_to_int(chord_symbol[0])).isalpha() or chord_symbol[1] == "t"):
            if(chord_symbol[0] == "N"):
                quality = 'N'
                inversion = 1
                roman_numeral = 'II'
            
            # italian 6th
            elif(chord_symbol[1] == "t"):
                quality = 'I'
                inversion = 2
                roman_numeral = 'I'
                
            elif(chord_symbol[0] == "F"):
                quality = 'F7'
                inversion = 3
                roman_numeral = 'I'
                
            elif(chord_symbol[0] == "G"):
                quality = 'G7'
                inversion = 3
                roman_numeral = 'I'
                
            secondary_dominant_numeral = ""
        
    # TODO: Flat seven, secondary dominant for special chords
    
    if(roman_numeral == 'VI'):
        quality = "major6"
    
    print("chord symbol: " + chord_symbol)
    print()
    print("roman numeral: " + str(roman_to_int(roman_numeral)))
    print("quality: " + str(quality))
    print("inversion: " + str(inversion))
    print("secondary dominant roman numeral: " + str(roman_to_int(secondary_dominant_numeral)))
    print("duration: " + str(duration))
    print()
    return roman_to_int(roman_numeral), quality, inversion, roman_to_int(secondary_dominant_numeral), duration


def note_to_midi(scale_degree, harmonicminor):
    # Convert a note name or scale degree to its corresponding MIDI value
    c_major_scale = [60, 62, 64, 65, 67, 69, 71, 72]
    
    if 1 <= scale_degree <= 7 and harmonicminor == 0:
        return c_major_scale[scale_degree - 1]
    elif 1 <= scale_degree <= 7 and harmonicminor == 1:
        return c_major_scale[scale_degree - 1] + 1
    else:
        raise ValueError("Scale degree must be between 1 and 7")
    
    
def chord_to_midi(degree, quality, inversion, secondary_dominant_numeral):
    
        harmonicminor = 0
    
        # deal with secondary dominant
        if secondary_dominant_numeral != "" and secondary_dominant_numeral != 0:
            # deal with harmonic minor
            if degree == 7:
                harmonicminor += 1
            degree = degree + int(secondary_dominant_numeral) - 1
            if degree >= 8:
                degree -= 7
                
                
        # Major, Minor, Diminished, Augmented, 
        # Dominant, Major 7th, Minor 7th, Half Diminished, Fully Diminished
        # Neapolitan chord, italian chord, french chord, german chord
        # TODO: add flat seven
        chord_intervals = {
            'M': [0, 4, 7],
            'm': [0, 3, 7],
            'd': [0, 3, 6],
            'a': [0, 4, 8],
            'major6': [-1, 3, 6], # fix root of VI chord in a minor context
            'D7': [0, 4, 7, 10],
            'M7': [0, 4, 7, 11],
            'm7': [0, 3, 7, 10],
            'fd7': [0, 3, 6, 9],
            'hd7': [0, 3, 6, 10],
            'N': [-1, 3, 6],
            'I': [0, 6, 8],
            'F7': [0, 2, 6, 8],
            'G7': [0, 3, 6, 8]
            # Add more chord types and intervals as needed
        }
        
        root_midi = note_to_midi(degree, harmonicminor)
        intervals = chord_intervals[quality]
        
        chord_midi_values = [root_midi + interval for interval in intervals]
        chord_midi_values = chord_midi_values[inversion:] + chord_midi_values[:inversion]
        
        return chord_midi_values


# get number closest to target given list
def closest_number(notes, target):
    closest = None
    min_difference = float('inf')

    for note in notes:
        difference = abs(note - target)
        if difference < min_difference:
            min_difference = difference
            closest = note

    return closest

def choose_alto_and_tenor(alto_and_tenor_choices):
    sums = []
    
    # get combinations of alto and tenor choices
    combinations = list(itertools.combinations(alto_and_tenor_choices, 2))
    
    # pick combinations of alto and tenor notes centered around their voicings
    distances = [(abs(max(x, y) - 62), abs(min(x, y) - 55)) for x, y in combinations]
    
    for x, y in distances:
        distance_sum = x + y
        sums.append(distance_sum)
    
    indexed_sums = [(value, index) for index, value in enumerate(sums)]
    indexed_sums.sort()
    indexes_of_best_scores = [index for value, index in indexed_sums]
    
    sorted_choices = [combinations[i] for i in indexes_of_best_scores]
    
    # try not to have same note in alto and tenor
    for x, y in sorted_choices:
        alto_note = note.Note(max(x, y))
        tenor_note = note.Note(min(x, y))
        if not ((alto_note.pitch.midi - tenor_note.pitch.midi) % 12 == 0): 
            return alto_note, tenor_note
    
    # worst case scenario
    first_choice = sorted_choices[0]
    alto_note = note.Note(max(first_choice))
    tenor_note = note.Note(min(first_choice))
            
    return alto_note, tenor_note
    
# Define the four-part harmonization rules

# duration in quarter notes
def harmonize_chord(chord, soprano_seed, quality, duration):
    soprano_choices = []
    alto_and_tenor_choices = []
    bass_choices = []
    
    unused_chord_members = []
    half_used_chord_members = []
    double = 0
    
    if quality[-1] == '7':
        for i in range(-3, 1):
            unused_chord_members.append(chord[i].name)
    else:
        for i in range(-2, 1):
            unused_chord_members.append(chord[i].name)
    
    
    # temporary assignment of bass voice
    bass_note = chord[0]
    
    # get bass note
    for x in range(4):
        bass_choices.append(bass_note.pitch.midi - (x*12))
    
    # get closest note to C3
    bass_note.pitch = pitch.Pitch(closest_number(bass_choices, 48))
    
    # doubling rules for bass
    if quality[-1] == '7':
        unused_chord_members = [item for item in unused_chord_members if item != bass_note.name]     
    else:
        if not (bass_note.name == 'C' or bass_note.name == 'F' or bass_note.name == 'G'):
            unused_chord_members = [item for item in unused_chord_members if item != bass_note.name]
            
        else:
            half_used_chord_members.append(bass_note.name)
    
    # get soprano note
    if quality[-1] == '7':
        for i in range(-3, 0):
            for j in range(-2, 4):
                soprano_choices.append(chord[i].pitch.midi + (j*12))
    else:
        if len(half_used_chord_members) > 0: 
            for i in range (-2, 1):
                for j in range(-2, 4):
                    soprano_choices.append(chord[i].pitch.midi + (j*12))
        else: 
            for i in range (-2, 0):
                for j in range(-2, 4):
                    soprano_choices.append(chord[i].pitch.midi + (j*12))
                    
    filtered_soprano_choices = [value for value in soprano_choices if (55 <= value <= 76)]
    # filtered_soprano_choices = [value for value in soprano_choices if (60 <= value <= 80)]
    
    # generate soprano melody
    
    mg = MelodyGenerator()
    
    soprano_melody, soprano_note_midi = mg.generate_melody_to_match_chord_progression(soprano_seed, SEQUENCE_LENGTH, duration, filtered_soprano_choices, 0.4)
    
    soprano_note = note.Note(soprano_note_midi)
    
    # doubling rules for soprano
    if quality[-1] == '7':
        unused_chord_members = [item for item in unused_chord_members if item != soprano_note.name]     
    else:
        if soprano_note.name == bass_note.name:
            unused_chord_members = [item for item in unused_chord_members if item != soprano_note.name]
            double += 1
            half_used_chord_members.pop(0)
        elif not (soprano_note.name == 'C' or soprano_note.name == 'F' or soprano_note.name == 'G'):
            unused_chord_members = [item for item in unused_chord_members if item != soprano_note.name]
        else: 
            half_used_chord_members.append(soprano_note.name)
    
    # fix some doubling rules
    if double == 0:
        if quality[-1] != '7':
            if len(unused_chord_members) == 1:
                if not (bass_note.name == 'C' or bass_note.name == 'F' or bass_note.name == 'G'):
                    unused_chord_members.append(bass_note.name)
            
    # alto and tenor choices        
    if(quality[-1] != '7'):
        if(len(half_used_chord_members) != 2):
            for i in range(len(unused_chord_members)):       
                for j in range(-3, 3):
                    alto_and_tenor_choices.append(note.Note(unused_chord_members[i]).pitch.midi + (j*12))
        else:
            if(unused_chord_members[2] == 'C'): # very specific scenario to avoid strange doubling of I chord
                for i in range(0, 2): 
                    for j in range(-3, 3):
                        alto_and_tenor_choices.append(note.Note(unused_chord_members[i]).pitch.midi + (j*12))
            else:   
                for i in range(len(unused_chord_members) - 1):       
                    for j in range(-3, 3):
                        alto_and_tenor_choices.append(note.Note(unused_chord_members[i]).pitch.midi + (j*12))
    else:
        for i in range(len(unused_chord_members)):       
                for j in range(-3, 3):
                    alto_and_tenor_choices.append(note.Note(unused_chord_members[i]).pitch.midi + (j*12))
            
    alto_note, tenor_note = choose_alto_and_tenor(alto_and_tenor_choices)
                     
    return soprano_melody, alto_note, tenor_note, bass_note
    
def reverse_numbers_in_string(seed):
    
    new_string = ""
    current_number = ""

    for char in seed:
        if char.isdigit():
            current_number += char
        else:
            if current_number:
                if len(current_number) == 2:
                    new_string += current_number[::-1]
                else:
                    new_string += current_number
                current_number = ""
            new_string += char

    if current_number and len(current_number) == 2:
        new_string += current_number[::-1]
    else:
        new_string += current_number

    return new_string

def get_soprano_seed(soprano, soprano_seed, time_step = 0.25):
    
    # get last 64 sixteenth note events for melodygenerator to get next notes
    
    seed = []
    seed_length = 0
    total_steps = 0
    
    for event in reversed(soprano.flat.notesAndRests):
        if isinstance(event, note.Note):
            symbol = event.pitch.midi # 60
            # handle rests
        elif isinstance(event, note.Rest):
            symbol = "r"
            
            # convert the note/rest into time series notation
        steps = int(event.duration.quarterLength / time_step)
        seed_length += steps
        
        if seed_length < SEQUENCE_LENGTH:
            for step in range(steps):
                if step == (steps - 1):
                    seed.append(symbol)
                else:
                    seed.append("_")
        else:
            for step in range(SEQUENCE_LENGTH - total_steps):
                if step == SEQUENCE_LENGTH - total_steps - 1:
                    seed.append(symbol)
                else:
                    seed.append("_")
            reversed_encoded_seed = " ".join(map(str, seed))
            
            encoded_seed = reverse_numbers_in_string(reversed_encoded_seed[::-1])  # @UnusedVariable
            
        total_steps += steps
        
    reversed_encoded_seed = " ".join(map(str, seed))
            
    encoded_seed = reverse_numbers_in_string(reversed_encoded_seed[::-1])
    
    # append starting seed to encoded seed if encoded seed is not long enough
    if(total_steps < SEQUENCE_LENGTH):
        encoded_seed = ' '.join([soprano_seed, encoded_seed])
    
    # lower notes above C5 an octave so melodygenerator understands seed better
    altered_seed = []
    i = 0
    while i < len(encoded_seed):
        if encoded_seed[i:i + 2].isdigit():
            number = int(encoded_seed[i:i + 2])
            if number > 76:
                number -= 12
                while number > 76:
                    number -= 12  
                altered_seed.append(str(number))
            else:
                altered_seed.append(encoded_seed[i:i + 2])
            i += 2  # Move the index by 2 to skip the processed two-digit number
        else:
            altered_seed.append(encoded_seed[i])
            i += 1  # Move the index by 1 for non-numeric characters
    
    print(''.join(altered_seed))
    return ''.join(altered_seed)

def fix_range(soprano_melody):
    number_soprano_melody = []
    amount_of_numbers = 0

    i = 0
    while i < len(soprano_melody):
        if str(soprano_melody[i]).isdigit():
            num = soprano_melody[i]
            count = 0
            amount_of_numbers += 1
            while i + 1 < len(soprano_melody) and soprano_melody[i + 1] == '_':
                count += 1
                i += 1

            number_soprano_melody.extend([num] * (count + 1))
        i += 1
    
    
    number_soprano_melody = [int(num) for num in number_soprano_melody]
    
    total = sum(number_soprano_melody)
    average = int(total / len(number_soprano_melody))
    
    altered_soprano_melody = []
    
    # if majority of melody is under F#4, raise an octave
    if average < 67:
        for item in soprano_melody:
            if re.match(r'^[-+]?\d*$', item):  # Check if the item is a numeric string
                number = int(item)
                number += 12
                altered_soprano_melody.append(str(number))
            else:
                altered_soprano_melody.append(item)
                    
            
        return altered_soprano_melody
    
    for item in soprano_melody:
        if re.match(r'^[-+]?\d*$', item):  # Check if the item is a numeric string
            number = int(item)
            if(number < 65):
                number += 12
            altered_soprano_melody.append(str(number))
        else:
            altered_soprano_melody.append(item)
    
    return altered_soprano_melody

def append_soprano_melody(soprano, soprano_melody, step_duration = 0.25):
    
    start_symbol = None
    step_counter = 1
    
    for i, symbol in enumerate(soprano_melody): 
        # handle case in which we have a note/rest
        if symbol != "_" or i + 1 == len(soprano_melody):
            # ensure we're not dealing with note/rest beyond the first symbol
            if start_symbol is not None: 
                quarter_length_duration = step_duration * step_counter # 0.25 * 4
                        
                # handle rest
                if start_symbol == "r":
                    m21_event = note.Rest(quarterLength = quarter_length_duration)
                        
                # handle note
                else:
                    m21_event = note.Note(int(start_symbol), quarterLength = quarter_length_duration)
                        
                soprano.append(m21_event)
                        
                # reset step counter
                step_counter = 1
                        
            start_symbol = symbol
        # handle case in which we have a prolongation sign "_"
        else:
            step_counter += 1
            
    return soprano
                    
def main():
    
    # Create a stream for the four parts   
    soprano = stream.Part()
    alto = stream.Part()
    tenor = stream.Part()
    bass = stream.Part()
    index = 0
    chord_index = 0
    
    # Create a XML file and add the four parts
    xml_stream = stream.Score()
    
    for chord_name in symbol_chord_progression:
        
        degree, quality, inversion, secondary_dominant_numeral, duration = analyze_chord_symbol(chord_name, index, symbol_chord_progression)
        
        if quality != "":
            
            # set seed
            if index == 0:
                soprano_seed = soprano_beginning_seed
            else:
                soprano_seed = get_soprano_seed(soprano, soprano_beginning_seed)
            
            
            # set notes and soprano melody
            chord_notes = chord.Chord(chord_to_midi(degree, quality, inversion, secondary_dominant_numeral))
            soprano_melody, alto_note, tenor_note, bass_note = harmonize_chord(chord_notes, soprano_seed, quality, duration)
            
            # set note lengths
            alto_note.quarterLength = duration
            tenor_note.quarterLength = duration
            bass_note.quarterLength = duration
            
            # add chord under bass note
            bass_note.lyric = chord_name
            
            # signal end of each chord so soprano melody ends correctly
            soprano_melody.append("/")
            
            altered_soprano_melody = fix_range(soprano_melody)
            
            # last soprano melody changed to only one note
            if chord_index == len(symbol_chord_progression) - duration:
                altered_soprano_melody = ['72'] + ['_' for _ in range(1, len(altered_soprano_melody))]
                altered_soprano_melody[-1] = '/'
            
            print()
            print("soprano melody: " + str(altered_soprano_melody))
            print()
            print(str(int(float((chord_index + duration) / len(symbol_chord_progression)) * 100)) + "% complete")
            
            # append soprano melody
            soprano = append_soprano_melody(soprano, altered_soprano_melody)
            
            print ("-" * 80) 
                
            # append other voices
            alto.append(alto_note)
            tenor.append(tenor_note)
            bass.append(bass_note)
        
        index += 1
        chord_index += 1
    
    # Add the parts to the XML stream
    xml_stream.insert(0, soprano)
    xml_stream.insert(0, alto)
    xml_stream.insert(0, tenor)
    xml_stream.insert(0, bass)
    
    # Save the XML file
    xml_stream.write('xml', fp='harmonywithmelody.xml')

if __name__ == "__main__":
    main()