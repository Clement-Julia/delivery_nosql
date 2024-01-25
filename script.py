import pandas as pd
from pymongo import MongoClient

# Load the CSV data into a pandas DataFrame
df = pd.read_csv('data/train.csv')

# Create a MongoDB client
client = MongoClient('localhost', 27017)

# Create a database named 'mydatabase'
db = client['food_delivery']

# Create a collection named 'mycollection'
collection = db['edf']

# Convert the DataFrame to a list of dictionaries and insert them into the collection
records = df.to_dict('records')
collection.insert_many(records)