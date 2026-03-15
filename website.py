""" Creates the website which validates license plates"""

import re
from pathlib import Path

import streamlit as st
import pandas as pd
from unscrambler import normalize, char_replace
from unscrambler import substr_exact_match, rapid_fuzzymatching

#make sure there is no button when you start
if 'show_button' not in st.session_state:
    st.session_state['show_button'] = False

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
    """Initial checks for license plate basics"""
    # fir go through her checks
    msg = None
    if len(plate) > 7 or (len(plate) < 2 and len(plate) > 0):
        msg = f"{plate} is an invalid length"

    elif not plate.isalnum() and len(plate)>0:
        msg = f"{plate} has invalid characters"

    elif sum(c.isdigit() for c in plate) == 4 and sum(c.isalpha() for c in plate) == 2:
        msg = f"{plate} must be for Purple Heart Vessels, Disabled Person, or Disabled Veteran"

    elif sum(c.isdigit() for c in plate) == 5 and sum(c.isalpha() for c in plate) == 1:
        msg = f"{plate} must be for a commercial vehical"

    elif sum(c.isdigit() for c in plate) == 5 and sum(c.isalpha() for c in plate) == 2:
        msg = f"{plate} must be for a Disabled Person, or Disabled Veteran"

    elif bool(re.fullmatch(r"^\d{5}[a-zA-Z]\d$", plate)):
        msg = f"{plate} must be for a commercial vehical"
    # user normalized + decoded to catch any bad items in the plate
    elif any(item in plate.upper() for item in band_list):
        bad_item = next(item for item in band_list if item in plate.upper())
        msg = f"{plate} contains the restricted letter combination {bad_item}"
    return msg

def evaluate_plate(plate: str, list_words: list[str]) -> dict:
    """Evaluate the plate with the fuzzymatching"""
    normalized = normalize(plate)
    decoded = char_replace(normalized)
    cleaned = decoded[0]
    exct_match = substr_exact_match(cleaned, list_words)
    # print("Exact matches? ",exct_match
    if exct_match is not False:
        print("Substring matches?")
        print(exct_match)
        return "substring match", exct_match
    fuzz_res = rapid_fuzzymatching(decoded, list_words)
        # print("Fuzzy matching: ", fuzz_res)
    if fuzz_res is not None:
        print("Fuzzy matching score: ", fuzz_res[0][1])
        print(plate, " may contain the word ", fuzz_res[0][0])
        print()
        msg = ("fuzzmatch", fuzz_res[0][0], fuzz_res[0][1])
        return msg
    return None

#getting the files for the checking evil
plates_root = Path(__file__).resolve().parent  # -> License-Plates/
data_path = plates_root / "datacleaning" / "master_counts_scores.csv"

df_scores = pd.read_csv(data_path)
evil_list = df_scores['nospace'].tolist() # bad words list

# def check_evil(plate):
#     """Initial check"""
#     if plate in evil_list:
#         return "This plate contains a restricted word"
#     return "This plate does not contain a restricted word"

def button_output(plate):
    """Running the plate against our list"""
    if plate in evil_list:
        row = df_scores.loc[df_scores['nospace'] == plate]
        print(row)
        hate = list(row['hate_speech'])
        offensive = list(row['offensive_language'])
        total_count = list(row['count_words'])
        txt = f"""Your plate contains a word that appeared in
        {total_count} tweets marked as hatefull or offensive.
        This word appeared in tweets which {hate} people marked as
        hatefull and {offensive} marked as offensive.
        If all of these are zero, then it appeared in no tweets but was
        still captured by our hatefull algorithm."""
        return txt
    return"This plate does not contain a restricted word"

# Streamlit stuff
st.title("License Plate Tester 🚗")

tab1, tab2 = st.tabs(["Single Plate", "Batch CSV"])

# Single License Plate
with tab1:
     user_lic = st.text_input("Please write your desired license plate:")
     mesg = validation_rules(user_lic)

     if user_lic:
          if mesg is not None:
               st.write(mesg)
          else:
               matches = evaluate_plate(user_lic, evil_list)
               button_input = user_lic
               if matches is not None: 
                    
                    match_type = matches[0]
                    if match_type == "substring match":
                         st.write("This plate contains a restricted word.")
                         exact_msg = f"""
                         **Detected restricted word**
                         
                         - Detected word: {matches[1]}
                         - Detection method: exact match
                         """
                         
                    else:
                         st.write("This plate closely resembles a word or phrase that may be considered inappropriate.")
                         exact_msg = f"""
                         **Detected similarity**

                         - Possible match: {matches[1]}
                         - Similarity score: {matches[2]}%
                         - Detection method: similarity matching
                         """
                    #add a button for more information but only when it is restricted
                    
                    button_input = matches[1]
                    clicked = st.button("See More Information")
                    if clicked:
                         st.markdown(exact_msg)
                         st.write(button_output(button_input))
               else: 
                    st.write("This plate does not contain a restricted word")
               

# Batch License Plates
with tab2:
     # maybe we can provide them a template csv or something
    uploaded_lics = st.file_uploader("Upload csv of License Plates", type = "csv")

    if uploaded_lics is not None:
          input_df = pd.read_csv(uploaded_lics)
          if input_df.empty:
               st.write("The uploaded CSV is empty.")
          elif "plate" not in input_df.columns:
            # if not empty, check for correct format (we can add more if needed)
               st.write("CSV must contain a column called 'plate'.")
          else:
               decisions = []
               reasons = []
               notes = []
            
               for line in input_df['plate']:
                # 1. first check if violates basic rules
                    message = validation_rules(line)
                    dec = 'Y'
                    reason = 'N/A'
                    note = 'N/A'
                    if message is not None:
                         dec = "N"
                         reason = message
                         note = "n/a"
                    
                    # 2. check for any matches with unscrambler + evaluate function
                    else:
                    # have to fix this part later, temporary will work on this tmr
                         matches = evaluate_plate(line, evil_list)
                             
                         if matches is not None: 
                              dec = 'N'
                              match_type = matches[0]
                              if match_type == "substring match":
                                   reason = "This plate contains a restricted word."
                                   exact_msg = f"""The detected word is {matches[1]}. The detection method is exact match."""
                                   
                              else:
                                   reason = "This plate closely resembles a word or phrase that may be considered inappropriate."
                                   exact_msg = f"Plate closely resembles the restricted word '{matches[1]}' (similarity score: {matches[2]}%)."
                                   
                              tweet_info = button_output(matches[1])
                              
                              note = exact_msg + "\n" + tweet_info
                         
                    decisions.append(dec)
                    reasons.append(reason)
                    notes.append(note)
                         
               print("plate:", len(input_df["plate"]))
               print("decisions:", len(decisions))
               print("reasons:", len(reasons))
               print("notes:", len(notes))
                    
                    
               data = {'plate': input_df['plate'], 'approved?': decisions, 'reason': reasons, 'notes': notes}
               csv_df = pd.DataFrame(data)
               csv = csv_df.to_csv(index=False)
               
               # preview before download
               st.subheader("Results Preview")
               st.dataframe(csv_df)
               
               st.info("""Note: The decisions shown are generated by an automated screening tool and are intended to assist DMV staff. 
                          Final approval should follow official DMV policies and reviewer judgment.""")
               
               # Download button
               st.download_button(
                    label="Download processed CSV",
                    data=csv,
                    file_name="processed_output.csv",
                    mime="text/csv",
               )
                         