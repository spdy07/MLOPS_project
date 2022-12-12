import streamlit as st
import requests
import os

api = os.environ.get('BACKEND_URL')

def add_data(country, child_mort, exports, health, imports, income, inflation, life_expec, total_fer, gdpp):
  r = requests.post(api + '/add-data', json ={"country": country, "child_mort": child_mort, "exports": exports, "health": health, "imports": imports, "income": income, "inflation": inflation, "life_expec": life_expec, "total_fer": total_fer, "gdpp": gdpp})
  # r = requests.post('http://localhost:3000/add-data', json ={"country": country, "child_mort": child_mort, "exports": exports, "health": health, "imports": imports, "income": income, "inflation": inflation, "life_expec": life_expec, "total_fer": total_fer, "gdpp": gdpp})
  return r.json(), r.status_code

st.title('MLOPS project')
st.markdown("## Data drift 💾")
