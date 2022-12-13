from flask import Flask, send_file
from flask import request
import joblib
import json
import pandas as pd
from eurybia import SmartDrift
import datetime
from sklearn.preprocessing import MinMaxScaler,StandardScaler

app = Flask(__name__)

model = joblib.load('./models/model.joblib')
data = pd.read_pickle('./datas/Country-data.pkl')
auc = pd.DataFrame(columns=['date', 'auc'])
pd.concat([auc, pd.DataFrame([[datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), 0.5]], columns=auc.columns)], axis=0)
print(auc)

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

@app.route("/add-data", methods=['POST'])
def add_data():
  Country = request.get_json()['Country']
  Health = request.get_json()['Health']
  Trade = request.get_json()['Trade']
  Finance = request.get_json()['Finance']
  
  global data
  
  if Country == None or Health == None or Trade == None or Finance == None:
    response = {"Error": "Please provide all the features"}
    status = 400
  else:
    new_row = pd.DataFrame([[Country, Health, Trade, Finance]], columns=data.columns)
    data = pd.concat([data, new_row], axis=0)
    response =  {"message": "Data added"}
    status = 200

  
  return app.response_class(
      response=json.dumps(response),
      status=status,
    )
  
@app.route("/get-report", methods=['GET'])
def get_report():
  global data
  global auc
  date = datetime.datetime.now()
  print(data)

  sd = SmartDrift(
    df_current=data.drop(['Country'], axis=1),
    df_baseline=data.drop(['Country'], axis=1),
  )
  sd.compile(
      full_validation=True,
      date_compile_auc=date,
  )
  sd.generate_report(output_file='reports/report-'  + date.strftime("%Y-%m-%d-%H-%M-%S") + '.html')
  
  print(f"auc before {auc}")
  new_row = pd.DataFrame([[date, sd.auc]], columns=auc.columns)
  auc = pd.concat([auc, new_row])
  print(f"auc after {auc}")
  
  return send_file('./reports/report-'  + date.strftime("%Y-%m-%d-%H-%M-%S") + '.html', mimetype='text/html', as_attachment=True), 200

@app.route("/get-auc", methods=['GET'])
def get_auc():
  global auc
  return app.response_class(
      response=json.dumps({'AUC': auc.to_dict()}),
      status=200,
    )
  

  
if __name__ == "__main__":
  app.run("0.0.0.0", port=3000)