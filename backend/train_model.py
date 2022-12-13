import pandas as pd
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from sklearn.cluster import KMeans
import joblib


def get_dataset():
  return pd.read_csv('./datas/Country-data.csv')

def feature_engineering(data):

  # dissolve features into categories and normalize them
  df1 = pd.DataFrame()
  df1['Health'] = (data['child_mort'] / data['child_mort'].mean()) + (data['health'] / data['health'].mean()) + (data['life_expec'] / data['life_expec'].mean()) + (data['total_fer'] / data['total_fer'].mean())
  df1['Trade'] = (data['imports'] / data['imports'].mean()) + (data['exports'] / data['exports'].mean())
  df1['Finance'] = (data['income'] / data['income'].mean()) + (data['inflation'] / data['inflation'].mean()) + (data['gdpp'] / data['gdpp'].mean())


  # Data scaling
  mms = MinMaxScaler() # Normalization
  ss = StandardScaler() # Standardization

  df1['Health'] = mms.fit_transform(df1[['Health']])
  df1['Trade'] = mms.fit_transform(df1[['Trade']])
  df1['Finance'] = mms.fit_transform(df1[['Finance']])
  df1.insert(loc = 0, value = list(data['country']), column = 'Country')
  print(df1.head())
  return df1

def train_model(df1):
  m1 = df1.drop(columns = ['Country']).values # Feature Combination : Health - Trade - Finance
  model = KMeans(n_clusters = 3,max_iter = 1000)
  model.fit(m1)
  return model

def model_predict(model, Health, Trade, Finance):
  pred =  model.predict([[Health, Trade, Finance]])[0]
  if pred == 0:
    return 'might need help'
  elif pred == 1:
    return 'need help'
  else:
    return "don't need help"
  
  
def save_model(model):
  joblib.dump(model, './models/model.joblib')
  
data = get_dataset()
df = feature_engineering(data)
model2 = joblib.load('./models/model.joblib')
pred2 = model_predict(model2, 0.62, 0.2, 0.08)
print(f"Your country {pred2}")

pd.to_pickle(df, './datas/Country-data.pkl')