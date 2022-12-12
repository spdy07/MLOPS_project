from flask import Flask
from flask import request
import joblib
import json
import pandas as pd

app = Flask(__name__)

model = joblib.load('./models/model.joblib')

@app.route("/predict", methods=['POST'])
def model_predict():
  Health = request.get_json()['Health']
  Trade = request.get_json()['Trade']
  Finance = request.get_json()['Finance']
  if Health == None or Trade == None or Finance == None:
    return json.dumps({"Error": "Please provide all the features"}), 400
  
  pred =  model.predict([[Health, Trade, Finance]])[0]
  status = 200
  if pred == 0:
    response = {"prediction": "might need help"}
  elif pred == 1:
    response = {"prediction":  "need help"}
  elif pred == 2:
    response = {"prediction": "don't need help"}
  else:
    response = {"Error"}
    status = 500
  return app.response_class(
    response=json.dumps(response),
    status=status,
  )

data = pd.read_csv('./datas/Country-data.csv')
@app.route("/add-data", methods=['POST'])
def add_data():
  country = request.get_json()['country']
  child_mort = request.get_json()['child_mort']
  exports = request.get_json()['exports']
  health = request.get_json()['health']
  imports = request.get_json()['imports']
  income = request.get_json()['income']
  inflation = request.get_json()['inflation']
  life_expec = request.get_json()['life_expec']
  total_fer = request.get_json()['total_fer']
  gdpp = request.get_json()['gdpp']
  
  global data
  
  if country == None or child_mort == None or exports == None or health == None or imports == None or income == None or life_expec == None or total_fer == None or gdpp == None:
    response = {"Error": "Please provide all the features"}
    status = 400
  else:
    new_row = pd.DataFrame([[country, child_mort, exports, health, imports, income, inflation, life_expec, total_fer, gdpp]], columns=data.columns)
    data = data.append(new_row, ignore_index=True)
    response =  {"message": "Data added"}
    status = 200

  
  return app.response_class(
      response=json.dumps(response),
      status=status,
    )
  
if __name__ == "__main__":
    app.run("0.0.0.0", port=3000)