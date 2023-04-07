import json
from pymongo import MongoClient, ASCENDING, DESCENDING

# Load course data from courses.json
with open('data/courses.json', 'r') as f:
    courses_data = json.load(f)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  
db = client['kimo']
courses_collection = db['courses']

# Drop existing collection if exists
courses_collection.drop()

# Create indices for efficient retrieval
courses_collection.create_index([('name', ASCENDING)])
courses_collection.create_index([('date', DESCENDING)])
courses_collection.create_index([('total_rating', DESCENDING)])

# Insert course data into MongoDB
courses_collection.insert_many(courses_data)
