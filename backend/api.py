from flask import Flask
from flask import request
import joblib

app = Flask(__name__)

model = joblib.load('./models/model.joblib')

@app.route("/predict", methods=['POST'])
def model_predict():
  Health = request.get_json()['Health']
  Trade = request.get_json()['Trade']
  Finance = request.get_json()['Finance']
  if Health == None or Trade == None or Finance == None:
    return 'Please provide all the features', 400
  
  pred =  model.predict([[Health, Trade, Finance]])[0]
  if pred == 0:
    return 'might need help'
  elif pred == 1:
    return 'need help'
  elif pred == 2:
    return "don't need help", 200
  else:
    return 'Error', 500
  
if __name__ == "__main__":
    app.run("0.0.0.0", port=3000)