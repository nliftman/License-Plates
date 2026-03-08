"""Creates multiple functions to assist in unscrambling
license plates."""
from pathlib import Path

# 1. normalize
from rapidfuzz import process as p1, fuzz as f1

import re
# Pandas DataFrames as table elements
import pandas as pd

PLATES_ROOT = Path(__file__).resolve().parent  # -> License-Plates/

print(PLATES_ROOT)
# DATA_PATH = PLATES_ROOT / "data" / "uniqueevilmasterdoc.csV"
DATA_PATH = PLATES_ROOT / "datacleaning" / "cleaned_evilwords.csv"

DATA_PATH2 = PLATES_ROOT / "data" / "applications.csv"

df = pd.read_csv(DATA_PATH)
words_list = df['nospace'].tolist() # bad words list
df2 = pd.read_csv(DATA_PATH2)
plates_list = df2['plate'].tolist() # plates list
decisions_list = df2['status'].tolist()

# 1. Normalize (remove everything other than alphanumeric)
def normalize(plate):
    """ Normalize (remove everything other than alphanumeric) """
    plate = plate.upper()
    cleaned = cleaned = ''.join(c for c in plate if c.isalnum() or c == " ")
    # words = cleaned.split()
    return cleaned

# 2. Single char variant replacement (visual encodings)
def char_replace(plate):
    """ single variant replacement """
    var_dict = {'0': 'O', '4': 'A', '8': 'B', '1':'I', '3':'E', '9': 'G', '5': 'S', '7':'T'}
    # Create a translation table
    table = str.maketrans(var_dict)
    result = plate.translate(table)
    # split by space (if there is space)
    tokens = result.split()
    no_space = result.replace(" ", "")
    return no_space, tokens  # return nonsplit + split tokens

# 3. Look for exact substring matches in master list
def substr_exact_match(plate, words_list):
    """ substring matching """
    found = any(substring in plate.lower() for substring in words_list)
    if found:
        res = [word for word in words_list if word in plate.lower()]
        return res[0]
    #print("found: ", found)
    return found

# 4. Fuzzy match for similar words if exact match not found
def rapid_fuzzymatching(plate, words_list):
    """Fuzzy matching similar words"""
    # 1. to lower case + split by space?
    # 2. split up phrases to words? or can it auto find words?
    # 3. character replacement with dictionary?
    # 3. fuzzy match to find close enough word from master list?
    nospace = plate[0].lower()
    tokens = plate[1]
    threshold = 80
    # if plate has no space:
    if len(tokens) > 1:
        full_extract = p1.extract(nospace, words_list, scorer=f1.WRatio, limit=1)
        # threshold set for minimum score for match (can change this)
        if full_extract[0][1] >= threshold:
            print(full_extract, " is a match for ", nospace)
            return full_extract

    # if plate has space, go through tokens
    else:
        for token in tokens:
            tok1 = p1.extract(token.lower(), words_list, scorer=f1.WRatio, limit=1)
            if tok1[0][1] > threshold:
                return tok1
            tok2 = p1.extract(token.lower(), words_list, scorer=f1.WRatio, limit=1)
            if  tok2[0][1] > threshold:
                return tok2
    # split plate into 2 tokens to check if meets fuzzymatching score for similarity
    for i in range(1, len(nospace)):
        left = nospace[:i]
        right = nospace[i:]
        # only fuzzymatch if left/right is at least of length 3 to avoid garbage
        if len(left) >= 4:
            left_extract = p1.extract(left, words_list, scorer=f1.WRatio, limit=1)
            if left_extract[0][1] > threshold:
                print(left_extract, " is a match for ", left)
                return left_extract
        if len(right) >= 4:
            right_extract = p1.extract(right, words_list, scorer=f1.WRatio, limit=1)
            if right_extract[0][1] > threshold:
                print(right_extract, " is a match for ", right)
                return right_extract
        # print("score ", ans[0][1],"for ", ans[0][0] , " is too low")
    return None


# # Testing
# test_plates = ['H3LL', 'VTARDED', 'GTK1LR', 'BUTCH']

# print("=== Package 2: RapidFuzz ===")
# for test_plate in test_plates:
#     print("Test for plate: ", test_plate)
#     norm = normalize(test_plate)
#     print("Normalized: ",norm)

#     decoded = char_replace(norm)
#     print("Variants Replaced: ",decoded)

#     exct_match = substr_exact_match(decoded, words_list)
#     print("Exact matches? ",exct_match)

#     if exct_match == False:
#         fuzz_res = rapid_fuzzymatching(decoded, words_list)
#         print("Fuzzy matching: ", fuzz_res)
#         print()
#     else:
#         print("Word matches: ", exct_match)
#         print()

# Testing

