import streamlit as st
import requests
import os

api = os.environ.get('BACKEND_URL')

def get_report():
  r = requests.get(api + '/get-report')
  return r

st.title('MLOPS project')
st.markdown("## Data drift 💾")

def main():
  if st.button('Get report'):
    response= get_report()
    if response.ok:
      file_data = response.content
      st.python("""
        with open('report.html', 'wb') as f:
          f.write(file_data)          
      """)
      st.download_button(label="Download report", data=file_data, file_name='report.html', mime='text/html')
      st.write(f"The file has been downloaded")
      st.write(f"Error : {response.get('Error')}")
    else:
      st.error(f"Coudn't get the report : {response.get('Error')}")
if __name__ == "__main__":
  main()
