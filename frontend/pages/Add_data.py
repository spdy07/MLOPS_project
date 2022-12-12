import streamlit as st
import requests
import os

api = os.environ.get('BACKEND_URL')

def add_data(country, child_mort, exports, health, imports, income, inflation, life_expec, total_fer, gdpp):
  r = requests.post(api + '/add-data', json ={"country": country, "child_mort": child_mort, "exports": exports, "health": health, "imports": imports, "income": income, "inflation": inflation, "life_expec": life_expec, "total_fer": total_fer, "gdpp": gdpp})
  # r = requests.post('http://localhost:3000/add-data', json ={"country": country, "child_mort": child_mort, "exports": exports, "health": health, "imports": imports, "income": income, "inflation": inflation, "life_expec": life_expec, "total_fer": total_fer, "gdpp": gdpp})
  return r.json(), r.status_code

st.title('MLOPS project')
st.markdown("## Add data ✚")

country = st.text_input("Country")
child_mort = st.number_input("Child mortality")
exports = st.number_input("Exports")
health = st.number_input("Health")
imports = st.number_input("Imports")
income = st.number_input("Income")
inflation = st.number_input("Inflation")
life_expec = st.number_input("Life expectancy")
total_fer = st.number_input("Total fertility")
gdpp = st.number_input("GDP per capita")

def main():
  if st.button('Add data'):
    response, status = add_data(country, child_mort, exports, health, imports, income, inflation, life_expec, total_fer, gdpp)
    if status == 400:
      st.write(f"Error : {response.get('Error')}")
    else:
      print(response)
      st.write(f"The data has been added : {response.get('message')}")

if __name__ == "__main__":
  main()