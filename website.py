import re

import streamlit as st
import pandas as pd
import numpy as np



band_list = ['ABM', 'ANO', 'APE', 'ARS', 'ASB', 'ASS', 'BAD', 'BAG', 'BED', 'BRA', 'BUN', 'BUT', 'BVD', 'CHP', 'CIA', 
             'COC', 'COK', 'CON', 'COP', 'CQC', 'CQK', 'CQN', 'CUL', 'CUM', 'CUN', 'CUR', 'CUZ', 'DAG', 'DAM', 'DDT', 
             'DIC', 'DIE', 'DIK', 'DOA', 'DUD', 'DUF', 'DUM', 'DUN', 'FAG', 'FAN', 'FAT', 'FBI' , 'FCK', 'FKU', 'FOC',
             'FOK', 'FQC', 'FQK', 'FQU', 'FUC', 'FUD', 'FUG', 'FUK', 'FUN', 'FUX', 'FUY', 'GAT', 'GAY', 'GEE', 'GOD',
             'GQD', 'GUT', 'HAG', 'HAM', 'HEL', 'HEN', 'HIC', 'HIK', 'HIV', 'HOG', 'HOR', 'HQR', 'JAP', 'JAZ', 'JEW',
             'JIG', 'KIK', 'KKK', 'KOC', 'KOK', 'KON', 'KOX', 'KQC', 'KQK', 'KQN', 'KQX', 'KYK', 'LAY', 'LSD', 'MEX',
             'NAG', 'NGR', 'NIG', 'NIP', 'NUN', 'OVA', 'PEA', 'PEE', 'PEW', 'PIG', 'PIS', 'POT', 'POW', 'PST', 'PUD',
             'PUS', 'PYS', 'QVA', 'RAG', 'RAT', 'RAW', 'RUT', 'SAC', 'SAK', 'SAM', 'SEX', 'SHT', 'SIF', 'SIN', 'SLA', 
             'SOB', 'SOT', 'SQB', 'SUC', 'SUK', 'SUR', 'SUX', 'TIT', 'TUB', 'UCK', 'UPP', 'UPU', 'URN', 'URP', 'USB',
             'USR', 'VUC', 'VUK', 'VUX', 'WAD', 'WOP', 'WQP', 'YEP', 'YID']

st.title("License Plate Tester 🚗")

user_lic = st.text_input("Please write your desired license plate:")


if len(user_lic) > 7 and len(user_lic) < 2:
    st.write(user_lic, "is an invalid length")

if not user_lic.isalnum() and len(user_lic)>0:
    st.write(user_lic, "has invalid characters")

for item in band_list:
    if item in  user_lic.upper():
        st.write(user_lic, "contains the in restricted letter combination", item)

if sum(c.isdigit() for c in user_lic) == 4 and sum(c.isalpha() for c in user_lic) == 2:
     st.write(user_lic, "must be for Purple Heart Vessels, Disabled Person, or Disabled Veteran")

if sum(c.isdigit() for c in user_lic) == 5 and sum(c.isalpha() for c in user_lic) == 1:
     st.write(user_lic, "must be for a commercial vehical")

if sum(c.isdigit() for c in user_lic) == 5 and sum(c.isalpha() for c in user_lic) == 2:
     st.write(user_lic, "must be for a Disabled Person, or Disabled Veteran")

if bool(re.fullmatch(r"^\d{5}[a-zA-Z]\d$", user_lic)):
     st.write(user_lic, "must be for a commercial vehical")


uploaded_lics = st.file_uploader("Upload csv of License Plates", type = "csv")