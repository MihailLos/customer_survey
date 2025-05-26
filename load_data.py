from airtable import Airtable
from datetime import datetime
import streamlit as st

# --- Параметры доступа к Airtable ---      
AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"] 

RESPONSE_FIELDS = [
    "q1", "q2", "q2_other", "q3_1", "q3_2", "q3_3",
    *[f"m{i}" for i in range(1, 10)],
    *[f"l{i}" for i in range(1, 10)],
    "q13", "q14", "q15", "q16", "q17", "q17_other",
    "q18", "q19", "q20", "q21", "q22", "q22_other",
    "q23", "q23_other", "q24", "q25", "q26", "q27"
]

def send_to_airtable(data_dict):
    airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
    data_dict["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    airtable.insert(data_dict)

def build_answers():
    answers = {}
    for key in RESPONSE_FIELDS:
        val = st.session_state.get(key, "")
        if isinstance(val, list):
            val = ", ".join(val)
        answers[key] = val
    answers["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return answers