'''
Created on Aug 17, 2023

@author: dillontsang
'''
from music21 import *

# Define the chord progression
symbol_chord_progression = ['i', '_', '_', '_', 'V65', '_', '_', '_', 'i', '_', 'ii', '_', 'I64', '_', 'V7', '_', 'I', '_', 
                            '_', '_', 'i', '_', '_', '_', 'V43/VI', '_', '_', '_', 'VI', 'i64', 'vii-7', 'V65', 'i', '_', 
                            'ii=65', '_', 'i64', '_', 'V', '_', 'i', '_', 'V/iv', '_', 'N6', '_', '_', '_', 'V/iv', '_', 
                            '_', '_', 'N6', '_', '_', '_', 'V/iv', '_', 'iv', '_', 'V65/III', '_', '_', 'III', 'VI65', 'ii-', 
                            'V65', 'i', 'ii=43', '_', 'i64', 'ii=65', 'i64', '_', 'V7', '_', 'i', '_', '_', '_', 'V65', '_', 
                            '_', '_', 'i', '_', '_', '_', 'V7', '_', '_', '_', 'i', '_', '_', '_', 'V7', '_', '_', '_', 'i', 
                            '_', '_', '_']
chord_progression = []

def roman_to_int(roman):
        roman_numerals = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vii': 7,
                      'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}

        return roman_numerals.get(roman, roman)

def analyze_chord_symbol(chord_symbol):
          
    roman_numeral_end = 0
    triad_or_seventh = 0
    inversion_end = 0
    inversion = 0
    secondary_dominant_numeral = 0
        
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
            quality = 'hd'
            remainder = chord_symbol[roman_numeral_end + 1:]
    
    # check inversion
    if remainder != "":
        if remainder[:2].isdigit():
            inversion_end = 2
        elif remainder[:1].isalpha():
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
            
    # deal with dominant
        if quality == 'M' and triad_or_seventh == 1:
            quality = 'D'
            
    # secondary dominant
    if remainder[inversion_end:] != "":
        secondary_dominant_numeral = remainder[inversion_end + 1:]
        
    
    print("roman numeral: " + str(roman_to_int(roman_numeral)))
    print("quality: " + str(quality))
    print("inversion: " + str(inversion))
    print("chord or seventh: " + str(triad_or_seventh))
    print("secondary dominant roman numeral: " + str(roman_to_int(secondary_dominant_numeral)))
    print()
    return roman_numeral, quality, inversion, triad_or_seventh, secondary_dominant_numeral

    
def chord_to_midi(chord_name):
        note_mapping = {
            'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63, 'Eb': 63,
            'E': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68,
            'Ab': 68, 'A': 69, 'A#': 70, 'Bb': 70, 'B': 71
        }
        root_note = chord_name[:-1]
        chord_type = chord_name[-1]
        
        root_midi = note_mapping.get(root_note)
        if root_midi is None:
            return None
        
        chord_intervals = {
            'M': [0, 4, 7],
            'm': [0, 3, 7],
            '7': [0, 4, 7, 10],
            # Add more chord types and intervals as needed
        }
        
        intervals = chord_intervals.get(chord_type)
        if intervals is None:
            return None
        
        chord_midi = [root_midi + interval for interval in intervals]
        return chord_midi


# Define the four-part harmonization rules

def harmonize_chord(chord):
    soprano_note = chord[-1]
    alto_note = chord[-2]
    tenor_note = chord[-3]
    bass_note = chord[0]
    
    return soprano_note, alto_note, tenor_note, bass_note


def main():
    
    for symbol in symbol_chord_progression:
        # print(symbol)
        roman_numeral, quality, inversion, triad_or_seventh, secondary_dominant_numeral = analyze_chord_symbol(symbol)
        
        # chord_progression.append()
    
    # Create a stream for the four parts   
    soprano = stream.Part()
    alto = stream.Part()
    tenor = stream.Part()
    bass = stream.Part()
    
    # Create a MIDI file and add the four parts
    midi_stream = stream.Score()
    
    for chord_name in chord_progression:
        print(chord_to_midi(chord_name))
        
        
        soprano_note, alto_note, tenor_note, bass_note = harmonize_chord(chord.Chord(chord_to_midi(chord_name)))
        print(soprano_note)
        print(alto_note)
        print(tenor_note)
        print(bass_note)
        
        soprano_note.duration.type = 'quarter'
        alto_note.duration.type = 'quarter'
        tenor_note.duration.type = 'quarter'
        bass_note.duration.type = 'quarter'
        
        soprano.append(soprano_note)
        alto.append(alto_note)
        tenor.append(tenor_note)
        bass.append(bass_note)
    
    # Add the parts to the MIDI stream
    midi_stream.insert(0, soprano)
    midi_stream.insert(0, alto)
    midi_stream.insert(0, tenor)
    midi_stream.insert(0, bass)
    
    # Save the MIDI file
    midi_stream.write('midi', fp='harmony.midi')

if __name__ == "__main__":
    main()