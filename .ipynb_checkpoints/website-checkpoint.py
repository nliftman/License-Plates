""" Creates the website which validates license plates"""

import re

import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from unscrambler import normalize, char_replace
from unscrambler import substr_exact_match, rapid_fuzzymatching

band_list = ['ABM', 'ANO', 'APE', 'ARS', 'ASB', 'ASS', 'BAD', 'BAG',
             'BED', 'BRA', 'BUN', 'BUT', 'BVD', 'CHP', 'CIA',
             'COC', 'COK', 'CON', 'COP', 'CQC', 'CQK', 'CQN', 'CUL',
             'CUM', 'CUN', 'CUR', 'CUZ', 'DAG', 'DAM', 'DDT',
             'DIC', 'DIE', 'DIK', 'DOA', 'DUD', 'DUF', 'DUM', 'DUN',
             'FAG', 'FAN', 'FAT', 'FBI' , 'FCK', 'FKU', 'FOC',
             'FOK', 'FQC', 'FQK', 'FQU', 'FUC', 'FUD', 'FUG', 'FUK',
             'FUN', 'FUX', 'FUY', 'GAT', 'GAY', 'GEE', 'GOD',
             'GQD', 'GUT', 'HAG', 'HAM', 'HEL', 'HEN', 'HIC', 'HIK',
             'HIV', 'HOG', 'HOR', 'HQR', 'JAP', 'JAZ', 'JEW',
             'JIG', 'KIK', 'KKK', 'KOC', 'KOK', 'KON', 'KOX', 'KQC',
             'KQK', 'KQN', 'KQX', 'KYK', 'LAY', 'LSD', 'MEX',
             'NAG', 'NGR', 'NIG', 'NIP', 'NUN', 'OVA', 'PEA', 'PEE',
             'PEW', 'PIG', 'PIS', 'POT', 'POW', 'PST', 'PUD',
             'PUS', 'PYS', 'QVA', 'RAG', 'RAT', 'RAW', 'RUT', 'SAC',
             'SAK', 'SAM', 'SEX', 'SHT', 'SIF', 'SIN', 'SLA',
             'SOB', 'SOT', 'SQB', 'SUC', 'SUK', 'SUR', 'SUX', 'TIT',
             'TUB', 'UCK', 'UPP', 'UPU', 'URN', 'URP', 'USB',
             'USR', 'VUC', 'VUK', 'VUX', 'WAD', 'WOP', 'WQP', 'YEP', 'YID']

def validation_rules(plate):
    # fir go through her checks
    msg = None
    if len(plate) > 7 or len(plate) < 2:
        msg = plate + "is an invalid length"

    elif not plate.isalnum() and len(plate)>0:
        msg = plate + "has invalid characters"

    elif sum(c.isdigit() for c in plate) == 4 and sum(c.isalpha() for c in plate) == 2:
        msg = plate + "must be for Purple Heart Vessels, Disabled Person, or Disabled Veteran"

    elif sum(c.isdigit() for c in plate) == 5 and sum(c.isalpha() for c in plate) == 1:
        msg = plate + "must be for a commercial vehical"

    elif sum(c.isdigit() for c in plate) == 5 and sum(c.isalpha() for c in plate) == 2:
        msg = plate +  "must be for a Disabled Person, or Disabled Veteran"

    elif bool(re.fullmatch(r"^\d{5}[a-zA-Z]\d$", plate)):
        msg = plate + "must be for a commercial vehical"
    # user normalized + decoded to catch any bad items in the plate
    elif any(item in plate.upper() for item in band_list):
        bad_item = next(item for item in band_list if item in plate.upper())
        msg = plate + "contains the restricted letter combination", bad_item
    return msg


def evaluate_plate(plate: str, words_list: list[str]) -> dict:
    normalized = normalize(plate)
    decoded = char_replace(normalized)
    cleaned = decoded[0]
    exct_match = substr_exact_match(cleaned, words_list)
    # print("Exact matches? ",exct_match
    if exct_match is not False:
        print("Substring matches?")
        print(exct_match)
        return "found exact substring match: " + exct_match
    
    else: # exct_match is False
        fuzz_res = rapid_fuzzymatching(decoded, words_list)
        # print("Fuzzy matching: ", fuzz_res)

        if fuzz_res is not None:
            print("Fuzzy matching score: ", fuzz_res[0][1])
            print(plate, " contains the word ", fuzz_res[0][0])
            print()
            msg = plate + " contains the word " + fuzz_res[0][0] + " (score: " + str(fuzz_res[0][1]) + ")"
            return msg
        else:
            return "No Fuzzy Matches"


# Streamlit stuff
st.title("License Plate Tester 🚗")

tab1, tab2 = st.tabs(["Single Plate", "Batch CSV"])

PLATES_ROOT = Path(__file__).resolve().parent  # -> License-Plates/
DATA_PATH = PLATES_ROOT / "datacleaning" / "cleaned_evilwords.csv"

df = pd.read_csv(DATA_PATH)
words_list = df['nospace'].tolist() # bad words list

# Single License Plate
with tab1:
    user_lic = st.text_input("Please write your desired license plate:")
    msg = validation_rules(user_lic)

    if msg is not None:
        st.write(msg)
    else:
        matches = evaluate_plate(user_lic, words_list)
        st.write(matches)
     # CONTINUE WITH REST OF SCORING STUFF HERE 
     
     
    clicked = st.button("See More Information")

    if(clicked):
        st.write("This is the more info")
          
# Batch License Plates
with tab2:
     # maybe we can provide them a template csv or something
    uploaded_lics = st.file_uploader("Upload csv of License Plates", type = "csv")

    if uploaded_lics is not None:
        input_df = pd.read_csv(uploaded_lics)

        if input_df.empty:
            st.write("The uploaded CSV is empty.")
               
        elif "plate" not in input_df.columns: # if not empty, check for correct format (we can add more if needed)
            st.write("CSV must contain a column called 'plate'.")
               
        else:
            decisions = []
            reasons = []
            scores = []
            for plate in input_df['plate']: 
                    # 1. first check if violates basic rules
                msg = validation_rules(plate)
                if msg is not None:
                    decisions.append("Rejected")
                    reasons.append(msg)
                    scores.append("n/a")
                    # 2. check for any matches with unscrambler + evaluate function
                else:
                         # have to fix this part later, temporary will work on this tmr
                    result = evaluate_plate("plate")
                    decisions.append("???")
                    reasons.append(result)
                    scores.append("n/a")
                         
                         
                    
          
          