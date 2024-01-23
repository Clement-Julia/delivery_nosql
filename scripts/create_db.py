import pandas as pd
from pymongo import MongoClient

df = pd.read_csv('./data/train.csv')
client = MongoClient('localhost', 27017)

db = client['food_delivery']
collection = db['edf']

records = df.to_dict('records')
collection.insert_many(records)