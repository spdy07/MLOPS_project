import streamlit as st
import requests
import os

api = os.environ.get('BACKEND_URL')
# api = "http://localhost:3000"

def add_data(country, health, trade, finance):
  r = requests.post(api + '/add-data', json ={ "Country": country, "Health": health, "Trade": trade, "Finance": finance})
  # r = requests.post('http://localhost:3000/add-data', son ={ "health": health, "trade": trade, "finance": finance})
  return r.json(), r.status_code

st.title('MLOPS project')
st.markdown("## Add data ✚")

country = st.text_input("Country")
health = st.number_input("Health")
trade = st.number_input("Trade")
finance = st.number_input("Finance")

def main():
  if st.button('Add data'):
    response, status = add_data(country=country, health=health, trade=trade, finance=finance)
    if status == 400:
      st.error(f"Error : {response.get('Error')}")
    else:
      print(response)
      st.write(f"The data has been successfully added")

if __name__ == "__main__":
  main()