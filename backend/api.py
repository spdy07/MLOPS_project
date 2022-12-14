from flask import Flask, send_file
from flask import request
import joblib
import json
import pandas as pd
from eurybia import SmartDrift
import datetime
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import mysql.connector
import os


app = Flask(__name__)

db = os.environ.get('DB')

model = joblib.load('./models/model.joblib')

def connect_db():
  cnx = mysql.connector.connect(
    host= "db",
    password="password",
  )
  cursor = cnx.cursor()
  return cnx, cursor

def send_data_to_db(cnx, cursor):
  cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")
  cnx.commit()
  cnx.database = "mydb"
  df = pd.read_pickle('./datas/Country-data.pkl')
  query = "CREATE TABLE DF (Country VARCHAR(255), Health FLOAT, Trade FLOAT, Finance FLOAT)"
  cursor.execute(query)

  for _, row in df.iterrows():
    cursor.execute("INSERT INTO DF (Country, Health, Trade, Finance) VALUES (%s, %s, %s, %s)", (row['Country'], row['Health'], row['Trade'], row['Finance']))
  cnx.commit()
  
def first_auc(cnx, cursor):
  data = pd.read_pickle('./datas/Country-data.pkl')
  query = "CREATE TABLE AUC (date VARCHAR(255), auc FLOAT)"
  cursor.execute(query)
  cnx.commit()
  
  date = datetime.datetime.now()

  sd = SmartDrift(
    df_current=data.drop(['Country'], axis=1),
    df_baseline=data.drop(['Country'], axis=1),
  )
  sd.compile(
      full_validation=True,
      date_compile_auc=date,
  )
  sd.generate_report(output_file='reports/report-'  + date.strftime("%Y-%m-%d-%H-%M-%S") + '.html')
  
  cursor.execute("INSERT INTO AUC (date, auc) VALUES (%s, %s)", (date.strftime("%Y-%m-%d-%H-%M-%S"), sd.auc))
  cnx.commit()
  
cnx, cursor = connect_db()
send_data_to_db(cnx, cursor)
first_auc(cnx, cursor)
  
  

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
  
  # global data
  
  if Country == None or Health == None or Trade == None or Finance == None:
    response = {"Error": "Please provide all the features"}
    status = 400
  else:
    query = "INSERT INTO DF (Country, Health, Trade, Finance) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (Country, Health, Trade, Finance))
    cnx.commit()
    response =  {"message": "Data added"}
    status = 200

  
  return app.response_class(
      response=json.dumps(response),
      status=status,
    )
  
@app.route("/get-report", methods=['GET'])
def get_report():
  data = pd.read_sql("SELECT * FROM DF", cnx)
  date = datetime.datetime.now()

  sd = SmartDrift(
    df_current=data.drop(['Country'], axis=1),
    df_baseline=data.drop(['Country'], axis=1),
  )
  sd.compile(
      full_validation=True,
      date_compile_auc=date,
  )
  sd.generate_report(output_file='reports/report-'  + date.strftime("%Y-%m-%d-%H-%M-%S") + '.html')
  
  cursor.execute("INSERT INTO AUC (date, auc) VALUES (%s, %s)", (date.strftime("%Y-%m-%d-%H-%M-%S"), sd.auc))
  cnx.commit()
  
  return send_file('./reports/report-'  + date.strftime("%Y-%m-%d-%H-%M-%S") + '.html', mimetype='text/html', as_attachment=True), 200

@app.route("/get-auc", methods=['GET'])
def get_auc():
  auc = pd.read_sql("SELECT * FROM AUC", cnx)
  return app.response_class(
      response=json.dumps({'AUC': auc.to_dict()}),
      status=200,
    )

@app.route("/get-data", methods=['GET'])
def get_data():
  data = pd.read_sql("SELECT * FROM DF", cnx)
  return app.response_class(
      response=json.dumps({'data': data.to_dict()}),
      status=200,
    )
  
if __name__ == "__main__":
  app.run("0.0.0.0", port=3000)