band_list = ['ABM', 'ANO', 'APE', 'ARS', 'ASB', 'ASS',
             'BAD', 'BAG', 'BED', 'BRA', 'BUN', 'BUT', 'BVD', 'CHP', 'CIA',
             'COC', 'COK', 'CON', 'COP', 'CQC', 'CQK', 'CQN', 'CUL', 'CUM', 
             'CUN', 'CUR', 'CUZ', 'DAG', 'DAM', 'DDT',
             'DIC', 'DIE', 'DIK', 'DOA', 'DUD', 'DUF', 'DUM', 'DUN', 'FAG',
             'FAN', 'FAT', 'FBI' , 'FCK', 'FKU', 'FOC',
             'FOK', 'FQC', 'FQK', 'FQU', 'FUC', 'FUD', 'FUG', 'FUK', 'FUN',
             'FUX', 'FUY', 'GAT', 'GAY', 'GEE', 'GOD',
             'GQD', 'GUT', 'HAG', 'HAM', 'HEL', 'HEN', 'HIC', 'HIK', 'HIV',
             'HOG', 'HOR', 'HQR', 'JAP', 'JAZ', 'JEW',
             'JIG', 'KIK', 'KKK', 'KOC', 'KOK', 'KON', 'KOX', 'KQC', 'KQK',
             'KQN', 'KQX', 'KYK', 'LAY', 'LSD', 'MEX',
             'NAG', 'NGR', 'NIG', 'NIP', 'NUN', 'OVA', 'PEA', 'PEE', 'PEW',
             'PIG', 'PIS', 'POT', 'POW', 'PST', 'PUD',
             'PUS', 'PYS', 'QVA', 'RAG', 'RAT', 'RAW', 'RUT', 'SAC', 'SAK',
             'SAM', 'SEX', 'SHT', 'SIF', 'SIN', 'SLA',
             'SOB', 'SOT', 'SQB', 'SUC', 'SUK', 'SUR', 'SUX', 'TIT', 'TUB',
             'UCK', 'UPP', 'UPU', 'URN', 'URP', 'USB',
             'USR', 'VUC', 'VUK', 'VUX', 'WAD', 'WOP', 'WQP', 'YEP', 'YID']










test_plates = ['LDYNBLU',
'LIL515O',
'AHHBLUE',
'ALDRG59',
'LUVIN',
'AIR4MND',
'NVW3N17',
'LGLYRED',
'NOTTYPB',
'ASEWERG',
'LTLBLUE',
'LAVYBLU',
'LKB4UGO',
'ARMY13B',
'442RUST',
'LYTLRED',
'AGUAYOG',
'LOT8GAS',
'LV2SLPN',
'NVRGIVN']

decisions = []
notes = []

print("=== Package 2: RapidFuzz ===")
for i, test_plate in enumerate(plates_list):
    # print("Test for plate: ", test_plate)
    norm_plate = normalize(test_plate)
    # print("Normalized: ",norm)

    decoded_plate = char_replace(norm_plate)
    cleaned_plate = decoded_plate[0]
    # print("Variants Replaced: ",decoded)
    # fir go through her checks
    if len(test_plate) > 7 or len(test_plate) < 2:
        # print(test_plate, "is an invalid length")
        decisions.append("N")
        notes.append("invalid length")

    elif not test_plate.isalnum() and len(test_plate)>0:
        # print(test_plate, "has invalid characters")
        decisions.append("N")
        notes.append("invalid characters")

    elif sum(c.isdigit() for c in test_plate) == 4 and sum(c.isalpha() for c in test_plate) == 2:
        # print(test_plate, "must be for Purple Heart Vessels,
        # Disabled Person, or Disabled Veteran")
        decisions.append("N")
        notes.append("must be for Purple Heart Vessels, Disabled Person, or Disabled Veteran")

    elif sum(c.isdigit() for c in test_plate) == 5 and sum(c.isalpha() for c in test_plate) == 1:
        # print(test_plate, "must be for a commercial vehical")
        decisions.append("N")
        notes.append("must be for commerical vehicle")

    elif sum(c.isdigit() for c in test_plate) == 5 and sum(c.isalpha() for c in test_plate) == 2:
        # print(test_plate, "must be for a Disabled Person, or Disabled Veteran")
        decisions.append("N")
        notes.append("must be for disabled person or veteran")

    elif bool(re.fullmatch(r"^\d{5}[a-zA-Z]\d$", test_plate)):
        # print(test_plate, "must be for a commercial vehical")
        decisions.append("N")
        notes.append("must be for commerical vehicle")

    # user normalized + decoded to catch any bad items in the plate
    elif any(item in cleaned_plate.upper() for item in band_list):
        bad_item = next(item for item in band_list if item in cleaned_plate.upper())
        # print(decoded_plate, "contains the restricted letter combination", bad_item)
        decisions.append("N")
        note = "contains the restricted letter combination" + bad_item
        notes.append(note)

    # this now goes on to substring match + fuzz matching (if needed)
    else:
        exct_match = substr_exact_match(cleaned_plate, words_list)
        # print("Exact matches? ",exct_match)

        if exct_match == False:
            fuzz_res = rapid_fuzzymatching(decoded_plate, words_list)
            # print("Fuzzy matching: ", fuzz_res)
            # print()
            if fuzz_res is not None:
                decisions.append("N")
                notes.append(fuzz_res)
            else:
                decisions.append("Y")
                notes.append("Approved")
        else:
            # print("Word matches: ", exct_match)
            # print()
            decisions.append("N")
            notes.append(exct_match)

# dff = pd.DataFrame({
#     "plate": test_plates,
#     "our decision": decisions,
#     "notes": notes
# })
# print(dff)



df2['our decision'] = decisions
df2['notes'] = notes

filtered_df = df2[df2['status'] != df2['our decision']]
filtered_df.to_csv("unmatched.csv", index=False)

df2.to_csv("testing.csv", index=False)

num_tot = len(df2)
num_cor = num_tot - len(filtered_df)
print(num_cor/num_tot)

unique_notes = df2['notes'].astype(str).unique()
print(unique_notes)
