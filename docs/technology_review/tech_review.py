
# Package 1: leetcoder encoder decoder
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3] / "leetspeak-encoder-decoder"))
# now import whatever module file the repo provides
import multilang

language_id = 'en'

print("=== Package 1: leetspeak decoder ===")
# Get and display the character replacement dictionary
char_replacement_dict = multilang.get_character_replacement_dict(language_id)
print(f"The character replacement dictionary for language '{language_id}' is: {char_replacement_dict}")

    # Get and display the language dictionary module
language_dict = multilang.get_language_dictionary_module(language_id)
print(f"The language dictionary for language  '{language_id}' is: {language_dict}")

# Test encoding and decoding
# test_text = "Hello, World!"
# test_text = "H3LL0!"
plate_cases = [
    "H3LL0"
    "H8TR",
    "A55MAN",
    "K1LLR",
    "GO2HELL",
]

# encoded_text = multilang.encode_leet(test_text, 'en')
decoded_list = []
for plate in plate_cases:
    decoded_text = multilang.decode_leet(plate, 'en')
    decoded_list.append(decoded_text)

# print(f"Encoded Text: {encoded_text}")
print(f"Decoded Text: {decoded_list}")


print()

# Package 2: rapid fuzz

# general rules: only letters, nums or spaces; number 0 is not allowed only O
# 1. normalize

import numpy as np
# Pandas DataFrames as table elements
import pandas as pd

PLATES_ROOT = Path(__file__).resolve().parents[2]   # -> License-Plates/
# DATA_PATH = PLATES_ROOT / "data" / "uniqueevilmasterdoc.csV"
DATA_PATH = PLATES_ROOT / "data" / "cleaned_evilwords.csv"


df = pd.read_csv(DATA_PATH)

# df = pd.read_csv('License-Plates/data/uniqueevilmasterdoc.csv')
# print(df.columns.tolist())
words_list = df['nospace'].tolist() # bad words list

# 1. Normalize (remove everything other than alphanumeric)
def normalize(plate):

    plate = plate.upper()
    filtered_plate = ''.join(filter(str.isalnum, plate))

    # var_dict = {'A': '4', 'B': '8', 'L': '1', 'E': '3', 'G': '9', 'I': '1', 'O': '0', 'S': '5', 'T': '7', 'Z': '2'}

    return filtered_plate

# 2. Single char variant replacement (visual encodings)
def char_replace(plate):
    var_dict = {'4': 'A', '8': 'B', '1':'I', '3':'E', '9': 'G', '5': 'S', '7':'T'}

    # Create a translation table
    table = str.maketrans(var_dict)
    result = plate.translate(table)

    return(result)  # Output: Hell0 w0rld

# 3. Look for exact substring matches in master list
def substr_exact_match(plate, words_list):
    # substring matching
    found = any(substring in plate.lower() for substring in words_list)

    if found: 
        res = [word for word in words_list if word in plate.lower()]
        return res
    #print("found: ", found)
    return found


# 4. Fuzzy match for similar words if exact match not found
from rapidfuzz import process as p1, fuzz as f1
def rapid_fuzzymatching(plate, words_list):
    # 1. to lower case + split by space?
    # 2. split up phrases to words? or can it auto find words?
    # 3. character replacement with dictionary?
    # 3. fuzzy match to find close enough word from master list?
    plate = plate.lower()
    ans = p1.extract(plate, words_list, scorer=f1.WRatio, limit=2)

    return ans

# Package 3: theFuzz

# 4. Fuzzy match for similar words if exact match not found
from thefuzz import process as p2, fuzz as f2
def thefuzz_fuzzymatching(plate, words_list):
    # 1. to lower case + split by space?
    # 2. split up phrases to words? or can it auto find words?
    # 3. character replacement with dictionary?
    # 3. fuzzy match to find close enough word from master list?
    plate = plate.lower()
    ans = p2.extract(plate, words_list, scorer=f2.WRatio, limit=2)

    return ans

# Testing functions
test_plates = ['H3LL', 'VTARDED', 'GTK1LR', 'BUTCH']

print("=== Package 2: RapidFuzz ===")
for test_plate in test_plates: 
    print("Test for plate: ", test_plate)
    norm = normalize(test_plate)
    print("Normalized: ",norm)

    decoded = char_replace(norm)
    print("Variants Replaced: ",decoded)

    exct_match = substr_exact_match(decoded, words_list)
    print("Exact matches? ",exct_match)

    if exct_match == False: 
        fuzz_res = rapid_fuzzymatching(decoded, words_list)
        print("Fuzzy matching: ", fuzz_res)
        print()
    else: 
        print("Word matches: ", exct_match)
        print()

print("=== Package 3: thefuzz ===")
for test_plate in test_plates: 
    print("Test for plate: ", test_plate)
    norm = normalize(test_plate)
    print("Normalized: ",norm)

    decoded = char_replace(norm)
    print("Variants Replaced: ",decoded)

    exct_match = substr_exact_match(decoded, words_list)
    print("Exact matches? ",exct_match)

    if exct_match == False: 
        fuzz_res = thefuzz_fuzzymatching(decoded, words_list)
        print("Fuzzy matching: ", fuzz_res)
        print()
    else: 
        print("Word matches: ", exct_match)
        print()



import time

print("=== Runtime Comparison ===")

test_plate = "BUTCH"
norm = normalize(test_plate)
decoded = char_replace(norm)

# Repeat many times to amplify difference
iterations = 1000

# RapidFuzz timing
start = time.time()
for _ in range(iterations):
    rapid_fuzzymatching(decoded, words_list)
end = time.time()
print("RapidFuzz time:", end - start)

# thefuzz timing
start = time.time()
for _ in range(iterations):
    thefuzz_fuzzymatching(decoded, words_list)
end = time.time()
print("thefuzz time:", end - start)
