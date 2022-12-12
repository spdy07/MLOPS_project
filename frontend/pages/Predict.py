import streamlit as st
import requests
import json
import os

api = os.environ.get('BACKEND_URL')


def predict(health, trade, finance):
  print(json.dumps({"Health": health, "Trade": trade, "Finance": finance}))
  r = requests.post(api + '/predict', json = {"Health": health, "Trade": trade, "Finance": finance})
  # r = requests.post('http://localhost:3000/predict', json = {"Health": health, "Trade": trade, "Finance": finance})
  
  return r.json(), r.status_code
  
st.title('MLOPS project')
st.markdown("## Predict 📈")

health = st.number_input("Health")
trade = st.number_input("Trade")
finance = st.number_input("Finance")
    
def main():
  if st.button('Predict'):
    print(health, trade, finance)
    prediction, status = predict(health, trade, finance)
    if status == 400:
      st.write(f"Error : {prediction.get('Error')}")
    else:
      st.write(f"The prediction is : {prediction.get('prediction')}")
  
if __name__ == "__main__":
  main()


