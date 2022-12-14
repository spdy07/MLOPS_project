import streamlit as st
import requests
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit.components.v1 as components

api = os.environ.get('BACKEND_URL')
# api = "http://localhost:3000"

def get_report():
  r = requests.get(api + '/get-report')
  return r

def get_auc():
  r = requests.get(api + '/get-auc')
  r = r.json()
  r = r["AUC"]
  df = pd.DataFrame(r)
  return df
  

st.title('MLOPS project')
st.markdown("## Data drift 💾")

auc = get_auc()
# st.write(auc)
st.line_chart(auc.set_index('date'))


def main():
  if st.button('Generate report'):
    response= get_report()
    if response.ok:
      file_data = response.text.encode('utf-8')
      st.download_button(label="Download report", data=file_data, file_name='report.html', mime='text/html')
      st.write(f"The file has been downloaded")
      components.html(response.text, height=500)
    else:
      st.error(f"Coudn't get the report : {response.get('Error')}")
if __name__ == "__main__":
  main()
