from airtable import Airtable
from datetime import datetime
import streamlit as st

# --- Параметры доступа к Airtable ---      
AIRTABLE_TABLE_NAME = 'Results'
AIRTABLE_API_KEY = st.secrets["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"]                

def send_to_airtable(data_dict):
    airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
    data_dict["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    airtable.insert(data_dict)
