import streamlit as st
import requests
import os

api = os.environ.get('BACKEND_URL')

def add_data(health, trade, finance):
  r = requests.post(api + '/add-data', json ={ "health": health, "trade": trade, "finance": finance})
  # r = requests.post('http://localhost:3000/add-data', son ={ "health": health, "trade": trade, "finance": finance})
  return r.json(), r.status_code

st.title('MLOPS project')
st.markdown("## Add data ✚")

health = st.number_input("Health")
trade = st.number_input("Trade")
finance = st.number_input("Finance")

def main():
  if st.button('Add data'):
    response, status = add_data(health=health, trade=trade, finance=finance)
    if status == 400:
      st.error(f"Error : {response.get('Error')}")
    else:
      print(response)
      st.write(f"The data has been added : {response.get('message')}")

if __name__ == "__main__":
  main()